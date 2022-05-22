from yandex_disk import user_photo_upload_yd
from google_drive import user_photo_upload_gd
from data_json import Json_data_create


class User_list():
    def __init__(self):
        self.user_list = []
    def save_user_photo_to_YD(self, user, ya_token, data_list, ProgressBarWindow):
        user_photo_upload_yd(ya_token, user, data_list, ProgressBarWindow)
        Json_data_create(data_list)

    def save_all_user_photo_to_YD(self, ya_token, data_list, ProgressBarWindow):
        for user in self.user_list:
            user_photo_upload_yd(ya_token, user, data_list, ProgressBarWindow)
        Json_data_create(data_list)

    def save_user_photo_to_GD(self, folder_id, scopes, SERVICE_ACCOUNT_FILE, user, data_list, ProgressBarWindow):
        user_photo_upload_gd(folder_id, scopes, SERVICE_ACCOUNT_FILE, user, data_list, ProgressBarWindow)
        Json_data_create(data_list)

    def save_all_user_photo_to_GD(self, folder_id, scopes, SERVICE_ACCOUNT_FILE, data_list, ProgressBarWindow):
        for user in self.user_list:
            user_photo_upload_gd(folder_id, scopes, SERVICE_ACCOUNT_FILE, user, data_list, ProgressBarWindow)
        Json_data_create(data_list)