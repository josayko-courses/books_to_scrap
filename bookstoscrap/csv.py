import csv
import os
from progress.spinner import MoonSpinner
from bcolors.colors import Color
from bookstoscrap.book import get_details


def create_csv(books_urls, category):
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

    path = os.getcwd()
    if os.path.isdir(path + '/data') == False:
        os.mkdir(path + '/data')

        # Write description headers
    file_csv = open('data/' + category + ".csv", "w")
    writer = csv.writer(file_csv, delimiter=",")
    writer.writerow(headers)

    # Get and write each book details
    with MoonSpinner('Processing...') as spinner:
        for url in books_urls:
            details = get_details(url)
            spinner.next()
            if details != None:
                writer.writerow(details)

    file_csv.close()
    print("[" + Color.OKGREEN + "OK" + Color.ENDC + "] " + category + ".csv")


def fetch_data(books_urls, filename):
    try:
        create_csv(books_urls, filename)
        return True
    except:
        print(Color.FAIL + "Error: cannot fetch data from url" + Color.ENDC)
    return False
