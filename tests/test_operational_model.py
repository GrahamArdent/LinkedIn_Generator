import pytest
from src.app import operational_runtime as m


def test_unavailable_requested_model_never_uses_costlier_fallback():
    with pytest.raises(ValueError,match='REQUESTED_MODEL_UNAVAILABLE'):
        m.select_model('gpt-6.1-sol',[{'id':'gpt-6-sol','model':'gpt-6-sol','supportedReasoningEfforts':[{'reasoningEffort':'medium'}]},{'id':'gpt-6-astra','model':'gpt-6-astra'}])
    assert m.select_model('gpt-6.1-sol',[{'id':'gpt-6.1-sol','model':'gpt-6.1-sol','supportedReasoningEfforts':[{'reasoningEffort':'medium'}]}])=='gpt-6.1-sol'
