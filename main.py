from bookstoscrap.category import get_categories, get_books_url
from bcolors.colors import Color
from bookstoscrap.csv import fetch_data
import sys


def main(argv):
    if len(argv) == 3 and argv[1] == "bookurl":
        book_url = [argv[2]]
        if fetch_data(book_url, "book") == True:
            return

    elif len(argv) == 3 and argv[1] == "category":
        categories = get_categories('http://books.toscrape.com')
        if categories == None:
            return
        for category in categories:
            if category == argv[2].capitalize():
                books_urls = get_books_url(categories[category])
                if fetch_data(books_urls, category) == True:
                    return
        print(Color.FAIL + "Error: category doesn't exist" + Color.ENDC)

    elif len(argv) == 2 and argv[1] == "getall":
        categories = get_categories('http://books.toscrape.com')
        if categories == None:
            return
        print(
            Color.WARNING +
            "Warning: this operaton will take some time. Please wait..."
            + Color.ENDC)
        for category in categories:
            if category != 'Books':
                books_urls = get_books_url(categories[category])
                if fetch_data(books_urls, category) == False:
                    return
    else:
        print(Color.HEADER + "Usage: python main.py [OPTIONS]")
        print(
            "OPTIONS: getall, --save-images, bookurl [URL], category [CATEGORY]" + Color.ENDC)


if __name__ == "__main__":
    main(sys.argv)
