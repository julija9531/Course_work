import os #Системная библиотека для работы с файлами (открытие/закрытие/сохранение)

import requests #Библиотека для работы с api
from PIL import Image #Pillow - Библиотека для работы с фото (определяем разрешение фото)


'''Создание папки на Яндекс Диске'''
def create_folder_yd(ya_token, folder_path):
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {'Content-Type': 'application/json', 'Authorization': 'OAuth ' + ya_token}
    params = {'path': folder_path}
    requests.put(url, headers=headers, params=params)


'''Загрузка файлов на Яндекс Диск'''
def user_photo_upload_yd(ya_token, user, data_list, ProgressBarWindow):

    if not user.soc_set in data_list: data_list[user.soc_set] = []

    url_yandex_disk = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers_yandex_disk = {'Content-Type': 'application/json', 'Authorization': 'OAuth ' + ya_token}

    '''Название папки Пользователя'''
    folder_path = str(user.last_name) +'_'+ str(user.first_name) +'_'+ user.soc_set +'_'+ str(user.user_id)
    create_folder_yd(ya_token, folder_path)

    '''Добавление информации о пользователе в файл данных:'''
    data_list[user.soc_set] += [{'first_name': user.first_name,
                                 'last_name': user.last_name,
                                 'user_id': user.user_id,
                                 'albums_list': []}]

    '''Перебор всех добавленных альбомов пользователя'''
    for album in user.albums_list:

        '''Добавление информации о альбоме в файл данных:'''
        data_list[user.soc_set][-1]['albums_list'] += [{'album_title': album.album_title,
                                                         'album_id': album.album_id,
                                                         'photos_list': []}]

        '''Путь до папки Альбома'''
        folder_path = user.last_name +'_'+ user.first_name +'_'+ user.soc_set +'_'+ str(user.user_id) +'/'\
                      + str(album.album_title) +'_'+ str(album.album_id)
        create_folder_yd(ya_token, folder_path)

        '''Перебор всех фото в текущем альбоме'''
        for photo in album.photos:

            '''Получение ссылки для загрузки на Яндекс Диск'''
            params_yandex_disk = {'path': folder_path + '/' + photo.photo_name, 'overwrite': 'true'}
            response = requests.get(url_yandex_disk, headers=headers_yandex_disk, params=params_yandex_disk)
            url_yandex_disk_2 = response.json()['href']

            '''Скачивание файла фото по ссылке (с сервера соц сети)'''
            photo_file = requests.get(photo.photo_url)

            '''Загрузка файла на Яндекс Диск'''
            requests.put(url_yandex_disk_2, data=photo_file)

            '''Определение разрешения фото'''
            with open('temp.jpg', 'wb') as temp_file:
                temp_file.write(photo_file.content)
                temp_file.close()
            im = Image.open('temp.jpg')
            photo.max_size = str(im.size[0]) + 'X' + str(im.size[1])
            im = None
            os.remove('temp.jpg')

            '''Добавление информации о фото в файл данных:'''
            data_list[user.soc_set][-1]['albums_list'][-1]['photos_list'] += [{'file_name':photo.photo_name,
                                                                       'size': photo.max_size}]
            '''Обновление прогресс бара'''
            ProgressBarWindow.change_photo_load()
        ProgressBarWindow.change_album_load()
    ProgressBarWindow.change_user_load()