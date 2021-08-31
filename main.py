"""CLI program for web scrapping

Get books data from http://books.toscrape.com
"""

from bookstoscrap.csv import save_data
from bookstoscrap.fetch import Fetch, Category, Book
from bcolors.colors import Color
import sys


def main(argv):
    """Main program with 3 options: getall, bookurl and category"""

    if len(argv) >= 3 and argv[1] == "bookurl":
        book = list([Book(argv[2])])
        category = Category('Book', argv[2])
        category.books = book
        data = list([category])
        save_data(data, argv)

    elif len(argv) >= 3 and argv[1] == "category":
        data = Fetch.categories(
            'http://books.toscrape.com', argv[2].capitalize())
        if not data:
            print(Color.FAIL + "Error: category doesn't exist" + Color.ENDC)
            sys.exit(1)
        save_data(data, argv)

    elif len(argv) >= 2 and argv[1] == "getall":
        data = Fetch.categories('http://books.toscrape.com')
        save_data(data, argv)

    else:
        print(Color.HEADER + "Usage: python main.py [OPTIONS]")
        print(
            "OPTIONS: getall, --save-img, bookurl [URL], category [CATEGORY]" +
            Color.ENDC)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
