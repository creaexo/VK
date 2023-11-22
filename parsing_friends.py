"""
    Эта программа, которая парсит друзей на страничках и выводит их id в текстовый документ. Для успешного парсинга,
    нужно чтоб у аккаунта, токен которого используется, был доступ к списку друзей парсящихся страниц.
    По умолчанию, выводятся пользователи, которые заходили на аккаунт не позже чем неделю назад и
    кому можно написать с незнакомой страницы. Прочитав официальную документацию по VK API, можно кастомизировать этот
    парсер под свои нужды. Документация по получению списка друзей: https://dev.vk.com/ru/method/friends.get
"""

from datetime import timedelta, datetime
import requests
import time

# Указываем адреса/id страниц в формате строк, через запятую
user_list = ['', '',]

# Указываем token для работы с API VK. Можно получить здесь: https://vkhost.github.io/
token = ''


def get_offset(users_id: str):
    """
        Так как vk выдаёт максимум 5000 друзей за один запрос, нужно делать множество запросов, каждый и которых
        должен начинаться с индекса последнего полученного друга. Эта функция высчитывает, сколько таких запросов
        потребуется сделать, чтобы пройтись по всем друзьям аккаунта.
        :param users_id: Адрес или id страницы, друзей которой парсим.
        :type users_id: Str.
    """
    try:
        response = requests.get('https://api.vk.com/method/friends.get', params={
            'access_token': token,
            'v': 5.131,
            'user_id': users_id,
            'sort': 'id_desc',
            'offset': 0,
        }).json()
        try:
            count = response['response']['count']
            return count
        except:
            print(response['error']['error_msg'])
    except Exception as E:
        print(E)
        return 0


def get_users(
        user_id: str, order: str = '', fields: str = '',
        last_seen: int = time.mktime((datetime.now() - timedelta(days=7)).timetuple())):
    """
        Функция получения подходящих по критериям друзей конкретной страницы, которым можно написать сообщение.
        :param user_id: Адрес или id страницы, друзей которой парсим.
        :param order:  Порядок, в котором нужно вернуть список друзей. Допустимые значения:
            random — возвращает друзей в случайном порядке.
            name — сортировать по имени. Данный тип сортировки работает медленно, так как сервер будет получать всех
            друзей, а не только указанное количество count. (работает только при переданном параметре fields).
            По умолчанию список сортируется в порядке возрастания идентификаторов пользователей.
        :param fields: Список дополнительных полей, которые необходимо вернуть. Значения указываются в формате одной строки
        перечисляясь через запятую. Доступные значения можно посмотреть здесь: https://dev.vk.com/ru/method/friends.get
            Значения last_seen и can_write_private_message не нужно указывать, они автоматически добавляются к запросу.
        :param last_seen: Дата и время последнего посещения пользователя. Если пользователь заходил на аккаунт не позже
        этого значения, то попадает в список подходящих пользователей. Указывается в формате UNIX.
    """
    fields = f'last_seen, can_write_private_message, {fields}'
    st = time.perf_counter()
    good_id_list = []
    offset = 0
    max_offset = get_offset(user_id)
    while offset < max_offset:
        response = requests.get('https://api.vk.com/method/friends.get', params={
            'access_token': token,
            'v': 5.199,
            'user_id': user_id,
            'order': order,
            'offset': offset,
            'count': 5000,
            'fields': fields
        }).json()['response']
        offset += 5000
        for item in response['items']:
            try:
                if item['last_seen']['time'] >= last_seen and item['can_write_private_message'] == 1:
                    good_id_list.append(item['id'])
                    print(item['id'])
            except:
                continue
    print(user_id + " - " + str(time.perf_counter()-st))
    return good_id_list


def start_parsing(file_name: str = 'users'):
    """
        Функция запуска парсинга.
        :param file_name: Имя файла.
        :type file_name: Str.
    """
    # Сюда будут заноситься id подходящих друзей из всех страниц
    all_users_users = []

    # Добавление друзей, прошедших фильтры, в общий лист по всем парсящимся страницам
    for user_from_list in user_list:
        all_users_users = list(set(all_users_users + get_users(user_from_list)))

    # Запись друзей
    for item in all_users_users:
        with open(f'{file_name}.txt', 'a+') as f:
            f.write(f'"{item}",\n')


start_parsing(file_name='file_name')
