import requests
from bs4 import BeautifulSoup
from .urlcat import urlcat
from bcolors.colors import Color


def urlnext(base, chunk):
    next_url = ""
    for str in base.split('/'):
        if ".html" not in str:
            next_url += (str + '/')
    next_url += chunk
    return next_url


def extract_urls(soup):
    urls = []

    article_list = soup.find_all("article", class_="product_pod")
    for article in article_list:
        href = article.find("h3").a['href']
        url = urlcat("http://books.toscrape.com/catalogue", href)
        urls.append(url)
    return urls


def get_books_url(page_url):
    books_urls = []

    while True:
        response = requests.get(page_url)
        if (response.ok):
            soup = BeautifulSoup(response.content, "html.parser")
            books_urls += extract_urls(soup)
            li = soup.find('li', class_="next")
            if li is not None:
                page_url = urlnext(page_url, li.a['href'])
            else:
                break
        else:
            print("Error: cannot get data from url")
            break
    return books_urls


def get_categories(url):
    categories = {}

    try:
        response = requests.get(url)
    except:
        print(Color.FAIL + "Error: cannot fetch data from url" + Color.ENDC)
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    nav = soup.find("ul", class_="nav")
    taglist = nav.find_all("a")

    for tag in taglist:
        for str in tag.stripped_strings:
            categories[str] = urlcat(url, tag['href'])

    return categories
