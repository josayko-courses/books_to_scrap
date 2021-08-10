from bookstoscrap import book
import csv

product_url = "http://books.toscrape.com/catalogue/soumission_998/index.html"

details = book.get_details(product_url)

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

# Create a csv file
with open("data.csv", "w") as file_csv:
    writer = csv.writer(file_csv, delimiter=",")
    writer.writerow(headers)
    writer.writerow(details)
