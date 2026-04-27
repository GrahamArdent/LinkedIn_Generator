from src.app.composer import compose_post


def test_compose_post_minimal():
    blocks = {
        "personas": {
            "graham_thought_leadership": {
                "cta_patterns": ["Comment CHECKLIST for a 1-pager"],
                "hashtag_set": "graham_core",
            }
        },
        "prompts": {
            "skeleton": {
                "sections": [
                    "hook",
                    "exec_pov",
                    "proof_point",
                    "micro_plays",
                    "quote",
                    "cta",
                    "hashtags",
                ]
            },
            "section_templates": {},
        },
        "hashtags": {"graham_core": ["#a", "#b", "#c"]},
    }
    p = compose_post(
        "graham_thought_leadership",
        blocks,
        {"quote": "q", "author": "a", "source": "s"},
        {"metric": "m", "value": "1", "unit": "", "source": "src", "date": "2025"},
    )
    assert "Comment CHECKLIST" in p["body"]
