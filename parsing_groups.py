"""
    Эта программа, которая парсит группы вк и выводит id пользователей, подходящих под выбранные параметры,
    в текстовый документ. По умолчанию, выводятся пользователи, которые заходили на аккаунт не позже чем неделю назад и
    кому можно написать с незнакомой страницы. Прочитав официальную документацию по VK API, можно кастомизировать этот
    парсер под свои нужды. Документация по получению пользователей групп: https://dev.vk.com/ru/method/groups.getMembers
"""

from datetime import timedelta, datetime
import requests
import time

# Указываем адреса/id групп в формате строк, через запятую
group_list = ['', '', ]

# Указываем token для работы с API VK. Можно получить здесь: https://vkhost.github.io/
token = ''


def get_offset(group: str):
    """
        Так как vk выдаёт максимум 1000 пользователей за один запрос, нужно делать множество запросов, каждый и которых
        должен начинаться с индекса последнего полученного пользователя. Эта функция высчитывает, сколько таких запросов
        потребуется сделать, чтобы пройтись по всем пользователям группы.
        :param group: Адрес или id группы.
        :type group: Str.
    """
    try:
        response = requests.get('https://api.vk.com/method/groups.getMembers', params={
                'access_token': token,
                'v': 5.131,
                'group_id': group,
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
        group: str, sort: str = 'id_desc', fields: str = '',
        last_seen: int = time.mktime((datetime.now() - timedelta(days=7)).timetuple())):
    """
        Функция получения подходящих по критериям пользователей, из конкретной группы, которым можно написать сообщение.
        :param group: Адрес или id группы.
        :param sort:  Сортировка, с которой необходимо вернуть список участников. Может принимать значения:
            id_asc — в порядке возрастания ID;
            id_desc — в порядке убывания ID;
            time_asc — в хронологическом порядке по вступлению в сообщество;
            time_desc — в антихронологическом порядке по вступлению в сообщество.
            Сортировка по time_asc и time_desc возможна только при вызове от модератора сообщества.
        :param fields: Список дополнительных полей, которые необходимо вернуть. Значения указываются в формате одной строки
        перечисляясь через запятую. Доступные значения можно посмотреть здесь: https://dev.vk.com/ru/method/groups.getMembers
            Значения last_seen и can_write_private_message не нужно указывать, они автоматически добавляются к запросу.
        :param last_seen: Дата и время последнего посещения пользователя. Если пользователь заходил на аккаунт не позже этого
            значения, то попадает в список подходящих пользователей. Указывается в формате UNIX.
    """
    fields = f'last_seen, can_write_private_message, {fields}'
    st = time.perf_counter()
    good_id_list = []
    offset = 0
    max_offset = get_offset(group)
    while offset < max_offset:
        response = requests.get('https://api.vk.com/method/groups.getMembers', params={
            'access_token': token,
            'v': 5.131,
            'group_id': group,
            'sort': sort,
            'offset': offset,
            'count': 1000,
            'fields': fields
        }).json()['response']
        offset += 1000
        for item in response['items']:
            try:
                if item['last_seen']['time'] >= last_seen and item['can_write_private_message'] == 1:
                    good_id_list.append(item['id'])
                    print(item['id'])
            except:
                continue
    print(group + " - " + str(time.perf_counter()-st))
    return good_id_list


def start_parsing(file_name: str = 'users'):
    """
        Функция запуска парсинга.
        :param file_name: Имя файла.
        :type file_name: Str.
    """
    # Сюда будут заноситься id подходящих пользователей из всех групп
    all_groups_users = []

    # Добавление пользователей, прошедших фильтры, в общий лист по всем группам
    for group_from_list in group_list:
        all_groups_users = list(set(all_groups_users + get_users(group_from_list)))

    # Запись пользователей
    for item in all_groups_users:
        with open(f'{file_name}.txt', 'a+') as f:
            f.write(f'"{item}",\n')


start_parsing(file_name='file_name')
