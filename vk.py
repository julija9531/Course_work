import time
import datetime

import requests


class User_vk():
    def __init__(self, token, ident_album, user_list, ProgressBarWindow):
        ProgressBarWindow.change_user_all()

        user_list.user_list += [self]
        self.token = token
        self.soc_set = 'vk'
        self.ident_album = ident_album

        '''1. Получение данных акаунта:'''
        url_base = 'https://api.vk.com/method/'
        params_account = {'access_token': self.token,
                         'v': 5.131}
        resp_account = requests.get(url_base + 'account.getProfileInfo', params=params_account)
        self.first_name = str(resp_account.json()['response']['first_name'])
        self.last_name = str(resp_account.json()['response']['last_name'])
        self.user_id = resp_account.json()['response']['id']
        self.albums_list = []

        '''2. Получение данных по альбому "фотографии с моей страницы":'''
        ProgressBarWindow.change_album_all()

        self.albums_list += [Album(self.token, self.user_id, 'profile', 'Фотографии_профиля', ProgressBarWindow)]

        ProgressBarWindow.change_album_getinf()

        '''3. Получение данных по альбомам:'''
        if ident_album:
            params_albums = {'access_token': self.token,
                             'owner_id': self.user_id,
                             'v': 5.131}
            resp_albums = requests.get(url_base + 'photos.getAlbums', params=params_albums)
            for album in resp_albums.json()['response']['items']:
                ProgressBarWindow.change_album_all()

                self.albums_list += [Album(self.token, self.user_id, album['id'], str(album['title']), ProgressBarWindow)]

                ProgressBarWindow.change_album_getinf()

        ProgressBarWindow.change_user_getinf()


class Album():
    def __init__(self, token, user_id, album_id, album_title, ProgressBarWindow):
        self.album_id = album_id
        self.album_title = str(album_title)
        url_base = 'https://api.vk.com/method/'
        params_photos = {'access_token': token,
                         'owner_id': user_id,
                         'album_id': self.album_id,
                         'v': 5.131}
        resp_photos = requests.get(url_base + 'photos.get', params=params_photos)

        '''Получаем информацию о фото данного альбома, заполняем список фотографий'''
        self.photos = []
        for photo in resp_photos.json()['response']['items']:
            ProgressBarWindow.change_photo_all()

            photo_inf = {'date': datetime.datetime.fromtimestamp(photo['date']).strftime('%d.%m.%Y'),
                         'photo_id': photo['id'],
                         'max_size': photo['sizes'][-1]['type'],
                         'photo_url': photo['sizes'][-1]['url']}
            self.photos += [Photo(token, user_id, photo_inf)]

            ProgressBarWindow.change_photo_getinf()

            time.sleep(0.5) #Добавляем задержку, иначе сервер ругается на большое колличество запросов в секунду

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
    def __init__(self, token, user_id, photo_inf):
        self.date = photo_inf['date']
        self.photo_id = photo_inf['photo_id']
        self.max_size = str(photo_inf['max_size'])
        self.photo_url = photo_inf['photo_url']
        #Получение данных о количестве лайков на фото
        url_base = 'https://api.vk.com/method/'
        params_photos = {'access_token': token,
                         'type': 'photo',
                         'owner_id': user_id,
                         'item_id': self.photo_id,
                         'v': 5.131}
        resp_photos = requests.get(url_base + 'likes.getList', params=params_photos)
        try:
            self.like_count = str(resp_photos.json()['response']['count'])
            self.photo_name = str(self.like_count) + '.jpg'
        except:
            print('Увеличьте задержку строка 73 модуля vk')