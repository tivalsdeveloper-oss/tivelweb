from tivelweb import create_blog_site, create_business_site, create_portfolio_site

create_portfolio_site(name="Tivalsdeveloper", output="portfolio", style="midnight")
create_business_site(name="Tivals Digital", output="business", style="ocean")
create_blog_site(name="Tivals Blog", author="Lufuno", output="blog", style="rose")

print("Created portfolio, business and blog websites.")
