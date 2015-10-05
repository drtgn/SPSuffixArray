__author__ = 'SteamPowered'
import requests as rq

class Wiki:
    def __init__(self):

        self.page_dict = {}

        resp = str(rq.get('http://www.wikipedia.org/'))
        if resp == '<Response [200]>':
            print "\nWikipedia is working!"


if __name__ == "__main__":
    wk = Wiki()