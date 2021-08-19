import requests
from bs4 import BeautifulSoup


class Category:
    books = []

    def __init__(self, name, url):
        self.name = name
        self.url = url


class Fetch:
    def soup(url):
        try:
            response = requests.get(url)
        except:
            print("Error")
            return None
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def urlcat(base, chunk):
        for str in chunk.split('/'):
            if str != "..":
                base += ('/' + str)
        return base

    @classmethod
    def categories(cls, url):
        categories = []
        soup = cls.soup(url)
        if soup:
            nav = soup.find("ul", class_="nav")
            elements = nav.find_all("a")

        for a in elements:
            for str in a.stripped_strings:
                if str != 'Books':
                    categories.append(
                        Category(str, cls.urlcat(url, a['href'])))

        return categories
