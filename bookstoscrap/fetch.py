"""Extract and transform data from url 

Fetch methods extracts urls and create a Category.
Each instance of Book tranform data from book url.
Book instances are stored in respective Category.
"""

from bcolors.colors import Color
from bs4 import BeautifulSoup
import requests
import sys
import re


class Book:
    """Create a Book to store details from url"""
    def __init__(self, url):
        soup = Fetch.soup(url)
        self.details = {}

        # Get the product url
        self.details['url'] = url

        # Get title
        title_tag = soup.find("h1")
        self.details['title'] = title_tag.string

        # Get product description
        meta_desc = soup.find("meta", {"name": "description"})
        self.details['product_description'] = meta_desc['content'].strip()

        # Get product category
        breadcrumb = soup.find("li", class_="active")
        link = breadcrumb.find_previous_sibling("li")
        category = link.find("a").string
        self.details['category'] = category

        # Get review rating
        p = soup.find("p", class_="star-rating")
        ratings = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five']
        for index, rating in enumerate(ratings):
            if rating == p['class'][1]:
                self.details['review_rating'] = index

        # Get the image url
        img_tag = soup.find("img", alt=self.details['title'])
        link_str = img_tag['src']
        link_url = Fetch.urlcat("http://books.toscrape.com", link_str)
        self.details['image_url'] = link_url

        # Get upc, prices and availability
        tds = soup.find_all("td")
        for index, td in enumerate(tds):
            if (index == 0):
                self.details['upc'] = td.string
            elif (index == 2):
                number = re.findall(r'[\d\.\d+]', td.string)
                self.details['price_including_tax'] = float(''.join(number))
            elif (index == 3):
                number = re.findall(r'[\d\.\d+]', td.string)
                self.details['price_excluding_tax'] = float(''.join(number))
            elif (index == 5):
                number = re.findall(r'[\d\.\d+]', td.string)
                self.details['number_available'] = int(''.join(number))

    def __repr__(self):
        return repr(self.details)


class Category:
    """Create a category to store a list of Book"""
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.books = None

    def __repr__(self):
        return f'{self.name}: {self.url}'


class Fetch:
    """Useful methods for fetching data from url"""
    @staticmethod
    def soup(url):
        """Returns html code source as a BeautifulSoup instance"""
        try:
            response = requests.get(url)
        except:
            print(f'{Color.WARNING}Error: Fetch.soup(url){Color.ENDC}')
            sys.exit(1)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    @staticmethod
    def urlcat(base, chunk):
        """Concatenate base and relatvive url to get absolut url"""
        for str in chunk.split('/'):
            if str != "..":
                base += ('/' + str)
        return base

    @staticmethod
    def next_page(base, chunk):
        """Returns next pasge url or empty string"""
        url = ""
        for str in base.split('/'):
            if ".html" not in str:
                url += (str + '/')
        url += chunk
        return url

    @classmethod
    def books_from_page(cls, soup):
        """Extract all books url from page"""
        books = []
        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            href = article.find("h3").a['href']
            book = Book(cls.urlcat(
                "http://books.toscrape.com/catalogue", href))
            books.append(book)
        return books

    @classmethod
    def books_from_category(cls, name, url):
        """Create Book instance for each book url"""
        books = []

        print(f'Processing {name} books...')
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
    def categories(cls, url, filter=None):
        """Extract categories url and returns a list of Category"""
        categories = []
        soup = cls.soup(url)
        nav = soup.find("ul", class_="nav")
        elements = nav.find_all("a")

        for a in elements:
            for str in a.stripped_strings:
                if str != 'Books':
                    if (filter and filter == str) or filter == None:
                        category = Category(str, cls.urlcat(url, a['href']))
                        category.books = cls.books_from_category(
                            category.name, category.url)
                        categories.append(category)
                        print(
                            f'    [{Color.OKGREEN}OK{Color.ENDC}] {category.name} books details')

        return categories
