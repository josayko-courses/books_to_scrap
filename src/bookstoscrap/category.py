import requests
from bs4 import BeautifulSoup
from .utils import urlcat


def extract_urls(page_url):
    response = requests.get(page_url)
    if (response.ok):
        soup = BeautifulSoup(response.content, "html.parser")
        books_url = []

        article_list = soup.find_all("article", class_="product_pod")
        for article in article_list:
            href = article.find("h3").a['href']
            url = urlcat("http://books.toscrape.com/catalogue", href)
            books_url.append(url)
    return books_url
