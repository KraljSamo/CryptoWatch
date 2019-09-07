import requests
import os
from collections import defaultdict

import json

import datetime
import time

from notifier import Notifier


class Watcher():

    def __init__(self, price_change=0.05):

        self.crypto_data = defaultdict(list)
        self.notifier = Notifier()
        self.price_change = price_change
        self.base_url = 'http://api.coingecko.com/api/v3'
        self.top100 = self.get_top_100()

        try:
            current_path = os.getcwd()
            with open(os.path.join(current_path, 'price_history.json'), 'r+') as infile:
                self.crypto_data = json.load(infile)
        except:
            pass
    
    def get_top_100(self):
        url = '/coins/markets'
        params = {'vs_currency' : 'usd'}

        coin_data = self.call_coingecko_api(url, params)

        return coin_data
    
    def save(self, outfile_name='price_history.json'):
        with open(outfile_name, 'w') as outfile:
            json.dump(self.crypto_data, outfile, indent=1)
    
    def call_coingecko_api(self, url, params):
        try:        
            request = requests.get(self.base_url + url, params=params)
            return request.json()
        except Exception as e:
            print(e)
            return False

    def check_prices(self):
        pass

    def run(self):
        
        while True:
            time.sleep(5)
            try:
                x = 5
                print(x)
                print(1/0)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e)


if __name__ == '__main__':
    w = Watcher()
    res = w.call_coingecko_api('/coins/markets', {'vs_currency' : 'usd'})
    print(res)


