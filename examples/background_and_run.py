from tivelweb import create_portfolio_site

# Running this file builds the site, starts the server and opens the browser.
create_portfolio_site(
    name="Tivalsdeveloper",
    tagline="Building websites, libraries and AI tools.",
    style="midnight",
    background_image=(
        "https://images.unsplash.com/photo-1518770660439-4636190af475"
        "?auto=format&fit=crop&w=1600&q=85"
    ),
    serve=True,
)
