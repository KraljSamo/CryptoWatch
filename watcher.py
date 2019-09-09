import requests
import os
from collections import defaultdict

import json

import datetime
import time

from notifier import Notifier

def datetime_to_string(dt):
    return dt.strftime("%m/%d/%Y, %H:%M:%S")

def string_to_datetime(st):
    return datetime.datetime.strptime(st, "%m/%d/%Y, %H:%M:%S")


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

        ids = [coin['id'] for coin in coin_data]
        self.coins = ids
        
        return ids
    
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

    def update_prices(self):
    
        url = '/simple/price'
        params = {
            'ids' : ','.join(self.top100),
            'vs_currencies' : 'usd'
        }

        prices = self.call_coingecko_api(url, params)

        current_time = datetime.datetime.now()
        current_time = current_time.replace(second=0, microsecond=0)
        current_time_string = datetime_to_string(current_time)

        for coin, value in prices.items():
            self.crypto_data[coin].append((current_time_string, value['usd']))
            print(coin, self.crypto_data[coin])

        return prices
    
    def check_coin_anomalies(self):
        
        notifications = []

        for coin, price_data in self.crypto_data.items():
            last_date, last_price = price_data[-1]
            last_date = string_to_datetime(last_date)
            
            index = len(price_data) - 2
            while index >= 0:
                date, value = price_data[index]
                date = string_to_datetime(date)
                if last_date - date > datetime.timedelta(hours=2):
                    break
                if value * (1 + self.price_change) < last_price:
                    notifications.append((last_price/value, coin, date, value, last_date, last_price))
                    break
                
                index -= 1
        
        return notifications

    def run(self):

        save_cycle = 0
        
        while True:
            try:
                self.update_prices()
                notifications = self.check_coin_anomalies()

                if len(notifications) > 0:
                    self.notifier.create_update_message(notifications)
                
                if save_cycle == 0:
                    self.save()
                
                save_cycle = (save_cycle + 1) % 10

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e)

            time.sleep(60)


if __name__ == '__main__':
    w = Watcher()
    # res = w.call_coingecko_api('/coins/markets', {'vs_currency' : 'usd'})
    w.run()
