from src.app.validators import (
    append_sources_block,
    apply_house_rules,
    cap_emojis,
    clamp_hashtags,
    normalize_bullets,
    remove_links,
    replace_em_dashes,
)


def test_no_links_in_body():
    body, urls = remove_links("X http://a.com Y https://b.co Z")
    assert "http" not in body
    assert len(urls) == 2


def test_append_sources():
    out = append_sources_block("Body", ["http://a.com", "https://b.co"])
    assert "Sources:" in out


def test_bullets_and_emojis():
    t = normalize_bullets("- a\n• b\n- c", bullet="🔹")
    assert "🔹 a" in t and "🔹 b" in t
    t2 = cap_emojis("hi 😀😀😀😀", max_n=3)
    assert t2.count("😀") == 3


def test_em_dash_replacement():
    assert "—" not in replace_em_dashes("a—b")


def test_clamp_hashtags():
    clamped = clamp_hashtags(["#a", "#b", "#c", "#d", "#e", "#f"], 3, 5)
    assert len(clamped) == 5


def test_apply_house_rules():
    clean, issues = apply_house_rules(
        "— test\n- item", bullet="🔹", emoji_max=3, allow_em_dash=False
    )
    assert "—" not in clean
    assert "🔹 item" in clean
