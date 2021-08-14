from bookstoscrap.book import get_details
from bookstoscrap.category import get_categories, get_books_url
import csv
import sys
from progress.spinner import MoonSpinner
from bcolors.colors import Color


def create_csv(category_url, category):
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

    print("> Fetching data from " + category_url)
    books_urls = get_books_url(category_url)
    file_csv = open(category + ".csv", "w")
    writer = csv.writer(file_csv, delimiter=",")
    writer.writerow(headers)

    with MoonSpinner('Processing...') as spinner:
        for url in books_urls:
            details = get_details(url)
            writer.writerow(details)
            spinner.next()
    file_csv.close()

    print("[" + Color.OKGREEN + "OK" + Color.ENDC + "] " + category + ".csv")


def main(argv):
    if len(argv) == 3 and argv[1] == "--single-product":
        create_csv("data.csv", argv[2])
        return

    elif len(argv) == 3 and argv[1] == "--category":
        categories = get_categories('http://books.toscrape.com')
        for category in categories:
            if category == argv[2].capitalize():
                create_csv(categories[category], category)
                return
        print(Color.FAIL + "Error: category doesn't exist" + Color.ENDC)

    elif len(argv) == 2 and argv[1] == "--all":
        print(
            Color.WARNING +
            "Warning: this operaton will take some time. Please grab a coffee !"
            + Color.ENDC)
        categories = get_categories('http://books.toscrape.com')
        for category in categories:
            if category != 'Books':
                create_csv(categories[category], category)
                return

    else:
        print("Usage: python main.py [OPTIONS]")
        print(
            "OPTIONS: --all, --save-images, --single-product [URL], --category [CATEGORY]")


if __name__ == "__main__":
    main(sys.argv)
