import json
from pathlib import Path

import pytest

from src.app import operational
from src.app.codex_provider import CodexConfig
from src.app.operational_store import Store


def capture_writer(tmp_path, monkeypatch, topic, notes, reader, takeaway, beats=None, form=None, null_narrative=False):
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
                'narrative': None if null_narrative else {'form':'literal','beats':beats or ['Describe the reader’s decision.'],'symbol':None},
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
            assert json.loads(request['user'])['sources'] == []
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

def test_auto_form_can_resolve_a_native_null_after_the_reader_choice(tmp_path, monkeypatch):
    from src.app.editorial_structure import DEFAULT_BEATS
    r = capture_writer(tmp_path, monkeypatch, 'A workflow choice', 'AUTHOR WORDS: Start with the question.',
                       'A workflow owner', 'Identify the decision first.', null_narrative=True)
    q = r['prepared']['request']
    assert q['audience'] == 'A workflow owner' and q['objective'] == 'Identify the decision first.'
    assert q['editorial_handoff']['narrative']['beats'] == DEFAULT_BEATS


@pytest.mark.parametrize('label,source_id', [('EDITORIAL SUMMARY', 'B1'), ('AUTHOR WORDS', 'U1')])
def test_calendar_angle_preserves_ownership_at_writer_boundary(tmp_path, monkeypatch, label, source_id):
    topic = 'CIO pain: tool sprawl chaos'
    recommendation = 'Before renewal, ask what decision each tool helps someone make.'
    captured = capture_writer(tmp_path, monkeypatch, topic, f'{label}: {recommendation}',
                              'A CIO considering two renewals', 'Identify each tool’s purpose.')
    writer = captured['writer']
    profile, _ = json.JSONDecoder().raw_decode(writer['user'].split('Persona Profile: ', 1)[1])
    source, = profile['editorial_context']['source_bundle']['sources']
    assert source['source_id'] == source_id
    assert source['passages'][0]['excerpt'] == recommendation
    assert "only when Graham's supplied account supports that specific recommendation" in writer['system']


@pytest.mark.parametrize('scenario', ['reuse', 'different_topic', 'unavailable'])
def test_direction_only_reuses_cited_public_source(tmp_path, monkeypatch, scenario):
    app = operational.Application(Store.initialize(tmp_path / 'source-reuse'),
                                  CodexConfig(tmp_path, Path('/unused'), 'offline', 'fixture'))
    monkeypatch.setattr(operational, 'qualify_model', lambda cfg: {})
    topic = 'CIO pain: tool sprawl chaos'
    url = 'https://example.org/playbook'
    source = {'source_id': 'S1', 'url': url, 'status': 'usable', 'passages': [
        {'locator': 'paragraph 1', 'excerpt': 'An official guide describes application rationalization.'},
    ]}
    app.store.admit('prior', {'topic': topic, 'writing_snapshot': {}}, {})
    operational.commit_pure_stage(app.store, 'prior', 'preparation', {}, {'bundle': {
        'claims': [{'source_ids': ['S1']}],
        'sources': [source, {**source, 'source_id': 'S2', 'url': 'https://example.org/uncited'}],
    }})
    app.store.finish('prior', 'completed', {})
    fetches = []

    def acquire(self, requested_topic, urls, *, include_regulatory=False):
        assert include_regulatory == (scenario == 'different_topic')
        fetches.extend(urls)
        assert requested_topic == ('A different topic' if scenario == 'different_topic' else topic)
        assert urls == ([] if scenario == 'different_topic' else [url])
        return {'sources': [source] if scenario == 'reuse' else [],
                'errors': [] if scenario == 'reuse' else [{'error': 'SOURCE_HTTP_404'}],
                'http_activity': [{'url': url}]}

    monkeypatch.setattr(operational.Evidence, 'acquire', acquire)

    class Provider:
        def __init__(self, *args):
            self.receipts = []

        def generate(self, **request):
            assert scenario == 'reuse'
            assert json.loads(request['user'])['sources'] == [source]
            self.receipts.append({'attempt_id': 'preparation'})
            return json.dumps({'status': 'needs_more_evidence', 'reason': 'Which renewal decision?',
                               'meaning': None, 'narrative': None, 'support_checks': []})

    monkeypatch.setattr(operational, 'CodexProvider', Provider)
    app.save_idea('idea', 'A different topic' if scenario == 'different_topic' else topic,
                  notes='EDITORIAL DIRECTION: Compare two renewals.')
    result = app.draft_item('idea', 'attempt', expected_brief=1, expected_text=None)
    assert fetches == ([] if scenario == 'different_topic' else [url])
    if scenario == 'reuse':
        assert result['result']['author_question'] == 'Which renewal decision?'
    else:
        assert result['result']['author_question'] == 'Which specific observation or source passage should the post build on?'


@pytest.mark.parametrize('scenario', ['empty', 'unrelated', 'supported'])
def test_ed_direction_can_discover_public_sources(tmp_path, monkeypatch, scenario):
    app = operational.Application(Store.initialize(tmp_path / 'cold-discovery'),
                                  CodexConfig(tmp_path, Path('/unused'), 'offline', 'fixture'))
    monkeypatch.setattr(operational, 'qualify_model', lambda cfg: {})
    topic = 'Choosing a backup schedule'
    url = 'https://example.org/guide'
    discovered = []
    requests = []
    excerpt = ('A baking guide discusses oven temperature.' if scenario == 'unrelated'
               else 'Choose a backup schedule based on tolerable data loss.')

    def discover(self, requested_topic):
        discovered.append(requested_topic)
        return [] if scenario == 'empty' else [url]

    def fetch(self, requested_url):
        assert requested_url == url
        return url, f'<title>Planning guide</title><p>{excerpt}</p>'.encode(), 'text/html'

    monkeypatch.setattr(operational.Evidence, 'discover', discover)
    monkeypatch.setattr(operational.Evidence, 'fetch', fetch)

    class WriterReached(Exception):
        pass

    class Provider:
        def __init__(self, *args):
            self.receipts = []

        def generate(self, **request):
            requests.append(request)
            if len(requests) == 2:
                assert scenario == 'supported'
                assert request['system'].startswith('Write a LinkedIn post')
                assert excerpt in request['user']
                raise WriterReached()
            source, = json.loads(request['user'])['sources']
            assert source['url'] == url and 'record' not in source
            passage = next(p for p in source['passages'] if p['excerpt'] == excerpt)
            self.receipts.append({'attempt_id': 'fixture-preparation'})
            return json.dumps({
                'status': 'ready', 'reason': 'Fixture', 'intended_reader': 'A team setting recovery goals',
                'meaning': {'thesis': 'Review recovery goals', 'reader_consequence': 'Define tolerable data loss.',
                            'qualification': 'This guide provides general planning advice.',
                            'facts': [{'claim_id': 'C1', 'source_id': 'S1', 'locator': passage['locator']}]},
                'narrative': None,
                'support_checks': [{'claim_id': 'C1', 'relevant': scenario == 'supported',
                                    'primary_source': True, 'entails': scenario == 'supported',
                                    'contradicted': False, 'reason': 'Fixture support check.'}],
            })

    monkeypatch.setattr(operational, 'CodexProvider', Provider)
    app.save_idea('idea', topic, notes='EDITORIAL DIRECTION: Explain the recovery decision.')
    if scenario == 'unrelated':
        with pytest.raises(ValueError, match='UNSUPPORTED_MEANING'):
            app.draft_item('idea', 'attempt', expected_brief=1, expected_text=None)
    elif scenario == 'supported':
        with pytest.raises(WriterReached):
            app.draft_item('idea', 'attempt', expected_brief=1, expected_text=None)
    else:
        result = app.draft_item('idea', 'attempt', expected_brief=1, expected_text=None)
        assert result['state'] == 'needs_more_evidence'
        assert result['result']['author_question']
    assert discovered == [topic]
    assert len(requests) == {'empty': 0, 'unrelated': 1, 'supported': 2}[scenario]
    assert app.store.stage('attempt', 'evidence')['candidate_origin'] == 'public_discovery'


def test_public_rules_are_navigation_and_acquired_as_separate_sources(monkeypatch):
    from src.app.operational_evidence import Evidence

    seen = []
    document = 'https://www.govinfo.gov/content/pkg/FR-2025-01-17/html/2025-12345.htm'
    topic = 'Incident disclosure responsibilities'

    def fetch(self, url, *, discovery=False):
        seen.append((url, discovery))
        if discovery:
            assert url.startswith('https://www.federalregister.gov/api/v1/documents.json?')
            from urllib.parse import parse_qs, urlsplit
            assert parse_qs(urlsplit(url).query)['conditions[term]'] == [topic]
            return url, json.dumps({'results': [
                {'publication_date': '2025-01-17', 'document_number': '2025-12345',
                 'html_url': 'https://example.org/untrusted', 'abstract': 'Search metadata alone.'},
                {'publication_date': '2025-01-17', 'document_number': '../../bad'},
            ]}).encode(), 'application/json'
        assert url == document
        return url, b'<title>A rule</title><p>The published rule explains disclosure responsibility.</p>', 'text/html'

    monkeypatch.setattr(Evidence, 'fetch', fetch)
    monkeypatch.setattr(Evidence, 'discover', lambda self, requested: [])
    assert Evidence().acquire(topic)['sources'] == []
    assert Evidence().acquire('A general writing topic', include_regulatory=True)['sources'] == []
    assert seen == []
    discovered = Evidence().acquire(topic, include_regulatory=True)
    source, = discovered['sources']
    assert seen[1:] == [(document, False)]
    assert source['url'] == document
    passages = [p['excerpt'] for p in source['passages']]
    assert 'Search metadata alone.' not in passages
    assert 'The published rule explains disclosure responsibility.' in passages
