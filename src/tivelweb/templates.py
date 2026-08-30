"""Ready-to-use website templates."""

from .components import hero, section
from .site import Site


NEWS_STYLE = """
<style>
.breaking{background:#d71920;color:#fff;padding:12px 18px;border-radius:8px;font-weight:800}
.news-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:24px}
.news-card{overflow:hidden;background:#fff;border-radius:14px;box-shadow:0 10px 30px #00000018}
.news-card img{display:block;width:100%;height:210px;object-fit:cover}
.news-content{padding:20px}.category{color:#d71920;font-size:13px;font-weight:800;text-transform:uppercase}
.news-card h3{margin:8px 0;line-height:1.3}.news-card p{color:#555}
@media(max-width:850px){.news-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.news-grid{grid-template-columns:1fr}.news-card img{height:230px}}
</style>
"""


STORIES = [
    ("Technology", "Python helps developers build powerful tools",
     "Developers use Python for websites, artificial intelligence and automation.",
     "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=900&q=80"),
    ("Business", "Young developers build digital businesses",
     "Online tools make it easier to launch websites and technology products.",
     "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=900&q=80"),
    ("Sports", "Local athletes prepare for competition",
     "Athletes follow structured training programmes to reach their goals.",
     "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=900&q=80"),
    ("Education", "Students find new ways to learn programming",
     "Practical projects help students learn software development.",
     "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=900&q=80"),
    ("Community", "Technology creates community opportunities",
     "Digital projects improve access to information, education and skills.",
     "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?auto=format&fit=crop&w=900&q=80"),
    ("Science", "Computing helps researchers understand our world",
     "Computer models support research into weather, health and space.",
     "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=900&q=80"),
]


def create_news_site(
    name: str = "Tivals News",
    output: str = "news_website",
    theme_color: str = "#d71920",
) -> Site:
    """Create and build a responsive demonstration news website."""
    site = Site(name, theme_color=theme_color, output=output)
    home = site.page("Home", "index.html", "Technology, business, sports and community news.")
    home.add(NEWS_STYLE)
    home.add(hero(name, "Technology, business, sports and community stories.", "Latest news", "#latest"))

    cards = []
    for category, title, summary, image_url in STORIES:
        slug = category.lower()
        cards.append(
            f'<article class="news-card"><img src="{image_url}" alt="{category} story">'
            f'<div class="news-content"><span class="category">{category}</span>'
            f'<h3>{title}</h3><p>{summary}</p><a href="{slug}.html">Read article →</a></div></article>'
        )
        page = site.page(category, f"{slug}.html")
        page.add(hero(f"{category} News", title))
        page.add(section(title, summary))

    news = '<div id="latest" class="breaking">Welcome to the TivelWeb news template</div>'
    news += '<div class="news-grid">' + "".join(cards) + "</div>"
    home.add(section("Latest Stories", news, raw=True))
    site.build()
    return site

