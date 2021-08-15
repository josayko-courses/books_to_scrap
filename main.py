from bookstoscrap.book import get_details
from bookstoscrap.category import get_categories, get_books_url
from progress.spinner import MoonSpinner
from bcolors.colors import Color
import csv
import sys


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


def fetch_data(url, filename):
    try:
        create_csv(url, filename)
        return True
    except:
        print(Color.FAIL + "Error fetching data from url" + Color.ENDC)
    return False


def main(argv):
    if len(argv) == 3 and argv[1] == "--book":
        if fetch_data(argv[2], "book") == True:
            return

    elif len(argv) == 3 and argv[1] == "--category":
        categories = get_categories('http://books.toscrape.com')
        for category in categories:
            if category == argv[2].capitalize():
                if fetch_data(categories[category], category) == True:
                    return
        print(Color.FAIL + "Error: category doesn't exist" + Color.ENDC)

    elif len(argv) == 2 and argv[1] == "--all":
        print(
            Color.WARNING +
            "Warning: this operaton will take some time. Please wait..."
            + Color.ENDC)
        categories = get_categories('http://books.toscrape.com')
        for category in categories:
            if category != 'Books':
                if fetch_data(categories[category], category) == False:
                    return
        return

    else:
        print(Color.HEADER + "Usage: python main.py [OPTIONS]")
        print(
            "OPTIONS: --all, --save-images, --book [URL], --category [CATEGORY]" + Color.ENDC)


if __name__ == "__main__":
    main(sys.argv)
