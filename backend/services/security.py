import re

import bleach
from bleach.css_sanitizer import CSSSanitizer

# Generated artifacts are untrusted. Scripts, forms, frames, and images are
# blocked. CSS is limited to layout/typography properties.
ALLOWED_TAGS = [
    "h1", "h2", "h3", "h4", "h5", "h6",
    "p", "a", "ul", "ol", "li", "b", "i", "strong", "em", "s",
    "code", "pre", "hr", "br", "div", "span", "blockquote",
    "table", "thead", "tbody", "tr", "th", "td",
    "style",
]

ALLOWED_ATTRIBUTES = {
    "*": ["class", "id"],
    "a": ["href", "title"],
    "p": ["style"],
    "div": ["style"],
    "span": ["style"],
    "h1": ["style"],
    "h2": ["style"],
    "h3": ["style"],
    "td": ["style"],
    "th": ["style"],
}

ALLOWED_STYLES = [
    "color", "background-color", "font-family", "font-size", "font-weight",
    "text-align", "margin", "padding", "border", "display", "flex-direction",
    "gap", "width", "max-width", "line-height",
]

CSS_SANITIZER = CSSSanitizer(allowed_css_properties=ALLOWED_STYLES)


def sanitize_html(html_content: str) -> str:
    """Strip executable HTML. Pair this with a sandboxed iframe in the viewer."""
    cleaned = bleach.clean(
        html_content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=["http", "https", "mailto"],
        css_sanitizer=CSS_SANITIZER,
        strip=True,
    )
    cleaned = re.sub(r"@import[^;]*;?", "", cleaned, flags=re.I)
    cleaned = re.sub(r"expression\s*\(", "", cleaned, flags=re.I)
    cleaned = re.sub(r"url\s*\(\s*['\"]?\s*javascript:", "", cleaned, flags=re.I)
    cleaned = re.sub(r"on\w+\s*=", "", cleaned, flags=re.I)
    return cleaned
