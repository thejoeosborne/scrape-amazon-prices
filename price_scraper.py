from bs4 import BeautifulSoup
from curl_cffi import requests


async def price_scraper(url: str):

    # Create a session, send a request, and soupify the HTML
    session = requests.AsyncSession()
    res = await session.get(url, impersonate="chrome")
    soup = BeautifulSoup(res.text, "html.parser")

    # Grab the product title and price
    product_title = soup.select_one("span#productTitle").text.strip()
    product_price_whole = soup.select_one("div#corePriceDisplay_desktop_feature_div span.a-price-whole").text.strip()
    product_price_fraction = soup.select_one("span.a-price-fraction").text.strip()

    # Remove any commas from the whole part of the price
    product_price_whole = product_price_whole.replace(",", "")

    # Combine the dollars and cents to form the full price
    product_price = float(product_price_whole + product_price_fraction)

    data = {
        "title": product_title,
        "price": product_price,
        "url": url
    }

    return data


if __name__ == "__main__":
    import asyncio
    import json

    url = "https://www.amazon.com/dp/B0DLHMYX53"
    product_data = asyncio.run(price_scraper(url))
    print(json.dumps(product_data, indent=2))
