"""Consumer tests: source qualification must affect trial admission, not just prompt decoration."""
import copy,json,hashlib
import pytest
from src.app import codex_trial

def validate_trial_evidence(*args):
    assert callable(getattr(codex_trial, "validate_trial_evidence", None)), "trial evidence admission is not implemented"
    return codex_trial.validate_trial_evidence(*args)

def fixture():
    data={"topic":"MFA recovery","evidence":[{"title":"S1 advisory","fact":"Help desks were socially engineered to reset MFA."}]}
    bundle={"request_sha256":hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
      "sources":[{"source_id":"S1","status":"usable","checked_at":"2026-11-04","limitations":"Historical tactic; not incidence today."}],
      "claims":[{"claim_id":"C1","kind":"fact","text":data["evidence"][0]["fact"],"source_ids":["S1"]},
                {"claim_id":"C2","kind":"opinion","text":"Review recovery as well as sign-in.","source_ids":[]}],
      "central_claim_id":"C1"}
    return data,bundle

def test_evidence_brief_admits_supported_fact_and_unstatistical_opinion():
    data,bundle=fixture()
    assert validate_trial_evidence(data,bundle) is None

@pytest.mark.parametrize("status",["missing","stale","contradicted"])
def test_unusable_central_source_blocks_before_provider_launch(status):
    data,bundle=fixture()
    bundle["sources"][0]["status"]=status
    with pytest.raises(ValueError,match="EVIDENCE_SUPPORT_REQUIRED"):
        validate_trial_evidence(data,bundle)

def test_missing_source_and_changed_frozen_request_block():
    data,bundle=fixture()
    bundle["sources"]=[]
    with pytest.raises(ValueError,match="EVIDENCE_SUPPORT_REQUIRED"): validate_trial_evidence(data,bundle)
    data,bundle=fixture();data["evidence"][0]["fact"]="An invented financial loss."
    with pytest.raises(ValueError,match="EVIDENCE_REQUEST_MISMATCH"): validate_trial_evidence(data,bundle)
