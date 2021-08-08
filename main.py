import requests
from bs4 import BeautifulSoup

home_url = "http://books.toscrape.com/"
res = requests.get(home_url)

html_page = BeautifulSoup(res.content, "html.parser")
print(html_page)
