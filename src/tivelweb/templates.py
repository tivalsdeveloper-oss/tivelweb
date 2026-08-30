"""Ready-to-use website templates."""

from html import escape

from .components import hero, section
from .site import Site
from .styles import style_preset, theme_color


def _finish(site: Site, serve: bool, port: int) -> Site:
    if serve:
        site.run(port=port)
    else:
        site.build()
    return site


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
    background_image: str = "",
    serve: bool = False,
    port: int = 8000,
) -> Site:
    """Create and build a responsive demonstration news website."""
    site = Site(name, theme_color=theme_color, output=output, background_image=background_image)
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
    return _finish(site, serve, port)


def create_portfolio_site(
    name: str = "Your Name",
    tagline: str = "Python developer and creative problem solver.",
    output: str = "portfolio_website",
    style: str = "midnight",
    background_image: str = "",
    serve: bool = False,
    port: int = 8000,
) -> Site:
    """Create a polished four-page developer portfolio."""
    site = Site(name, theme_color=theme_color(style), output=output, background_image=background_image)
    home = site.page("Home", "index.html", tagline)
    home.add(style_preset(style))
    home.add(hero(name, tagline, "View projects", "projects.html"))
    features = (
        '<div class="feature-grid">'
        '<article class="feature-card"><span class="eyebrow">Python</span><h3>Useful libraries</h3><p>Create packages that solve real problems.</p></article>'
        '<article class="feature-card"><span class="eyebrow">Web</span><h3>Responsive websites</h3><p>Build fast sites that work across devices.</p></article>'
        '<article class="feature-card"><span class="eyebrow">AI</span><h3>Smart tools</h3><p>Experiment with practical local AI projects.</p></article>'
        '</div>'
    )
    home.add(section("What I build", features, raw=True))
    projects = site.page("Projects", "projects.html")
    projects.add(style_preset(style))
    projects.add(hero("Selected Projects", "A few things I have created."))
    projects.add(section("Projects", features, raw=True))
    site.page("About", "about.html").add(section("About Me", tagline))
    site.page("Contact", "contact.html").add(section("Contact", "Add your email and social links here."))
    return _finish(site, serve, port)


def create_business_site(
    name: str = "Your Business",
    description: str = "Reliable services for growing teams.",
    output: str = "business_website",
    style: str = "ocean",
    background_image: str = "",
    serve: bool = False,
    port: int = 8000,
) -> Site:
    """Create a professional small-business website."""
    site = Site(name, theme_color=theme_color(style), output=output, background_image=background_image)
    home = site.page("Home", "index.html", description)
    home.add(style_preset(style))
    home.add(hero(name, description, "Our services", "services.html"))
    services_html = (
        '<div class="feature-grid">'
        '<article class="feature-card"><span class="eyebrow">Plan</span><h3>Consulting</h3><p>Clear guidance shaped around your goals.</p></article>'
        '<article class="feature-card"><span class="eyebrow">Build</span><h3>Implementation</h3><p>Practical delivery from idea to launch.</p></article>'
        '<article class="feature-card"><span class="eyebrow">Grow</span><h3>Support</h3><p>Ongoing help as your business develops.</p></article>'
        '</div>'
    )
    home.add(section("Built for your next step", services_html, raw=True))
    services = site.page("Services", "services.html")
    services.add(style_preset(style))
    services.add(hero("Our Services", "Flexible support for your business."))
    services.add(section("What we offer", services_html, raw=True))
    site.page("About", "about.html").add(section("About", description))
    site.page("Contact", "contact.html").add(section("Start a conversation", "Add your contact details here."))
    return _finish(site, serve, port)


def create_blog_site(
    name: str = "My Blog",
    author: str = "Your Name",
    output: str = "blog_website",
    style: str = "rose",
    background_image: str = "",
    serve: bool = False,
    port: int = 8000,
) -> Site:
    """Create a blog homepage with three editable sample articles."""
    site = Site(name, theme_color=theme_color(style), output=output, background_image=background_image)
    home = site.page("Home", "index.html", f"Articles and ideas by {author}.")
    home.add(style_preset(style))
    home.add(hero(name, f"Articles and ideas by {author}."))
    posts = [
        ("Starting my creative journey", "What I learned by beginning before I felt ready."),
        ("How I organize a Python project", "A simple structure that keeps projects understandable."),
        ("Lessons from building in public", "Why sharing progress can accelerate learning."),
    ]
    cards = []
    for number, (title, summary) in enumerate(posts, 1):
        path = f"post-{number}.html"
        cards.append(
            f'<article class="feature-card"><span class="eyebrow">Article {number}</span>'
            f'<h3>{escape(title)}</h3><p>{escape(summary)}</p><a href="{path}">Read article →</a></article>'
        )
        post = site.page(f"Article {number}", path, summary)
        post.add(style_preset(style))
        post.add(hero(title, f"By {author}"))
        post.add(section(title, summary + " Replace this text with your complete article."))
    home.add(section("Latest writing", '<div class="feature-grid">' + "".join(cards) + "</div>", raw=True))
    site.page("About", "about.html").add(section("About the author", f"This blog is written by {author}."))
    return _finish(site, serve, port)
