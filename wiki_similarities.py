__author__ = 'SteamPowered'
import requests as rq

class Wiki:
    def __init__(self, title_list):
        self.page_dict = {}
        self.simi_matrix = []
        for title in title_list:
            self.page_dict[title] = ''
        resp = str(rq.get('http://www.wikipedia.org/'))
        if resp == '<Response [200]>':
            print "\nWikipedia is working!"
        else:
            print "Wikipedia or your internet connection is not responding!"

    def fill_page_dict(self):
        return None

    def find_mems(self):
        return None

    def fill_sim_matrix(self):
        return None


if __name__ == "__main__":
    wk = Wiki(['a'])
    print wk.page_dict