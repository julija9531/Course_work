'''используется для получения токена ВК'''
import os

import vk_api


def take_token(login, passw):
    VK = vk_api.VkApi(login, passw)
    VK.auth()
    VK = VK.get_api()
    try:
        User = VK.users.get()
    except:
        print("Error")
    else:
        with open('vk_config.v2.json', 'r') as data_file:
            data = json.load(data_file)
        for xxx in data[login]['token'].keys():
            for yyy in data[login]['token'][xxx].keys():
                access_token = data[login]['token'][xxx][yyy]['access_token']
        os.remove('vk_config.v2.json')
    return access_token


