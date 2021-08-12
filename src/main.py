from bookstoscrap.book import get_details
from bookstoscrap.category import get_categories, get_books_url
import csv
from progress.spinner import MoonSpinner

OKGREEN = '\033[92m'
ENDC = '\033[0m'

categories = get_categories('http://books.toscrape.com')

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

for category in categories:
    if category != 'Books':
        print("> Fetching data from " + categories[category])
        books_urls = get_books_url(categories[category])
        file_csv = open(category + ".csv", "w")
        writer = csv.writer(file_csv, delimiter=",")
        writer.writerow(headers)
        with MoonSpinner('Processing...') as spinner:
            for url in books_urls:
                details = get_details(url)
                writer.writerow(details)
                spinner.next()
        file_csv.close()
        print("[" + OKGREEN + "OK" + ENDC + "] " + category + ".csv")
