from bookstoscrap.book import get_details
from bookstoscrap.category import get_books_url
import csv
from progress.spinner import MoonSpinner


books_urls = get_books_url(
    "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html")

# Create a csv file
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

file_csv = open("data.csv", "w")
writer = csv.writer(file_csv, delimiter=",")
writer.writerow(headers)

with MoonSpinner('Processing...') as spinner:
    for url in books_urls:
        details = get_details(url)
        writer.writerow(details)
        spinner.next()

file_csv.close()
