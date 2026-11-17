import json

import pytest

from src.app.publish_quality import ESSENTIAL_CHECKS, assess_publish_quality


def assess(parent, text, response):
    class Fixture:
        def call(self, system, user, **kwargs):
            request = json.loads(user)
            assert request['post'] == text
            assert request.get('parent_post') == parent
            assert 'passage' in request['required_output']['essential_checks']['argument_voice']
            return {'text': json.dumps(response)}
    return assess_publish_quality(text=text, parent_text=parent, audience='Workflow owners',
                                  content_goal='Explain', evidence=[], persona_profile={'editorial_context': {'brief': {}}},
                                  client=Fixture())


@pytest.mark.parametrize('corruption', [None, 'wrong_parent', 'invented', 'missing', 'swapped'])
def test_revision_reasons_bound_to_both_passages(corruption):
    parent = 'I check who owns the decision. Then I ask what the form protects.'
    current = 'I check who owns the decision.'
    response = {'essential_checks': {key: {'verdict': 'pass', 'reason': 'Names the decision owner.',
                                          'passage': current} for key in ESSENTIAL_CHECKS},
                'revision_comparison': {'change': 'loss', 'parent_passage': 'what the form protects',
                                        'current_passage': current, 'reason': 'The second decision question disappears.'}}
    if corruption == 'wrong_parent':
        response['revision_comparison']['parent_passage'] = 'invented'
    if corruption == 'invented':
        response['essential_checks']['practical_value']['passage'] = 'invented'
    if corruption == 'missing':
        del response['revision_comparison']
    if corruption == 'swapped':
        response['revision_comparison']['current_passage'] = 'what the form protects'
    result = assess(parent, current, response)
    assert result.review_status == ('assessment_unavailable' if corruption else 'reviewable')
    if not corruption:
        assert result.as_dict()['revision_comparison']['change'] == 'loss'


def test_absent_contribution_can_be_flagged_without_inventing_a_quote():
    text = 'The meeting ended.'
    checks = {key: {'verdict':'pass', 'reason':'Names the recorded event.', 'passage':text}
              for key in ESSENTIAL_CHECKS}
    checks['argument_voice'] = {'verdict':'revise', 'reason':'No judgment about the event is supplied.', 'passage':''}
    assert assess(None, text, {'essential_checks':checks}).review_status == 'needs_rework'
