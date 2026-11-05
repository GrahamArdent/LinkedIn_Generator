"""Versioned style-only projections of recovered voice definitions."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

CATALOG_PATH = Path(__file__).resolve().parents[2] / "config/writing_voices.json"
_TRAITS = {
    "content_style", "avg_sentence_length", "sentence_length_variance",
    "colon_freq", "semicolon_freq", "question_freq", "exclamation_freq",
    "complexity_score", "professional_tone", "conversational_tone", "analytical_tone",
    "inspirational_tone", "controversial_strength", "vulnerability_comfort",
    "question_engagement_level", "preferred_emotional_triggers", "pain_point_intensity",
    "controversy_boundaries", "preferred_structure", "tone", "rhythm", "reasoning", "imagery",
}

def resolve_writing_voice(voice_id: str) -> dict:
    """Resolve a known ID/legacy alias; return no biography or imitation prompt."""
    if not isinstance(voice_id, str) or not voice_id:
        raise ValueError("writing_voice_id must name a known writing voice")
    try:
        catalog = json.loads(CATALOG_PATH.read_text())
        voices = catalog["voices"]
        matches = [(key, value) for key, value in voices.items()
                   if voice_id == key or voice_id in value.get("aliases", [])]
        if len(matches) != 1:
            raise ValueError("unknown or ambiguous writing_voice_id")
        key, value = matches[0]
        traits = value["style_traits"]
        if (type(value["version"]) is not int or value["version"] < 1
                or not isinstance(value["label"], str) or not value["label"].strip()
                or not isinstance(traits, dict) or not traits
                or set(traits) - _TRAITS):
            raise ValueError("invalid writing_voice definition")
        block = {"id": key, "version": value["version"], "label": value["label"],
                 "style_traits": traits}
        block["content_sha256"] = hashlib.sha256(
            json.dumps(block, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        return block
    except (KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
        raise ValueError("writing_voice catalogue unavailable or malformed") from exc
