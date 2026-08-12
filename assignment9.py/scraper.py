
import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"


def get_books():
    """
    Scrapes book titles and prices from books.toscrape.com.

    Returns:
        list[dict]: A list of dictionaries like
                     [{"title": "A Light in the Attic", "price": "£51.77"}, ...]
    """
    books = []

    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()  # raise an error if the request failed
    except requests.RequestException as e:
        print(f"Error fetching {URL}: {e}")
        return books  # return an empty list if scraping fails

    soup = BeautifulSoup(response.text, "html.parser")

    # Each book is inside an <article class="product_pod"> element
    all_books = soup.find_all("article", class_="product_pod")

    for book in all_books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        books.append({"title": title, "price": price})

    return books


# Quick manual test: run "python scraper.py" directly to check it works
if __name__ == "__main__":
    results = get_books()
    print(f"Scraped {len(results)} books.\n")
    for b in results[:5]:
        print(f"{b['title']} — {b['price']}")