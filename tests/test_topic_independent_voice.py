"""A reusable voice must not inject a previous story's substantive argument."""
import json
import pytest
from src.app import api

@pytest.mark.parametrize("topic,objective",[
 ("Stellar spectra","Explain how evidence supports a scientific interpretation."),
 ("Compost decomposition","Explain one useful distinction supported by the supplied material."),
])
def test_technical_style_does_not_inject_recorded_versus_enforced_argument(topic,objective):
    class Captured(Exception):pass
    class Client:
        def call(self,system,user,response_json=True):
            self.system,self.user=system,user
            raise Captured
    c=Client()
    with pytest.raises(Captured):
        api.run_generation(topic,[],persona_key="graham",audience="Curious professionals",
            objective=objective,writing_voice_id="technical_explainer",allowed_sources=[],
            opportunity_gate=False,publish_quality_gate=False,llm_client=c)
    profile=json.loads(next(x.split(": ",1)[1] for x in c.user.splitlines() if x.startswith("Persona Profile: ")))
    assert profile["editorial_context"]["objective"]==objective
    assert c.user.count(objective)==1
    assert "Separate what is recorded from what is enforced." not in c.user, "style injected a prior story's conclusion"
    assert not {"voice_authority","spoken_voice","tone","rhythm","devices"}.intersection(profile)
