import time
import datetime
import hashlib
from pprint import pprint

import requests


def hash_md5(text):
    '''Переводим текст в байты'''
    ok_byte_to_md5 = text.encode('utf-8')
    '''Получаем hash в байтовом виде'''
    ok_byte_hash = hashlib.md5(ok_byte_to_md5)
    '''Переводим hash в текстовый вид, получаем нужный нам sig'''
    return ok_byte_hash.hexdigest()


class User_ok():
    def __init__(self, token_ok, ident_album, user_list, session_secret_key, application_key, ProgressBarWindow):
        ProgressBarWindow.change_user_all()

        user_list.user_list += [self]
        self.token = token_ok
        self.soc_set = 'ok'
        self.ident_album = ident_album
        url_ok = 'https://api.ok.ru/fb.do'

        '''1. Получение данных акаунта:'''
        method_ok_user = 'users.getCurrentUser'

        '''Собираем строку для хеширования md5'''
        ok_str_to_md5 = 'application_key=' + application_key + 'format=jsonmethod=' + method_ok_user + session_secret_key
        sig_ok_user = hash_md5(ok_str_to_md5)

        '''Запрашиваем информацию по профилю'''
        params_ok_user = {'application_key': application_key,
                     'format': 'json',
                     'method': method_ok_user,
                     'sig': sig_ok_user,
                     'access_token': token_ok}
        resp_ok = requests.get(url_ok, params=params_ok_user)
        self.first_name = str(resp_ok.json()['first_name'])
        self.last_name = str(resp_ok.json()['last_name'])
        self.user_id = resp_ok.json()['uid']
        self.albums_list = []

        '''2. Получение данных по альбому "фотографии с моей страницы":'''
        ProgressBarWindow.change_album_all()

        self.albums_list += [Album(self.user_id, 'profile', 'Фотографии_профиля', application_key, session_secret_key, token_ok, url_ok, True, ProgressBarWindow)]

        ProgressBarWindow.change_album_getinf()

        '''3. Получение данных по альбомам:'''
        if ident_album:
            method_ok_albums = 'photos.getAlbums'
            '''Собираем строку для хеширования md5'''
            ok_str_to_md5 = 'application_key=' + application_key + 'fid=' + str(self.user_id) + 'format=jsonmethod=' + method_ok_albums + session_secret_key
            sig_ok_albums = hash_md5(ok_str_to_md5)
            params_albums_ok = {'application_key': application_key,
                                'fid': self.user_id,
                                'format': 'json',
                                'method': method_ok_albums,
                                'sig': sig_ok_albums,
                                'access_token': token_ok}
            resp_albums_ok = requests.get(url_ok, params=params_albums_ok)
            for album in resp_albums_ok.json()['albums']:
                ProgressBarWindow.change_album_all()

                self.albums_list += [Album(self.user_id, album['aid'], album['title'], application_key, session_secret_key, token_ok, url_ok, False, ProgressBarWindow)]

                ProgressBarWindow.change_album_getinf()

        ProgressBarWindow.change_user_getinf()


class Album():
    def __init__(self, user_id, album_id, album_title, application_key, session_secret_key, token_ok, url_ok, ind_profil_photo, ProgressBarWindow):
        self.album_id = album_id
        self.album_title = str(album_title)
        self.photos = []

        '''Для получения фото профиля:'''
        if ind_profil_photo:
            method_ok_profile_photos = 'photos.getUserPhotos'
            '''Собираем строку для хеширования md5'''
            ok_str_to_md5 = 'application_key=' + application_key + 'fid=' + str(user_id) + 'format=jsonmethod=' + method_ok_profile_photos + session_secret_key
            sig_ok_profile_photos = hash_md5(ok_str_to_md5)
            params_profile_photos = {'application_key': application_key,
                                     'fid': user_id,
                                     'format': 'json',
                                     'method': method_ok_profile_photos,
                                     'sig': sig_ok_profile_photos,
                                     'access_token': token_ok}
            resp_ok_photos_list = requests.get(url_ok, params=params_profile_photos)

        else:
            '''Для получения фото альбомов'''
            method_ok_photos_list = 'photos.getUserAlbumPhotos'
            '''Собираем строку для хеширования md5'''
            ok_str_to_md5 = 'aid=' + str(self.album_id) +'application_key=' + application_key + 'format=jsonmethod=' + method_ok_photos_list + session_secret_key
            sig_ok_photos_list = hash_md5(ok_str_to_md5)
            params_ok_photos_list = {'aid': self.album_id,
                               'application_key': application_key,
                                'format': 'json',
                                'method': method_ok_photos_list,
                                'sig': sig_ok_photos_list,
                                'access_token': token_ok}
            resp_ok_photos_list = requests.get(url_ok, params=params_ok_photos_list)

        '''Получаем информацию о фото данного альбома, заполняем список фотографий'''
        for photo in resp_ok_photos_list.json()['photos']:
            ProgressBarWindow.change_photo_all()

            self.photos += [Photo(photo['fid'], application_key, session_secret_key, token_ok, url_ok)]
            time.sleep(0.3) #Добавляем задержку, иначе сервер ругается на большое колличество запросов в секунду

            ProgressBarWindow.change_photo_getinf()

        self.check_photos_name()

    def check_photos_name(self):
        '''Проверка на совпадение колличества лайков:'''
        for photo in self.photos:
            photo_list = [photo]
            for photo_2 in self.photos:
                if (photo != photo_2) and (photo.photo_name == photo_2.photo_name) and (photo.photo_name.find('_') == -1):
                    photo_list += [photo_2]
            if len(photo_list) > 1:
                for photo_3 in photo_list:
                    photo_3.photo_name = photo_3.photo_name[:-4] +'_'+ photo_3.date + photo_3.photo_name[-4:]

        '''Проверка на совпадение колличества лайков и даты:'''
        for photo in self.photos:
            photo_list = [photo]
            for photo_2 in self.photos:
                if (photo != photo_2) and (photo.photo_name == photo_2.photo_name):
                    photo_list += [photo_2]
            if len(photo_list) > 1:
                for i_1 in range(len(photo_list)):
                    photo_list[i_1].photo_name = photo_list[i_1].photo_name[:-4] +'_'+ str(i_1 + 1) + photo_list[i_1].photo_name[-4:]


class Photo():
    def __init__(self, photo_id, application_key, session_secret_key, token_ok, url_ok):
        self.photo_id = photo_id

        method_ok_photo_inf = 'photos.getPhotoInfo'
        fields_photo_inf = 'photo.user_id,photo.created_ms,photo.like_count,photo.pic_max'
        '''Собираем строку для хеширования md5'''
        ok_str_to_md5 = 'application_key=' + application_key + 'fields=' + fields_photo_inf + 'format=jsonmethod=' + method_ok_photo_inf + 'photo_id=' + str(self.photo_id) + session_secret_key
        sig_ok_photo_inf = hash_md5(ok_str_to_md5)
        params_ok_photo_inf = {'application_key': application_key,
                               'fields': fields_photo_inf,
                               'format': 'json',
                               'method': method_ok_photo_inf,
                               'photo_id': self.photo_id,
                               'sig': sig_ok_photo_inf,
                               'access_token': token_ok}
        resp_ok_photo_inf = requests.get(url_ok, params=params_ok_photo_inf)
        self.date = datetime.datetime.fromtimestamp(resp_ok_photo_inf.json()['photo']['created_ms']/1000).strftime('%d.%m.%Y')
        self.like_count = str(resp_ok_photo_inf.json()['photo']['like_count'])
        self.photo_name = str(self.like_count) + '.jpg'
        self.photo_url = resp_ok_photo_inf.json()['photo']['pic_max']
        self.max_size = 'max'