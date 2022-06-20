import os
import json
from datetime import date
import requests
from pprint import pprint
# https://dev.vk.com/method/photos.get

class VkScanner:
    def __init__(self, token_vk_file):
        with open(token_vk_file, "r", encoding="utf-8") as file:
            self.token = file.read()
            self.pic_list = []
            self.top_list = []
            self.top_list_dic = []
            self.downloaded_list = []
            self.downloaded_dic = []
            self.id = 1   # нужна ли?

    def size_rating(self, size):
        # lst = [[0,'w'],[1,'z'],[2,'y'],[3,'r'],[4,'q'],[5,'p'],[6,'o'],[7,'x'],[8,'m'],[9,'s']]
        if size == 'w':
            return 0
        if size == 'z':
            return 1
        if size == 'y':
            return 2
        if size == 'r':
            return 3
        if size == 'q':
            return 4
        if size == 'p':
            return 5
        if size == 'o':
            return 6
        if size == 'x':
            return 7
        if size == 'm':
            return 8
        if size == 's':
            return 9

    def get_pic_list(self, owner_id):
        flag = True
        self.id = owner_id
        while flag:
            url = 'https://api.vk.com/method/photos.get'
            params1 = {'owner_id': self.id, 'access_token': self.token, 'v': '5.131', 'album_id': 'profile',
                       'extended': '1'}  # убрать 'count': '20',
            resp = requests.get(url, params1).json()
            if list(resp.keys())[0] == 'error':
                    self.id = input('Неверный id попробуйте еще раз:')
            else:
                    flag = False

        resp = resp['response']['items']

        for sizes in resp:
            tpm_lst = []
            likes = sizes['likes']['count']
            for i in sizes['sizes']:
                tpm_lst.append([self.size_rating(i['type']), i['type'], i['url']])
            tpm_lst.sort()
            # print(lst[0])# lst[0] нужен только первый
            # self.pic_list.append({'rating': tpm_lst[0][0],'size':tpm_lst[0][1],'url':tpm_lst[0][2],'likes': likes} )
            self.pic_list.append([tpm_lst[0][0],  tpm_lst[0][1], tpm_lst[0][2], likes])
            self.pic_list.sort()


    def get_top_list(self, default):
        if not default:
            default = 5
        else:
            default = int(default)
        if len(self.pic_list) < default:  # когда def больше фоток
            default = len(self.pic_list)
        print(f' для акаунта id{self.id} найдено Top {default} фотографий')
        # фактическое количество ссылок которе должно быть незавичимо от default и вdода пользователя
        dic = {}
        for i in range(default):
            # self.top_list.append((self.pic_list[i][0], self.pic_list[i][1], self.pic_list[i][2]))
            # так будет список множеств
            dic = {'size': self.pic_list[i][1], 'url': self.pic_list[i][2], 'likes': self.pic_list[i][3]}
            if self.pic_list[i][2]:  # url не пустой
                self.top_list_dic.append(dic)
                # print('print(dic)')
                # print(dic)
        print('Ссылки есть к ' + str(len(self.top_list_dic)))
        return True

    def download_pic(self, variant):
        for dic in self.top_list_dic:
            today = str(date.today())  # условие если лайки одинаковые
            resp = requests.get(dic['url'])
            size = str(dic['size'])
            likes = str(dic['likes'])
            new_file = likes + '.jpg'
            if os.path.isfile(new_file):
                new_file = f'{likes}-{today}.jpg'
            i = 1  # для случая когда больше 2х файлов имеют одинаковое количество лайков
            if os.path.isfile(new_file):
                new_file = f'{likes}-{today}-{i}.jpg'
                i += 1

            self.downloaded_list.append([new_file, size])
            self.downloaded_dic.append({'file_name': new_file, 'size': size})
            if variant == '2':
                with open(new_file, 'wb') as f:
                    f.write(resp.content)
        return True

    def joson_create(self):
        lst = []
        for item in self.downloaded_list:
            dic = {'file_name': item[0], 'size': item[1]}
            lst.append(dic)

        dic = {}
        for item in self.downloaded_dic:
            dic = {'file_name': item['file_name'], 'size': item['size']}
            lst.append(dic)
        new_json = json.dumps(lst, indent=2)
        with open('output.json', 'w') as f:
            f.write(new_json)
        return True


    def clean_files(self):
        flag = True
        while flag:
            inp = input('Хотите удалить фалы с локального диска y/n?: ')
            if inp.lower() in ('y','n'):
                flag =False

        if inp == 'y':
            for file_name in self.downloaded_dic:
                os.remove(file_name['file_name'])
                print('Файлы удалены')
        else:
            print('копия осталась на локальном диске')
        return True
