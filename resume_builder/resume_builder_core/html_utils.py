import markdown
import bleach


EXTRA_TAGS = {"p", "pre", "span", "h1", "h2", "h3", "h4", "h5", "h6", "code"}
ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS.union(EXTRA_TAGS)
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "img": ["src", "alt", "title"],
    "span": ["class"],
    "code": ["class"],
    "pre": ["class"],
}


def render_markdown(raw_text):
    html = markdown.markdown(
        raw_text,
        extensions=["fenced_code", "codehilite"],  # Highlighting enabled
    )
    clean_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    return bleach.linkify(clean_html)
