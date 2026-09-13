from backend.services.security import sanitize_html


def test_sanitize_html_removes_scripts_event_handlers_and_javascript_urls():
    result = sanitize_html(
        '<script>alert(1)</script><a href="javascript:alert(1)" '
        'onclick="alert(1)">unsafe</a><p style="color: red">safe</p>'
    )

    assert "<script" not in result
    assert "onclick" not in result
    assert "javascript:" not in result
    assert 'style="color: red;"' in result
