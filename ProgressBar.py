import tkinter as tk


class ProgressBar_Window():
    def __init__(self):
        self.window = tk.Tk()

        '''Создание шапки таблицы:'''
        self.label_head_0 = tk.Label(self.window, text='')
        self.label_head_0.grid(row=0, column=0)
        self.label_head_1 = tk.Label(self.window, text='Всего')
        self.label_head_1.grid(row=0, column=1)
        self.label_head_2 = tk.Label(self.window, text='Получено информации')
        self.label_head_2.grid(row=0, column=2)
        self.label_head_3 = tk.Label(self.window, text='Загружено в хранилище')
        self.label_head_3.grid(row=0, column=3)

        '''Пользователи:'''
        self.label_user_0 = tk.Label(self.window, text='Пользователи')
        self.label_user_0.grid(row=1, column=0)

        self.user_all = 0
        self.label_user_all = tk.Label(self.window, text=self.user_all) #Всего
        self.label_user_all.grid(row=1, column=1)

        self.user_getinf = 0
        self.label_user_getinf = tk.Label(self.window, text=self.user_getinf) #Получено информации
        self.label_user_getinf.grid(row=1, column=2)

        self.user_load = 0
        self.label_user_load = tk.Label(self.window, text=self.user_load) #Загружено в хранилище
        self.label_user_load.grid(row=1, column=3)

        '''Альбомы:'''
        self.label_album_0 = tk.Label(self.window, text='Альбомы')
        self.label_album_0.grid(row=2, column=0)

        self.album_all = 0
        self.label_album_all = tk.Label(self.window, text=self.album_all) #Всего
        self.label_album_all.grid(row=2, column=1)

        self.album_getinf = 0
        self.label_album_getinf = tk.Label(self.window, text=self.album_getinf) #Получено информации
        self.label_album_getinf.grid(row=2, column=2)

        self.album_load = 0
        self.label_album_load = tk.Label(self.window, text=self.album_load) #Загружено в хранилище
        self.label_album_load.grid(row=2, column=3)

        '''Фото:'''
        self.label_photo_0 = tk.Label(self.window, text='Фото')
        self.label_photo_0.grid(row=3, column=0)

        self.photo_all = 0
        self.label_photo_all = tk.Label(self.window, text=self.photo_all) #Всего
        self.label_photo_all.grid(row=3, column=1)

        self.photo_getinf = 0
        self.label_photo_getinf = tk.Label(self.window, text=0) #Получено информации
        self.label_photo_getinf.grid(row=3, column=2)

        self.photo_load = 0
        self.label_photo_load = tk.Label(self.window, text=self.photo_load) #Загружено в хранилище
        self.label_photo_load.grid(row=3, column=3)

        '''Обновление окна бара:'''
        self.window.update()

    def change_user_all(self):
        self.user_all += 1
        self.label_user_all = tk.Label(self.window, text=self.user_all) #Всего
        self.label_user_all.grid(row=1, column=1)
        self.window.update()
    def change_user_getinf(self):
        self.user_getinf += 1
        self.label_user_getinf = tk.Label(self.window, text=self.user_getinf)  # Получено информации
        self.label_user_getinf.grid(row=1, column=2)
        self.window.update()
    def change_user_load(self):
        self.user_load += 1
        self.label_user_load = tk.Label(self.window, text=self.user_load)  # Загружено в хранилище
        self.label_user_load.grid(row=1, column=3)
        self.window.update()

    def change_album_all(self):
        self.album_all += 1
        self.label_album_all = tk.Label(self.window, text=self.album_all)  # Всего
        self.label_album_all.grid(row=2, column=1)
        self.window.update()
    def change_album_getinf(self):
        self.album_getinf += 1
        self.label_album_getinf = tk.Label(self.window, text=self.album_getinf)  # Получено информации
        self.label_album_getinf.grid(row=2, column=2)
        self.window.update()
    def change_album_load(self):
        self.album_load += 1
        self.label_album_load = tk.Label(self.window, text=self.album_load)  # Загружено в хранилище
        self.label_album_load.grid(row=2, column=3)
        self.window.update()

    def change_photo_all(self):
        self.photo_all += 1
        self.label_photo_all = tk.Label(self.window, text=self.photo_all)  # Всего
        self.label_photo_all.grid(row=3, column=1)
        self.window.update()

    def change_photo_getinf(self):
        self.photo_getinf += 1
        self.label_photo_getinf = tk.Label(self.window, text=self.photo_getinf)  # Получено информации
        self.label_photo_getinf.grid(row=3, column=2)
        self.window.update()

    def change_photo_load(self):
        self.photo_load += 1
        self.label_photo_load = tk.Label(self.window, text=self.photo_load)  # Загружено в хранилище
        self.label_photo_load.grid(row=3, column=3)
        self.window.update()