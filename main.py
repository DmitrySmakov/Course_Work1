from vk_scanner import VkScanner
import ya_disk as ya1


owner_ids = ['1', '552934290', '3554188', '14098353']

def load_from_local(vk , ya):
    i =1
    for file_name in vk.downloaded_dic:
        print(f'Загрузка файла {file_name["file_name"]}  {i} из {len(vk.downloaded_dic)} ')
        i += 1
        ya.upload_from_disk(file_name['file_name'])
    print('Загрузка прошла успешно')

def load_from_url(vk, ya):
    i = 1
    for item in vk.top_list_dic:
        # print(item)
        f_name = str(item['likes'])+'_post'+'.jpg'
        print(f'Загрузка файла {f_name}  {i} из {len(vk.downloaded_dic)} ')
        i += 1
        ya.upload_from_url(item['url'], f_name)
    print('Загрузка прошла успешно')

def course_work():
    id = input('введите id пользователя: ')

    vk = VkScanner('token_vk.txt')
    vk.get_pic_list(id)  # id owner_ids[2]
    default = input('Введите количество фотографий (defaut=5) :')
    vk.get_top_list(default)
    flag = True
    while flag:
         variant = input('Выберите вариант загрузки: с сайта/ с локального диска/ выход: 1/ 2/ q:')
         if variant in ('1','2','q'):
             flag = False
             if variant == 'q':
                print('Загрузка отменена.')
                exit()

    vk.download_pic(variant)
    vk.joson_create()

    ya = ya1.YaDisk('token_ya.txt')
    ya.new_folder()

    if variant == '1':
        load_from_url(vk, ya)
    if variant == '2':
        load_from_local(vk, ya)
        vk.clean_files()


if __name__ == '__main__':
    course_work()
