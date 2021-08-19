import sys
import requests
from bs4 import BeautifulSoup


class Category:

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.books = None

    def __repr__(self):
        return f'{self.name}: {self.url}'


class Fetch:
    @staticmethod
    def soup(url):
        try:
            response = requests.get(url)
        except:
            print("Error: Fetch.soup(url)")
            sys.exit(1)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    @staticmethod
    def urlcat(base, chunk):
        for str in chunk.split('/'):
            if str != "..":
                base += ('/' + str)
        return base

    @staticmethod
    def urlnext(base, chunk):
        next_url = ""
        for str in base.split('/'):
            if ".html" not in str:
                next_url += (str + '/')
        next_url += chunk
        return next_url

    @classmethod
    def extract_urls(cls, soup):
        urls = []
        article_list = soup.find_all("article", class_="product_pod")
        for article in article_list:
            href = article.find("h3").a['href']
            url = cls.urlcat("http://books.toscrape.com/catalogue", href)
            urls.append(url)
        return urls

    @classmethod
    def books(cls, url):
        books = []
        while True:
            soup = cls.soup(url)
            books += cls.extract_urls(soup)
            li = soup.find('li', class_="next")
            if li is not None:
                url = cls.urlnext(url, li.a['href'])
            else:
                break
        return books

    @classmethod
    def categories(cls, url):
        categories = []
        soup = cls.soup(url)
        nav = soup.find("ul", class_="nav")
        elements = nav.find_all("a")

        for a in elements:
            for str in a.stripped_strings:
                if str != 'Books':
                    category = Category(str, cls.urlcat(url, a['href']))
                    category.books = cls.books(category.url)
                    categories.append(category)

        return categories
