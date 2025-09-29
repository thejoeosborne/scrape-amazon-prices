import asyncio

from price_scraper import price_scraper
from url_scraper import url_scraper


async def orchestrator(search_query: str, max_pages: int = None) -> list[dict]:

    # Step 1: Scrape product URLs based on the search query
    product_urls = await url_scraper(search_query, max_pages)

    print(f"Total product URLs found: {len(product_urls)}")

    # Step 2: For each product URL, scrape the price and other details
    tasks = [price_scraper(url) for url in product_urls]
    product_data = await asyncio.gather(*tasks, return_exceptions=True)

    return product_data


if __name__ == "__main__":

    search_query = "2024 macbook pro m4 max 16 inch"
    max_pages = 2  # Limit to first 2 pages for testing

    products_data = asyncio.run(orchestrator(search_query, max_pages))
    print(f"Scraped data for {len(products_data)} products")
