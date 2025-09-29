import re

from bs4 import BeautifulSoup
from curl_cffi import requests


async def url_scraper(search_query: str, max_pages: int = None) -> list[str]:

    # Send a request with a search query and soupify the HTML
    params = {
        "k": search_query
    }
    base_url = "https://www.amazon.com/s"
    session = requests.AsyncSession()
    res = await session.get(base_url, params=params, impersonate="chrome")
    soup = BeautifulSoup(res.text, "html.parser")

    # Use regex to find {"totalResultCount":\d+}
    num_results = re.search(r'"totalResultCount":(\d+)', res.text).group(1)
    if not num_results:
        raise ValueError("No results found for the brand search.")
    num_results = int(num_results)

    print(f"Found {num_results} results for query: {search_query}")

    # Find the ASINs and create the product URLs
    items = soup.select('div[role="listitem"][data-component-type="s-search-result"]')
    amazon_product_url = "https://www.amazon.com/dp/"
    product_urls = list(set([amazon_product_url + x.get("data-asin") for x in items]))

    print(f"Found {len(product_urls)} product URLs on the first page")

    # Calculate the number of pages in order to paginate and collect more URLs
    num_per_page = len(product_urls)
    num_pages = (num_results // num_per_page) + (
        1 if num_results % num_per_page > 0 else 0
    )

    # Paginate and repeat the process for each page
    for page in range(2, num_pages + 1):
        print(f"Fetching page {page} of {num_pages}")
        params["page"] = page
        res = await session.get(base_url, params=params, impersonate="chrome")
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(
            'div[role="listitem"][data-component-type="s-search-result"]'
        )
        product_urls.extend(
            list(set([amazon_product_url + x.get("data-asin") for x in items]))
        )

        # If you only want to scrape a certain number of pages, pass in max_pages
        if max_pages and page >= max_pages:
            break

    all_product_urls = list(set(product_urls))
    return all_product_urls


if __name__ == "__main__":
    import asyncio

    query = "2024 macbook pro m4 max 16 inch"
    results = asyncio.run(url_scraper(query))
    print(f"Found {len(results)} links for query: {query}")
