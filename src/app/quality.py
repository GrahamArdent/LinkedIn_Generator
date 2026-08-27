from __future__ import annotations

import re
from typing import Any

LINK_RE = re.compile(r"https?://\S+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF]")
EM_DASH = "—"
CONTRAST_RE = re.compile(
    r"\b(?:but|instead|rather than|versus|vs\.?|not only|not .{0,40} but)\b",
    re.IGNORECASE,
)
COLLECTIVE_PRONOUN_RE = re.compile(r"\b(?:we|us|our|ours)\b", re.IGNORECASE)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n+")


def _word_count(text: str) -> int:
    return len(re.findall(r"\b\w+[\w'-]*\b", text))


def _paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()]


def _semantic_rules(persona: dict[str, Any]) -> dict[str, Any]:
    direct = persona.get("semantic_quality")
    if isinstance(direct, dict):
        return direct
    authority = persona.get("voice_authority")
    if isinstance(authority, dict):
        nested = authority.get("semantic_quality")
        if isinstance(nested, dict):
            return nested
    return {}


def _matched_phrases(text: str, phrases: list[Any]) -> list[str]:
    lower = text.lower()
    matches: list[str] = []
    for item in phrases:
        phrase = str(item).strip().lower()
        if phrase and phrase in lower:
            matches.append(phrase)
    return list(dict.fromkeys(matches))


def evaluate_quality(
    text: str,
    persona: dict[str, Any],
    rules: dict[str, Any],
) -> dict[str, Any]:
    """Return an explainable deterministic quality assessment.

    This evaluates observable structure plus explicit public-language, POV and
    generic-language rules. It does not claim to prove subjective voice traits.
    """

    score = 100
    issues: list[str] = []
    signals: dict[str, Any] = {}

    word_count = _word_count(text)
    signals["word_count"] = word_count
    if word_count < 40:
        score -= 8
        issues.append("Draft is too thin to develop a useful LinkedIn point.")
    elif word_count > 320:
        score -= 8
        issues.append("Draft is longer than the current concise-post guardrail.")

    if LINK_RE.search(text):
        score -= 20
        issues.append("Publishable body contains a URL.")

    emoji_count = len(EMOJI_RE.findall(text))
    emoji_max = int(rules.get("emoji_max", persona.get("emoji_max", 3)))
    signals["emoji_count"] = emoji_count
    if emoji_count > emoji_max:
        penalty = min(15, 5 * (emoji_count - emoji_max))
        score -= penalty
        issues.append(f"Emoji count exceeds configured maximum of {emoji_max}.")

    allow_em_dash = bool(rules.get("allow_em_dash", False))
    if EM_DASH in text and not allow_em_dash:
        score -= 10
        issues.append("Draft contains an em dash even though the profile forbids it.")

    paragraphs = _paragraphs(text)
    sentences = _sentences(text)
    paragraph_lengths = [_word_count(p) for p in paragraphs]
    sentence_lengths = [_word_count(s) for s in sentences]
    signals["paragraph_word_counts"] = paragraph_lengths
    signals["sentence_word_counts"] = sentence_lengths

    rhythm = {str(item) for item in persona.get("rhythm", [])}
    wants_compact_rhythm = bool({"short_paragraphs", "tight", "punchy"} & rhythm)
    if wants_compact_rhythm:
        long_paragraphs = sum(1 for n in paragraph_lengths if n > 70)
        if long_paragraphs:
            score -= min(16, 8 * long_paragraphs)
            issues.append("One or more paragraphs are too long for the configured compact rhythm.")

        long_sentences = sum(1 for n in sentence_lengths if n > 35)
        if long_sentences:
            score -= min(12, 6 * long_sentences)
            issues.append("One or more sentences are too long for the configured punchy rhythm.")

    devices = {str(item) for item in persona.get("devices", [])}
    has_question = "?" in text
    has_contrast = bool(CONTRAST_RE.search(text))
    active_goal = str(persona.get("active_content_goal") or "").strip()
    earned_question = bool(persona.get("earned_question", False))
    signals["has_question"] = has_question
    signals["has_contrast"] = has_contrast
    signals["active_content_goal"] = active_goal or None
    signals["earned_question"] = earned_question

    # A question is a device, not a universal requirement. Research-backed
    # conversation strategy only requires one when the opportunity preflight
    # identifies enough genuine conversation potential to earn it.
    if "question" in devices and active_goal == "conversation" and earned_question and not has_question:
        score -= 5
        issues.append("Conversation-goal draft is missing the specific question this opportunity earned.")
    if "contrast" in devices and not has_contrast:
        score -= 3
        issues.append("Configured contrast device is absent.")

    forbidden_phrases = [
        str(item).strip().lower()
        for item in rules.get("forbidden_phrases", [])
        if str(item).strip()
    ]
    matched_forbidden = [phrase for phrase in forbidden_phrases if phrase in text.lower()]
    signals["matched_forbidden_phrases"] = matched_forbidden
    if matched_forbidden:
        score -= min(30, 15 * len(matched_forbidden))
        issues.append("Draft contains a repository-defined forbidden CTA phrase.")

    semantic = _semantic_rules(persona)
    internal_terms = _matched_phrases(text, list(semantic.get("internal_terms_needing_translation", []) or []))
    generic_phrases = _matched_phrases(text, list(semantic.get("generic_phrases", []) or []))
    signals["matched_internal_terms"] = internal_terms
    signals["matched_generic_phrases"] = generic_phrases

    if internal_terms:
        score -= min(24, 6 * len(internal_terms))
        issues.append("Draft uses internal project language that should be translated for a public reader.")

    if generic_phrases:
        score -= min(24, 8 * len(generic_phrases))
        issues.append("Draft contains stock LinkedIn/AI phrasing that weakens specificity and voice.")

    author_pov = str(persona.get("active_author_pov") or semantic.get("default_author_pov") or "").strip()
    collective_pronouns = COLLECTIVE_PRONOUN_RE.findall(text)
    signals["author_pov"] = author_pov or None
    signals["collective_pronoun_count"] = len(collective_pronouns)
    if author_pov == "individual" and collective_pronouns:
        score -= min(18, 6 * len(collective_pronouns))
        issues.append("Individual-author post uses collective we/us/our language without shared-action context.")

    unscored_traits: list[str] = []
    unscored_traits.extend(str(item) for item in persona.get("tone", []))
    if "clichés" in {str(item) for item in persona.get("donts", [])}:
        unscored_traits.append("clichés beyond the explicit generic-phrase list")
    signals["unscored_traits"] = list(dict.fromkeys(unscored_traits))

    return {
        "score": max(0, min(100, score)),
        "issues": issues,
        "signals": signals,
    }
