import sys
import requests
from bs4 import BeautifulSoup


class Book:
    def __init__(self, url):
        self.details = {}
        self.details['url'] = url

    def __repr__(self):
        return repr(self.details)


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
    def next_page(base, chunk):
        url = ""
        for str in base.split('/'):
            if ".html" not in str:
                url += (str + '/')
        url += chunk
        return url

    @classmethod
    def books_from_page(cls, soup):
        books = []
        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            href = article.find("h3").a['href']
            book = Book(cls.urlcat(
                "http://books.toscrape.com/catalogue", href))
            books.append(book)
        return books

    @classmethod
    def books_from_category(cls, url):
        books = []
        while True:
            soup = cls.soup(url)
            books += cls.books_from_page(soup)
            li = soup.find('li', class_="next")
            if li is not None:
                url = cls.next_page(url, li.a['href'])
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
                    category.books = cls.books_from_category(category.url)
                    categories.append(category)

        return categories
