from src.app.citations import filter_to_whitelist


def test_filter_to_whitelist():
    cites = [
        {"title": "IBM Report", "url": "https://www.ibm.com/reports/data-breach"},
        {"title": "Random Blog", "url": "https://randomblog.example/post"},
    ]
    wl = {"ibm.com"}
    out = filter_to_whitelist(cites, wl)
    assert len(out) == 1
    assert out[0]["title"] == "IBM Report"
