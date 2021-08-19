from bcolors.colors import Color
import requests
import csv
import os


def dl_image(image_url):
    r = requests.get(image_url)
    filename = image_url.rsplit('/', 1)[1]
    with open('img/' + filename, 'wb') as image:
        image.write(r.content)
    return


def save_data(data, argv):
    for option in argv:
        if option == "--save-img":
            path = os.getcwd()
            if os.path.isdir(path + '/img') == False:
                os.mkdir(path + '/img')
            for category in data:
                for book in category.books:
                    dl_image(book.details['image_url'])
            print(
                f'    [{Color.OKGREEN}OK{Color.ENDC}] images saved')

    path = os.getcwd()
    if os.path.isdir(path + '/data') == False:
        os.mkdir(path + '/data')

    headers = list(data[0].books[0].details.keys())
    for category in data:
        file_csv = open('data/' + category.name + ".csv", "w")
        writer = csv.writer(file_csv, delimiter=",")
        writer.writerow(headers)

        for book in category.books:
            values = list(book.details.values())
            writer.writerow(values)

        file_csv.close()
        print(
            f'    [{Color.OKGREEN}OK{Color.ENDC}] {category.name}.csv created')
