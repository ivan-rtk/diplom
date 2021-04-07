# -*- coding: utf-8 -*-
import logging
import disk as ya
import vk as vk

logging.basicConfig(level=logging.DEBUG, filename='log.txt', format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    start = input("""Введите количество фотографий для загрузки(или 0 если нужны все фотографии):""")
    id_user = input("""Введите id/username пользователя:""")
    vk_photos = vk.VLoad()
    dict_photo = vk_photos.photos_get(start, id_user)
    ya_uploader = ya.Disk()
    ya_dir = ya_uploader.create_dir()
    ya_uploader.upload(dict_photo, ya_dir)
    ya_uploader.create_report_json()
