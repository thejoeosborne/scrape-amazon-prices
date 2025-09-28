from bs4 import BeautifulSoup
from curl_cffi import requests

from regex_utility import regex_find


async def collect_urls_by_search_query(search_query: str):
    params = {
        "k": search_query
    }
    base_url = "https://www.amazon.com/s"

    session = requests.AsyncSession()

    res = await session.get(base_url, params=params, impersonate="chrome")

    soup = BeautifulSoup(res.text, "html.parser")

    # use regex to find {"totalResultCount":\d+}
    num_results = regex_find(r'"totalResultCount":(\d+)', res.text)
    if not num_results:
        raise ValueError("No results found for the brand search.")
    num_results = int(num_results)

    items = soup.select('div[role="listitem"][data-component-type="s-search-result"]')
    amazon_product_url = "https://www.amazon.com/dp/"
    links = list(set([amazon_product_url + x.get("data-asin") for x in items]))

    num_per_page = len(links)

    num_pages = (num_results // num_per_page) + (
        1 if num_results % num_per_page > 0 else 0
    )

    # Paginate through the results
    for page in range(2, num_pages + 1):
        print(f"Fetching page {page} of {num_pages} for query: {query}")
        params["page"] = page
        res = await session.get(base_url, params=params, impersonate="chrome")
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(
            'div[role="listitem"][data-component-type="s-search-result"]'
        )
        links.extend(
            list(set([amazon_product_url + x.get("data-asin") for x in items]))
        )
        break

    all_links = list(set(links))
    return all_links


if __name__ == "__main__":
    import asyncio

    query = "phone case iphone 17 pro"
    results = asyncio.run(collect_urls_by_search_query(query))
    print(f"Found {len(results)} links for query: {query}")
