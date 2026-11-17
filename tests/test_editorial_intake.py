import json
from pathlib import Path

import pytest

from src.app import operational
from src.app.codex_provider import CodexConfig
from src.app.operational_store import Store


def capture_writer(tmp_path, monkeypatch, topic, notes, reader, takeaway, beats=None, form=None):
    """Use the application up to its formatted outbound request, in a disposable store."""
    captured = {}
    app = operational.Application(Store.initialize(tmp_path / 'store'),
                                  CodexConfig(tmp_path, Path('/unused'), 'offline', 'fixture'))
    monkeypatch.setattr(operational, 'qualify_model', lambda cfg: {'model': cfg.model})

    class Captured(Exception):
        pass

    class OfflineProvider:
        def __init__(self, *args):
            self.receipts = []

        def generate(self, **request):
            if captured:
                assert request['system'].startswith('Write a LinkedIn post')
                captured['writer'] = request
                raise Captured()
            captured['preparation'] = request
            source = json.loads(request['user'])['sources'][0]
            self.receipts.append({'attempt_id': 'fixture-preparation'})
            return json.dumps({
                'status': 'ready', 'reason': 'Bounded offline fixture', 'intended_reader': reader,
                'meaning': {'thesis': topic, 'reader_consequence': takeaway,
                            'qualification': source['limitations'],
                            'facts': [{'claim_id': 'C1', 'source_id': source['source_id'],
                                       'locator': source['passages'][0]['locator']}]},
                'narrative': {'form':'literal','beats':beats or ['Describe the reader’s decision.'],'symbol':None},
                'support_checks': [{'claim_id': 'C1', 'relevant': True, 'primary_source': True,
                                    'entails': True, 'contradicted': False,
                                    'reason': 'Only the stated wording or proposed point is supported.'}],
            })

    monkeypatch.setattr(operational, 'CodexProvider', OfflineProvider)
    saved = app.save_idea('idea', topic, notes=notes, narrative=form)
    assert saved['brief']['notes'] == notes and not app.store.list()
    with pytest.raises(Captured):
        app.draft_item('idea', 'offline-attempt', expected_brief=1, expected_text=None)
    captured['prepared'] = app.store.stage('offline-attempt', 'preparation')
    captured['brief'] = saved['brief']
    return captured


@pytest.mark.parametrize('is_quote', [True, False])
def test_wording_at_writer_boundary(tmp_path, monkeypatch, is_quote):
    words = 'Who put {allowed_sources} on this form?'
    label = 'AUTHOR WORDS' if is_quote else 'EDITORIAL SUMMARY'
    reader = 'A team lead redesigning a form'
    takeaway = 'Identify which decision requires an extra field.'
    notes = f'{label}: {words}\nEDITORIAL DIRECTION: {takeaway}'
    captured = capture_writer(tmp_path, monkeypatch, 'Form design', notes, reader, takeaway)
    writer = captured['writer']
    profile, _ = json.JSONDecoder().raw_decode(writer['user'].split('Persona Profile: ', 1)[1])
    context = profile['editorial_context']
    assert context['source_bundle']['author_intent']['notes'] == notes
    source, = context['source_bundle']['sources']
    passage, = source['passages']
    assert passage['excerpt'] == words
    assert passage['wording'] == ('verbatim' if is_quote else 'editorial_paraphrase')
    assert 'narrative' not in captured['brief']
    assert context['handoff']['narrative']['beats'] == ['Describe the reader’s decision.']
    assert source['publisher'] == ('Graham Hill' if is_quote else 'Brief editor')
    assert f'Audience: {reader}\n' in writer['user']
    assert context['handoff']['meaning']['reader_consequence'] == takeaway
    assert 'Express a reported account or editorial_paraphrase indirectly' in writer['system']


def test_explicit_literal_retains_selected_structure(tmp_path, monkeypatch):
    from src.app.editorial_structure import DEFAULT_BEATS
    result = capture_writer(tmp_path, monkeypatch, 'Choosing a form', 'A reported viewpoint.',
                            'A business reader', 'Choose a form for this audience.', form='literal')
    assert result['prepared']['request']['editorial_handoff']['narrative']['beats'] == DEFAULT_BEATS


def test_missing_reader_stops_before_writer(tmp_path, monkeypatch):
    with pytest.raises(ValueError, match='INVALID_INTENDED_READER'):
        capture_writer(tmp_path, monkeypatch, 'Choosing a form', 'An account.', '', 'Choose an audience.')


def test_clarification_survives_reopen_and_answer_retires_question(tmp_path, monkeypatch):
    app = operational.Application(Store.initialize(tmp_path/'clarification'),
                                  CodexConfig(tmp_path, Path('/unused'), 'offline', 'fixture'))
    monkeypatch.setattr(operational, 'qualify_model', lambda cfg: {})
    question = 'Which part of planning the meeting actually held up the decision?'
    class Provider:
        def __init__(self, *args):
            self.receipts = []
        def generate(self, **request):
            assert 'Do not ask for sample preferences' in request['system']
            self.receipts.append({'attempt_id':'held'})
            return json.dumps({'status':'needs_more_evidence','reason':question,'meaning':None,
                               'narrative':None,'support_checks':[]})
    monkeypatch.setattr(operational, 'CodexProvider', Provider)
    app.save_idea('item','Planning meetings')
    result = app.draft_item('item','held',expected_brief=1,expected_text=None)
    assert result['state'] == 'needs_more_evidence'
    reopened = operational.Application(Store(app.store.root), None)
    assert reopened.show('item')['author_question'] == question
    reopened.save_idea('item','Planning meetings',notes='AUTHOR WORDS: We waited for an agenda.',expected_brief=1)
    assert 'author_question' not in reopened.show('item')
    assert len(reopened.store.list()) == 1
    assert reopened.store.get('held')['result']['author_question'] == question
