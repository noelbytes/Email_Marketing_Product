from __future__ import annotations


def render_html_document(*, html: str, css: str | None = None) -> str:
    """
    Ensure we send a single well-formed HTML document.

    GrapesJS may output fragments or include <body>/<html>. We avoid double-wrapping.
    """
    content = (html or "").strip()
    style = (css or "").strip()

    lower = content.lower()
    if "<html" in lower:
        return content

    head = "<head><meta charset=\"utf-8\"/>" + (f"<style>{style}</style>" if style else "") + "</head>"
    return f"<!doctype html><html>{head}<body>{content}</body></html>"

