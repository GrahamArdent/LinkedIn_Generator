
from __future__ import annotations
from typing import Dict, Any, Optional

DEFAULT_MAPPING = {
    "identity": {"pillar":"trend_decode","services":["adversarial_simulation","vulnerability_assessment"]},
    "third_party": {"pillar":"vendor_risk_teardown","services":["penetration_testing","compliance"]},
    "training": {"pillar":"checklist_drop","services":["training","compliance"]},
}

def infer_topic_key(topic: str) -> str:
    t = (topic or "").lower()
    if any(k in t for k in ["identity","oauth","okta","sso","mfa"]):
        return "identity"
    if any(k in t for k in ["vendor","third party","supply chain","saas"]):
        return "third_party"
    if any(k in t for k in ["training","awareness","phish","vishing","deepfake"]):
        return "training"
    return "identity"

def enrich_with_persona_rules(payload: Dict[str, Any], persona_key: str, topic: str) -> Dict[str, Any]:
    key = infer_topic_key(topic)
    mapping = DEFAULT_MAPPING.get(key, DEFAULT_MAPPING["identity"])
    # attach lightweight metadata to steer design/CTA down the line
    payload.setdefault("metadata",{})
    payload["metadata"]["inferred_pillar"] = mapping["pillar"]
    payload["metadata"]["service_map"] = mapping["services"]
    payload["metadata"]["topic_key"] = key
    # persona-specific CTA override example
    if persona_key.startswith("ardent"):
        payload["metadata"]["cta_override"] = "Book an assessment"
    return payload
