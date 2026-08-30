"""Reusable visual styles for TivelWeb sites."""

STYLE_PRESETS = {
    "ocean": {"primary": "#087ea4", "accent": "#22d3ee", "surface": "#ecfeff", "ink": "#123044"},
    "sunset": {"primary": "#ea580c", "accent": "#fbbf24", "surface": "#fff7ed", "ink": "#431407"},
    "forest": {"primary": "#16803b", "accent": "#84cc16", "surface": "#f0fdf4", "ink": "#14331f"},
    "midnight": {"primary": "#6857e5", "accent": "#22d3ee", "surface": "#f5f3ff", "ink": "#17152d"},
    "rose": {"primary": "#db2777", "accent": "#fb7185", "surface": "#fff1f2", "ink": "#4c152d"},
}


def theme_color(name: str = "midnight") -> str:
    """Return the primary color of a named style preset."""
    try:
        return STYLE_PRESETS[name]["primary"]
    except KeyError as error:
        choices = ", ".join(sorted(STYLE_PRESETS))
        raise ValueError(f"Unknown style {name!r}. Choose from: {choices}") from error


def style_preset(name: str = "midnight") -> str:
    """Return an embeddable style block for cards, grids, labels and callouts."""
    try:
        colors = STYLE_PRESETS[name]
    except KeyError as error:
        choices = ", ".join(sorted(STYLE_PRESETS))
        raise ValueError(f"Unknown style {name!r}. Choose from: {choices}") from error
    return f"""
<style>
:root{{--preset-primary:{colors['primary']};--preset-accent:{colors['accent']};--preset-surface:{colors['surface']};--preset-ink:{colors['ink']}}}
.feature-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1.25rem}}
.feature-card{{background:#fff;border:1px solid color-mix(in srgb,var(--preset-primary) 16%,white);border-radius:18px;padding:1.5rem;box-shadow:0 14px 35px #11182712}}
.feature-card h3{{color:var(--preset-ink);margin:.5rem 0}}.feature-card a{{color:var(--preset-primary);font-weight:800;text-decoration:none}}
.eyebrow{{color:var(--preset-primary);font-size:.78rem;font-weight:900;letter-spacing:.12em;text-transform:uppercase}}
.callout{{background:var(--preset-surface);border-left:5px solid var(--preset-primary);padding:1.2rem 1.4rem;border-radius:0 14px 14px 0}}
.stat{{font-size:2rem;font-weight:900;color:var(--preset-primary)}}
</style>"""

