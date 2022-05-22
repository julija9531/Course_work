from pprint import pprint #Библиотека для более удобного вывода информации на экран
import os #Системная библиотека для работы с файлами (открытие/закрытие/сохранение)

import requests #Библиотека для работы с api
from PIL import Image #Pillow - Библиотека для работы с фото (определяем разрешение фото)

'''Модули библиотеки Google API'''
from google.oauth2 import service_account #'''Работа с авторизацией'''
from googleapiclient.http import MediaFileUpload #'''Загрузка файлов на Google Drive'''
from googleapiclient.discovery import build #'''Создание ресурсов для обращения к API, то есть это некая абстракция над REST API Drive'''


'''Создание папки'''
def create_folder_gd(folder_id, service, folder_name):
    '''Проверка наличия папки, создание новой, в случае её отсутствия:'''
    results = service.files().list(pageSize=1000, fields="nextPageToken, files(id, name, mimeType, parents)",
                                   q="'" + folder_id + "'" + " in parents").execute()
    for file in results['files']:
        if (file['mimeType'] == 'application/vnd.google-apps.folder') and (file['name'] == folder_name):
            print('-' * 50)
            return file['id']
            break
    else:
        print('='*50)
        file_metadata = {'name': folder_name,
                         'mimeType': 'application/vnd.google-apps.folder',
                         'parents': [folder_id]}
        file = service.files().create(body=file_metadata, fields='id').execute() # в переменной file будет записан словарь с id созданной папки
        return file['id']


'''Загрузка файлов на Googlr Drive'''
def user_photo_upload_gd(folder_id, scopes, SERVICE_ACCOUNT_FILE, user, data_list, ProgressBarWindow):

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    service = build('drive', 'v3', credentials=credentials)

    if not user.soc_set in data_list: data_list[user.soc_set] = []

    '''Название папки Пользователя'''
    folder_user_name = str(user.last_name) +'_'+ str(user.first_name) +'_'+ user.soc_set +'_'+ str(user.user_id)
    folder_user_id = create_folder_gd(folder_id, service, folder_user_name)

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
        folder_album_name = str(album.album_title) +'_'+ str(album.album_id)
        folder_album_id = create_folder_gd(folder_user_id, service, folder_album_name)

        '''Перебор всех фото в текущем альбоме'''
        for photo in album.photos:

            '''Скачивание файла фото по ссылке (с сервера соц сети)'''
            temp_file_name = 'temp.jpg'
            photo_file = requests.get(photo.photo_url)
            with open(temp_file_name, 'wb') as temp_file:
                temp_file.write(photo_file.content)


            '''Загрузка файла на GD'''
            results = service.files().list(pageSize=1000, fields="nextPageToken, files(id, name, mimeType, parents)",
                                           q="'" + folder_album_id + "'" + " in parents").execute()
            for file in results['files']:
                if (file['mimeType'] == 'image/jpeg') and (file['name'] == photo.photo_name):
                    break
            else:
                file_path = temp_file_name
                file_metadata = {'name': photo.photo_name,
                                 'parents': [folder_album_id]}
                media = MediaFileUpload(file_path, resumable=True)
                service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                media = None

            '''Определение разрешения фото'''
            im = Image.open(temp_file_name)
            photo.max_size = str(im.size[0]) + 'X' + str(im.size[1])
            im = None
            os.remove(temp_file_name)

            '''Добавление информации о фото в файл данных:'''
            data_list[user.soc_set][-1]['albums_list'][-1]['photos_list'] += [{'file_name':photo.photo_name,
                                                                       'size': photo.max_size}]
            '''Обновление прогресс бара'''
            ProgressBarWindow.change_photo_load()
        ProgressBarWindow.change_album_load()
    ProgressBarWindow.change_user_load()