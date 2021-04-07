# -*- coding: utf-8 -*-
import requests
import logging
import sys
import json
import datetime as dt

logging.basicConfig(level=logging.DEBUG, filename='log.txt', format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


class VLoad:
    def __init__(self):
        with open('token.txt') as f:
            self.token = f.read().strip()
        self.file_array = []
        self.data_photo = []
        self.filename = ''

    def save_photo(self):
        with open('data.json', 'w', encoding="utf-8") as outfile:
            json.dump(self.data_photo, outfile)
        outfile.close()

    def photos_get(self, count_us: str, user_id: str):
        URL_photo = "https://api.vk.com/method/photos.get"
        URL_user = "https://api.vk.com/method/users.get"
        params_user = dict(user_ids=user_id, access_token=self.token, v='5.130')
        res_user = requests.get(URL_user, params=params_user)
        res_user.json()
        r_u = res_user.json()['response'][0]['id']
        if int(count_us) == 0:
            params = {
                'user_id': r_u,
                'access_token': self.token,
                'v': '5.130',
                'album_id': 'profile',
                'extended': 'likes',
                'photo_sizes': '-1',
                'rev': '1'
            }
        else:
            params = {
                'user_id': r_u,
                'access_token': self.token,
                'v': '5.130',
                'album_id': 'profile',
                'extended': 'likes',
                'photo_sizes': '-1',
                'rev': '1',
                'count': count_us
            }
        res = requests.get(URL_photo, params=params)
        r = res.json()
        print(r)
        try:
            r['response']['items']
        except Exception as e:
            print('This profile is private')
            logger.error(e)
            logger.error('This profile is private')
            sys.exit(1)
        count_in_vk = int(r['response']['count'])
        if int(count_us) == 0:
            count_photo = r['response']['count']
        else:
            if int(count_us) < count_in_vk:
                count_photo = int(count_us)
            else:
                count_photo = count_in_vk
        i: int = 0
        while i < count_photo:
            url_vk = r['response']['items'][i]['sizes'][-1]['url']
            type_vk = r['response']['items'][i]['sizes'][-1]['type']
            likes_vk = r['response']['items'][i]['likes']['count']
            print(url_vk, ' ', type_vk, ' ', likes_vk)
            self.filename = str(likes_vk) + '.jpeg'
            if self.file_array.count(self.filename) < 1:
                self.file_array.append(self.filename)
            else:
                date_ph = dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                self.filename = str(date_ph) + '_' + self.filename
            self.file_array.append(self.filename)
            self.data_photo.append([url_vk, self.filename, type_vk])
            i += 1
        try:
            self.save_photo()
        except Exception as e:
            logger.error(e)
            sys.exit(1)
        return self.data_photo
