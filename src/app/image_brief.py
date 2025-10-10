from __future__ import annotations
from typing import Dict, Any

def make_carousel_brief(payload: Dict[str, Any]) -> Dict[str, Any]:
    persona = payload.get("persona")
    tone = "executive, calm, precise" if persona == "graham" else "practical, action-forward"
    return {
        "tone": tone,
        "color": "neutral with brand accent",
        "layout": "document carousel: bold hook slide + 3 action slides + CTA slide",
        "avoid": ["clip art", "tiny text", "jargon"],
        "keywords": ["identity", "continuity", "SaaS trust", "controls", "roadmap"],
    }
