import requests
from bs4 import BeautifulSoup

home_url = "http://books.toscrape.com/"

product_url = "http://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html"

headers = ["product_page_url",
           "upc",
           "title",
           "price_including_tax",
           "price_excluding_tax",
           "number_available",
           "product_description",
           "category",
           "review_rating",
           "image_url"]


def get_html_page(url):
    """
    Return html page as an object from url
    """
    res = requests.get(url)
    html_page = BeautifulSoup(res.content, "html.parser")
    return html_page


data = get_html_page(product_url)
print(data)
