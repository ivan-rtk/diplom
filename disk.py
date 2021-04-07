# -*- coding: utf-8 -*-
import requests
import logging
import sys
import json
import datetime as dt

logging.basicConfig(level=logging.DEBUG, filename='log.txt', format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


class Disk:
    def __init__(self):
        with open('ya_token.txt') as f1:
            self.token_yandex = f1.read().strip()
            self.data_photo = {'photo': []}

    def create_dir(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        dir_name = dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        params = {'path': dir_name}
        headers = {'Authorization': self.token_yandex}
        response = requests.put(url, params=params, headers=headers)
        print(response.json())
        if response.status_code == 201:
            return dir_name
        else:
            return 'error'

    def create_report_json(self):
        with open('data.json', 'w', encoding="utf-8") as outfile:
            json.dump(self.data_photo, outfile)
        outfile.close()

    def upload(self, dict_photo: list, dir_name: str):
        for i in dict_photo:
            url_photo = i[0]
            filename = i[1]
            type_photo = i[2]
            if dir_name:
                params = {'path': dir_name + '/' + filename}
            else:
                logger.error('error name dir')
                sys.exit(1)
            response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                    params=params,
                                    headers={'Authorization': f'OAuth {self.token_yandex}'})
            logger.info(response.json())
            image = requests.get(url_photo)
            try:
                href = response.json()['href']
                logger.info(response.status_code)
            except Exception as e:
                logger.error(e)
                logger.error(response.status_code)
                sys.exit(1)
            try:
                requests.put(href, image.content)
                self.data_photo['photo'].append({
                    'file_name': filename,
                    'size': type_photo
                })
            except Exception as e:
                logger.error(e)
                sys.exit(1)
