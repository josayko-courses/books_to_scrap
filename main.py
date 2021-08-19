from bookstoscrap.fetch import Fetch, Book
from bcolors.colors import Color
import sys


def main(argv):
    if len(argv) >= 3 and argv[1] == "bookurl":
        book = list([Book(argv[2])])
    elif len(argv) >= 3 and argv[1] == "category":
        data = Fetch.categories('http://books.toscrape.com', argv[2])
        if not data:
            print(Color.FAIL + "Error: category doesn't exist" + Color.ENDC)
            sys.exit(1)
    elif len(argv) >= 2 and argv[1] == "getall":
        data = Fetch.categories('http://books.toscrape.com')
    else:
        print(Color.HEADER + "Usage: python main.py [OPTIONS]")
        print(
            "OPTIONS: getall, --save-img, bookurl [URL], category [CATEGORY]" +
            Color.ENDC)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
