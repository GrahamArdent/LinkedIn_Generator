"""No-model Graham structure compilation and exact pre-dispatch validation.

This is input provenance, not a signature or a substitute for source adjudication.
Existing completed trials remain immutable and are reconciled before this boundary.
"""
from copy import deepcopy
import fcntl
import hashlib
import json
from pathlib import Path

from .contracts import LinkedInContentRequest
from .editorial_handoff import freeze_handoff, validate_handoff
from .codex_trial import validate_trial_evidence

STRUCTURE_ID = 'graham-structured-v1'
STRUCTURE_VERSION = 1
DEFAULT_BEATS = [
    'Hook: introduce the central question.',
    'Tension: develop why the question matters.',
    'Evidence: place the relevant sourced facts.',
    "Interpretation: develop Graham's reading and its limits.",
    'Landing: earn the closing thought from the argument.',
]

def _hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

def _definition_hash():
    return _hash({'id': STRUCTURE_ID, 'version': STRUCTURE_VERSION, 'default_beats': DEFAULT_BEATS})

def _input_hash(data, bundle):
    source = {k:v for k,v in bundle.items() if k not in ('request_sha256', 'structure_preparation')}
    return _hash({'request': data, 'source_bundle': source})

def _supported_handoff(data, bundle):
    h = validate_handoff(data['editorial_handoff'])
    claims = {c['claim_id']:c for c in bundle['claims']}
    for fact in h['meaning']['facts']:
        c = claims.get(fact['claim_id'], {})
        if (c.get('kind') not in ('fact', 'observation') or c.get('text') != fact['text']
                or not set(fact['source_ids']).issubset(c.get('source_ids', []))):
            raise ValueError('STRUCTURE_PREPARATION_INVALID: unsupported handoff fact/source')
    LinkedInContentRequest.model_validate(data)

def prepare_graham_request(data: dict, bundle: dict):
    data, bundle = deepcopy(data), deepcopy(bundle)
    if not isinstance(data, dict) or data.get('persona_key', 'graham') != 'graham':
        raise ValueError('STRUCTURE_PREPARATION_INVALID: Graham persona required')
    if not isinstance(bundle, dict):
        raise ValueError('STRUCTURE_PREPARATION_REQUIRED: evidence bundle required')
    if 'structure_preparation' in bundle:
        validate_prepared_request(data, bundle)
        return data, bundle
    validate_trial_evidence(data, bundle)
    h = data.get('editorial_handoff')
    if not isinstance(h, dict) or not isinstance(h.get('meaning'), dict):
        raise ValueError('STRUCTURE_PREPARATION_REQUIRED: explicit meaning required')
    if set(h) - {'version', 'meaning', 'narrative', 'writing_plan'}:
        raise ValueError('STRUCTURE_PREPARATION_INVALID: unexpected handoff fields')
    provenance = 'caller-selected' if 'narrative' in h else 'default'
    if 'narrative' not in h:
        if 'writing_plan' in h or ('version' in h and h['version'] != 1):
            raise ValueError('STRUCTURE_PREPARATION_INVALID: incomplete selected plan')
        data['editorial_handoff'] = freeze_handoff(h['meaning'],
            {'form': 'literal', 'beats': DEFAULT_BEATS, 'symbol': None})
    else:
        # Supply the current envelope version without changing caller-selected narrative.
        data['editorial_handoff'] = validate_handoff({'version': 1, **h})
    bundle['request_sha256'] = _hash(data)
    _supported_handoff(data, bundle)
    bundle['structure_preparation'] = {
        'id': STRUCTURE_ID, 'version': STRUCTURE_VERSION,
        'definition_sha256': _definition_hash(), 'input_sha256': _input_hash(data, bundle),
        'prepared_request_sha256': _hash(data), 'provenance': provenance,
        'writing_voice_id': data.get('writing_voice_id'),
    }
    validate_prepared_request(data, bundle)
    return data, bundle

def validate_prepared_request(data: dict, bundle: dict):
    if not isinstance(bundle, dict) or not isinstance(bundle.get('structure_preparation'), dict):
        raise ValueError('STRUCTURE_PREPARATION_REQUIRED: use prepare before generate')
    b = bundle['structure_preparation']
    expected = {'id', 'version', 'definition_sha256', 'input_sha256',
                'prepared_request_sha256', 'provenance', 'writing_voice_id'}
    if (set(b) != expected or data.get('persona_key', 'graham') != 'graham'
            or b['id'] != STRUCTURE_ID or type(b['version']) is not int
            or b['version'] != STRUCTURE_VERSION or b['definition_sha256'] != _definition_hash()
            or b['input_sha256'] != _input_hash(data, bundle)
            or b['prepared_request_sha256'] != _hash(data)
            or b['writing_voice_id'] != data.get('writing_voice_id')
            or b['provenance'] not in ('default', 'caller-selected')):
        raise ValueError('STRUCTURE_PREPARATION_INVALID: stale or inconsistent binding; use prepare')
    validate_trial_evidence(data, bundle)
    _supported_handoff(data, bundle)
    if b['provenance'] == 'default' and data['editorial_handoff']['narrative'] != {
            'form':'literal', 'beats':DEFAULT_BEATS, 'symbol':None}:
        raise ValueError('STRUCTURE_PREPARATION_INVALID: default narrative changed')

def save_preparation(directory, data, bundle):
    """Conflict-safe, no-model preparation. Partial writes fail closed on reopen."""
    data, bundle = prepare_graham_request(data, bundle)
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory/'.prepare.lock').open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        outputs = {'request.json':data, 'source-bundle.json':bundle}
        encoded = {name:json.dumps(value, indent=2, ensure_ascii=False)+'\n' for name,value in outputs.items()}
        present = [name for name in outputs if (directory/name).exists()]
        if present:
            if len(present) != 2 or any((directory/name).read_text() != text for name,text in encoded.items()):
                raise ValueError('STRUCTURE_PREPARATION_CONFLICT: preserve existing outputs')
        else:
            if (directory/'trial.json').exists():
                raise ValueError('STRUCTURE_PREPARATION_CONFLICT: trial directory is not preparation output')
            for name,text in encoded.items():
                temporary = directory/(name+'.tmp')
                temporary.write_text(text)
                temporary.replace(directory/name)
    return {'state':'prepared', 'mode':'no_model', 'structure_preparation':bundle['structure_preparation']}
