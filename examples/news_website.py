from tivelweb import create_news_site

site = create_news_site(
    name="Tivals News",
    output="news_website",
    theme_color="#d71920",
)

print(f"News website created at: {site.output.resolve()}")

