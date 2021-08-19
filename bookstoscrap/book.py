import requests
import re
from bs4 import BeautifulSoup
from .fetch import Fetch
from bcolors.colors import Color


class Book:
    details = {}

    def __init__(self, url):
        self.details['url'] = url


def get_details(product_url):
    """
    Param is and url of a single product\n
    Return is an array with the following details:\n
    [0]product_page_url\n 
    [1]upc\n 
    [2]title\n
    [3]price_including_tax\n
    [4]price_excluding_tax\n
    [5]number_available\n
    [6]product_description\n
    [7]category\n
    [8]review_rating\n
    [9]image_url\n
    """
    product_details = [''] * 10
    soup = Fetch.soup(product_url)

    if soup:
        # Get the product url
        product_details[0] = product_url

        # Get title
        title_tag = soup.find("h1")
        product_details[2] = title_tag.string

        # Get product description
        meta_desc = soup.find("meta", {"name": "description"})
        product_details[6] = meta_desc['content'].strip()

        # Get product category
        breadcrumb = soup.find("li", class_="active")
        link = breadcrumb.find_previous_sibling("li")
        category = link.find("a").string
        product_details[7] = category

        # Get review rating
        p = soup.find("p", class_="star-rating")
        rating = 0
        if p['class'][1] == 'One':
            rating = 1
        elif p['class'][1] == 'Two':
            rating = 2
        elif p['class'][1] == 'Three':
            rating = 3
        elif p['class'][1] == 'Four':
            rating = 4
        elif p['class'][1] == 'Five':
            rating = 5
        product_details[8] = rating

        # Get the image url
        img_tag = soup.find("img", alt=product_details[2])
        link_str = img_tag['src']
        link_url = Fetch.urlcat("http://books.toscrape.com", link_str)
        product_details[9] = link_url

        # Get upc, prices and availability
        tds = soup.find_all("td")
        for index, td in enumerate(tds):
            if (index == 0):
                product_details[1] = td.string
            elif (index == 2):
                number = re.findall(r'[\d\.\d+]', td.string)
                product_details[3] = float(''.join(number))
            elif (index == 3):
                number = re.findall(r'[\d\.\d+]', td.string)
                product_details[4] = float(''.join(number))
            elif (index == 5):
                number = re.findall(r'[\d\.\d+]', td.string)
                product_details[5] = int(''.join(number))
    else:
        print(Color.FAIL + "Error: cannot get data from url" + Color.ENDC)
        return None

    return product_details
