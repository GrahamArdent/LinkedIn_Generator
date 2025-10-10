from src.app.generation import sanitize_and_validate

def test_sanitize_hashtags():
    text = "Hello world"
    fixed = sanitize_and_validate(text)
    assert "#CyberSecurity" in fixed
