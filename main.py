from typing import cast
import requests
from bs4 import BeautifulSoup
import csv

product_url = "http://books.toscrape.com/catalogue/soumission_998/index.html"

headers = [
    "product_page_url",
    "upc",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"
]

product_details = [''] * 10

# Get the html page source code
response = requests.get(product_url)
soup = BeautifulSoup(response.content, "html.parser")

# Get the product url
product_details[0] = product_url

# Get title
title_tag = soup.find("h1")
product_details[2] = title_tag.string

# Get product description
desc_title = soup.find("div", id="product_description")
desc_content = desc_title.find_next_sibling("p").string
product_details[6] = desc_content

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
link_url = "http://books.toscrape.com"

for str in link_str.split('/'):
    if str != "..":
        link_url += ('/' + str)

product_details[9] = link_url


# Get other details
tds = soup.find_all("td")
for index, td in enumerate(tds):
    if (index == 0):
        product_details[1] = td.string
    elif (index == 2):
        product_details[3] = td.string
    elif (index == 3):
        product_details[4] = td.string
    elif (index == 5):
        product_details[5] = td.string

# Log
print(product_details)

# Create a csv file
with open("data.csv", "w") as file_csv:
    writer = csv.writer(file_csv, delimiter=",")
    writer.writerow(headers)
    writer.writerow(product_details)
