from datetime import date
import requests


class YaDisk:
    def __init__(self, token_ya_file):
        with open(token_ya_file, "r", encoding="utf-8") as file:
            self.token = file.read()
        self.folder = str(date.today())  # +'/'  нужна ли эта переменная она используется внутри одного метода

    def headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': 'OAuth ' + self.token}

    def get_link(self, path):
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        path = self.folder+'/'+path    # не самое удачное место
        params = {"path": path, "overwrite": "true"}
        response = requests.get(url=url, headers=self.headers(), params=params)
        return response.json()

    def new_folder(self):
        folder = str(input('Введите имя папки (Enter: по умолчанию текущая дата): '))
        if folder.strip():
            self.folder = folder
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": self.folder, "overwrite": "true"}
        response = requests.put(url=url, headers=self.headers(), params=params)


    def upload_from_disk(self, filename):
        href = self.get_link(filename)['href']
        response = requests.put(href, headers=self.headers(), data=open(filename, "rb"))
        return response

    def upload_from_url(self,url_param,  filename ):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload' #url_param = 'https://sun9-63.userapi.com/c9591/u00001/136592355/w_62aef149.jpg'
        path = self.folder+'/'+filename  # 'test/w_62aef149.jpg'
        params = {"path": path , "url": url_param }
        response = requests.post(url=url, headers=self.headers(),  params=params)
        return response
