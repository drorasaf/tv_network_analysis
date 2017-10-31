from http import client as HTTPStatus
import requests
import os

class SeriesNotFoundError(ValueError):
    pass
    


class DataRetriever(object):
    base_url = "https://api.thetvdb.com"
    token_url = base_url + "/login"
    series_url = base_url + "/search/series?name="

    def __init__(self):
        API_KEY = "B4AE06586934396A"
        USER_KEY = "74A92E8E82AE2CE6"
        USERNAME = "hellfliers"
        login_json = {'apikey': API_KEY, 'username': USERNAME,
                      'userkey': USER_KEY}
        self.sess = requests.Session()
        res = self.sess.post(self.token_url, json=login_json)

        if res.status_code != HTTPStatus.OK:
            raise ValueError('Unable to authenticate, code: %s',
                             str(res.status_code))
        self.token = res.json()['token']
        self.sess.headers.update({'Authorization': 'Bearer ' + self.token})

    # TODO: add rotten tomatos score and metacritic
    def get_series_info(self, name):
        search_res = self.sess.get(self.series_url + name)
        if search_res.status_code != HTTPStatus.OK:
            raise SeriesNotFoundError('Unable to get info for %s, code: %s', (name, str(search_res.status_code)))
#        print (search_res.json()["data"][0])
        series_id = search_res.json()["data"][0]["id"]
        res = self.sess.get(self.base_url + "/series/" + str(series_id))
        return self.convert_info_to_entry(res.json()["data"])

    def convert_info_to_entry(self, data):
        important_keys = ["seriesName", "network", "genre", "runtime", "firstAired", "siteRating", "siteRatingCount", "rating"]
        entry = {k: v for k, v in data.items() if k in important_keys}
        return entry
        
        
retriever = DataRetriever()
#res = retriver.get_series_info('narcos')
from channel_db import series_db
import pandas as pd
from contextlib import suppress
df = pd.DataFrame(columns=["seriesName", "network", "genre", "runtime", "firstAired", "siteRating", "siteRatingCount", "rating"])
print ("Total: %d" % sum(len(x) for x in series_db.values()))
print ("Amount of shows per network:")
for network, shows in series_db.items():
    print ("%s: %d" % (network, len(shows)))
    for _, show in enumerate(shows):
        #TODO: swithc from suppress to appending the errnoeous shows
        with suppress(SeriesNotFoundError):
            data = retriever.get_series_info(show)
            df = df.append(data, ignore_index=True)
df.to_csv('channel_series.csv')
