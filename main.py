from user import User_list
from vk import User_vk
from vk_token import take_token
from ok import User_ok
from ProgressBar import ProgressBar_Window


if __name__ == '__main__':
    user_list = User_list()
    data_list = {}

    '''Создание окна прогресс бара'''
    ProgressBarWindow = ProgressBar_Window()

    '''Индикатор нужно ли получать все альбомы или только фото профиля:
       False - только фото профиля
       True - Фото из всех альбомов'''
    ident_album = True

    '''Индикатор на какой диск загружать фото
       YD - Яндекс диск;
       GD - Google Drive'''
    what_disk = 'GD'


    vk = True #Работа с Вконтакте
    if vk:
        '''Получение токена ВК по логину/паролю'''
        # login = ''
        # passw = ''
        # token_vk = take_token(login, passw)
        # print(token_vk)

        '''Ввод данных пользователей ВК:'''
        Skolov_token_vk = ''
        Skolov = User_vk(Skolov_token_vk, ident_album, user_list, ProgressBarWindow)


    ok = True # работа с одноклассниками
    if ok:
        '''Ввод данных приложения:'''
        ok_application_key = ''  # Публичный ключ приложения

        '''Ввод данных пользователей одноклассников:'''
        Pushkin_session_secret_key = '' #session_key
        Pushkin_token_ok = '' #Вечный session_key

        PushkinAS = User_ok(Pushkin_token_ok, ident_album, user_list, Pushkin_session_secret_key, ok_application_key, ProgressBarWindow)


    if what_disk == 'YD':
        '''Загрузка фото на Яндекс Диск:'''
        token_yandex_disk = ''

        # user_list.save_user_photo_to_YD(Skolov, token_yandex_disk, data_list, ProgressBarWindow)#Для загрузки фото 1 пользователя
        user_list.save_all_user_photo_to_YD(token_yandex_disk, data_list, ProgressBarWindow) #Для загрузки фото всех созданных пользователей

        '''Загрузка фото на Google Drive:'''
    elif (what_disk == 'GD'):
        folder_id = ''  # ID папки на GD, с которой будем работать
        scopes = ['https://www.googleapis.com/auth/drive']
        SERVICE_ACCOUNT_FILE = 'photoloadsocset-e45fe9adcee2.json'  # https://youtu.be/Lxxge05UP8M

        # user_list.save_user_photo_to_GD(folder_id, scopes, SERVICE_ACCOUNT_FILE, Skolov, data_list, ProgressBarWindow)#Для загрузки фото 1 пользователя

        user_list.save_all_user_photo_to_GD(folder_id, scopes, SERVICE_ACCOUNT_FILE, data_list, ProgressBarWindow) #Для загрузки фото всех созданных пользователей
    else:
        print('Неверно указан диск для загрузки фото!')

    print('Загрузка завершена.')



