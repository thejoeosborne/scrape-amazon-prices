from bs4 import BeautifulSoup
from curl_cffi import requests


async def collect_prices_by_url(url: str):
    session = requests.AsyncSession()
    res = await session.get(url, impersonate="chrome")
    soup = BeautifulSoup(res.text, "html.parser")

    product_title = soup.select_one("span#productTitle").text.strip()
    product_price_whole = soup.select_one("div#corePriceDisplay_desktop_feature_div span.a-price-whole").text.strip()
    product_price_fraction = soup.select_one("span.a-price-fraction").text.strip()

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

    url = "https://www.amazon.com/dp/B0FFGW3481"
    product_data = asyncio.run(collect_prices_by_url(url))
    print(json.dumps(product_data, indent=2))
