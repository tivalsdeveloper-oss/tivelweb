"""Safe, reusable HTML components."""

from html import escape


def _text(value: object) -> str:
    return escape(str(value), quote=True)


def button(label: str, href: str = "#", style: str = "primary") -> str:
    return f'<a class="btn btn-{_text(style)}" href="{_text(href)}">{_text(label)}</a>'


def image(src: str, alt: str = "", class_name: str = "") -> str:
    return f'<img src="{_text(src)}" alt="{_text(alt)}" class="{_text(class_name)}" loading="lazy">'


def hero(title: str, subtitle: str = "", action: str = "", action_url: str = "#") -> str:
    action_html = button(action, action_url) if action else ""
    return (
        '<section class="hero"><div class="container">'
        f'<h1>{_text(title)}</h1><p>{_text(subtitle)}</p>{action_html}'
        '</div></section>'
    )


def section(title: str, content: str, *, raw: bool = False) -> str:
    body = content if raw else f"<p>{_text(content)}</p>"
    return f'<section class="section"><div class="container"><h2>{_text(title)}</h2>{body}</div></section>'


def card(title: str, content: str, link: str = "", link_text: str = "Learn more") -> str:
    link_html = button(link_text, link, "secondary") if link else ""
    return f'<article class="card"><h3>{_text(title)}</h3><p>{_text(content)}</p>{link_html}</article>'

