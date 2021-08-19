from bs4 import BeautifulSoup
import requests


class Fetch:
    def soup(url):
        try:
            response = requests.get(url)
        except:
            print("Error")
            return None
        soup = BeautifulSoup(response.content, "html.parser")
        return soup


def urlcat(base, chunk):
    for str in chunk.split('/'):
        if str != "..":
            base += ('/' + str)
    return base
