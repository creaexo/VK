"""
    Здесь собраны все функции управления фермой аккаунтов, которые не взаимодействуют с базой данных. Для их работы
    необходимо создать токен для работы с VK API. Его можно сделать здесь:
"""


import vk_api_master.vk_api as api_vk
from random import randint
import time
import requests
from data import *


def add_friend(token: str, proxy: str, user_agent: str, user_id: str):
    """
        Функция, которая отправляет заявку в друзья.
        :param token: Принимает токен аккаунта для работы с VK API.
        :type token: Str.
        :param proxy: Принимает прокси адрес в формате: 'http://login:password@adres:port'.
        :type proxy: Str None.
        :param user_agent: Принимает юзерагент.
        :type user_agent: Str.
        :param user_id: Принимает id пользователя, которому будет отправлена заявка
        :type user_id: Str.
    """
    active_session = requests.Session()
    try:
        active_session.headers.update({'user-agent': user_agent})
    except:
        r = 'Ошибка использования юзерагента. Проверьте, правильно ли вы его указали?'
        print(r)
        return r
    try:
        active_session.proxies.update({"http": proxy, "https": proxy})
    except:
        r = 'Ошибка использования proxy. Проверьте, правильно ли вы указали значение?'
        print(r)
        return r
    api = api_vk.VkApi(token=token, session=active_session)
    try:
        api.method('list_friends.add', {'user_id': user_id})
    except Exception as E:
        print(f' ошибка {E} аккаунта - {token}')
        if E == '[177] Cannot add this user to list_friends as user not found':
            return 0
    return 1


def start_friending(accounts: list = list_accounts, proxies: list = list_proxies, useragent_value: list = list_useragent,
                    users: list = list_friends, count_applications: int = 15):
    """
        Функция, которая начинает отправку заявок в друзья по списку id пользователей, с итервалом от 20 до 40 минут.
        :param accounts: Принимает список с информацией об аккаунтах.
            Формат: accounts_list = [{"login": value, "password": value, "id": value, "api": value,
            "pts": value, "ban": value}, {"id":...]
        :type accounts: List.
        :param proxies: Список прокси адресов в формате: ['http://login:password@adres:port', None...]. Рекомендую
        использовать для каждого аккаунта личный прокси, так будет меньше подозрения от антиспам системы. Если же
        в списке меньше прокси, чем токенов рассылающих аккаунтов, то дойдя до крайнего прокси, начнётся повторное
        использование, начиная с первого. Если используется прокси с ротацией ip на каждый запрос, то можно использовать
        список с одной строкой прокси. То же касается отказа от прокси - список с одним None внутри(не рекомендуется).
        :type proxies: List.
        :param useragent_value: Список юзерагентов. Принцип аналогичен proxies: для каждого акка свой и т.д.
        :type useragent_value: List.
        :param users: Список id пользователй, которым будут отправляться заявки. Формат ['185001805','123456789'...]
        :type users: List.
        :param count_applications: Количество пользователей, которым отправит заявку каждый аккаунт. Чтобы не вызвать
        подозрения у антиспам системы, можно отправлять не более 15 заявок в друзья незнакомым людям с аккаунта в сутки.
        :type count_applications: Int.
    """
    counter = 0
    user_index = 0
    user_agent_index = 0
    proxy_index = 0
    count_proxy = len(proxies)
    count_accounts = len(accounts)
    while counter < count_applications:
        for token in accounts:
            result = add_friend(token['api'], proxies[proxy_index], useragent_value[user_agent_index], users[user_index])
            print(f' Заявка в друзья отправлена\n Отправлено - {user_index+1}')
            user_agent_index += 1
            if proxy_index+1 == count_proxy:
                proxy_index = 0
            else:
                proxy_index += 1
            if (accounts.index(token) + 1) == count_accounts * (1 + counter):
                counter += 1
                user_agent_index = 0
                sleep = randint(1200, 3600)
                print(sleep/60)
                time.sleep(sleep)
            if result == 1:
                user_index += 1
        user_agent_index, proxy_index = 0, 0


def mess(token: str, proxy: str, user_agent: str, message: str, user_id: str):
    """
        Функция, которая отправляет сообщение.
        :param token: Принимает токен аккаунта для работы с VK API.
        :type token: Str.
        :param proxy: Принимает прокси адрес в формате: 'http://login:password@adres:port'.
        :type proxy: Str None.
        :param user_agent: Принимает юзерагент.
        :type user_agent: Str.
        :param message: Текст сообщения.
        :type message: Str.
        :param user_id: Принимает id пользователя, которому будет отправлено сообщение
        :type user_id: Str.
    """
    active_session = requests.Session()
    try:
        active_session.headers.update({'user-agent': user_agent})
    except:
        r = 'Ошибка использования юзерагента. Проверьте, правильно ли вы его указали?'
        print(r)
        return r
    if proxy is not None:
        try:
            active_session.proxies.update({"http": proxy, "https": proxy})
        except:
            r = 'Ошибка использования proxy. Проверьте, правильно ли вы указали значение?'
            print(r)
            return r
    api = api_vk.VkApi(token=token, session=active_session)
    try:
        api.method('messages.send', {'user_id': user_id, 'random_id': 0, 'message': message})
    except Exception as E:
        if str(E) == '[7] Permission to perform this action is denied' or str(E) == "[902] Can't send messages to this user due to their privacy settings":
            return 0
        if 'HTTPSConnectionPool' in str(E):
            return 2
        print(f'mess: ошибка - {E} аккаунта - {token}')
    return 1
# mess(first_brazilia[0]['api'], proxies[4], useragent_value[19], messages[1], '185001805')


def wall_message(token: str, proxy: str, user_agent: str, wall: str, user_id: str):
    """
        Функция, которая отправляет пост в личное сообщение.
        :param token: Принимает токен аккаунта для работы с VK API.
        :type token: Str.
        :param proxy: Принимает прокси адрес в формате: 'http://login:password@adres:port'.
        :type proxy: Str None.
        :param user_agent: Принимает юзерагент.
        :type user_agent: Str.
        :param wall: Пост для отправки. Формат '{wall}{id владельца поста}_{id поста}' (без фигурных скобок).
        :type wall: Str.
        :param user_id: Принимает id пользователя, которому будет отправлен пост
        :type user_id: Str.
    """
    active_session = requests.Session()
    try:
        active_session.headers.update({'user-agent': user_agent})
    except:
        r = 'Ошибка использования юзерагента. Проверьте, правильно ли вы его указали?'
        print(r)
        return r
    try:
        active_session.proxies.update({"http": proxy, "https": proxy})
    except:
        r = 'Ошибка использования proxy. Проверьте, правильно ли вы указали значение?'
        print(r)
        return r
    api = api_vk.VkApi(token=token, session=active_session)
    try:
        api.method('messages.send', {'user_id': user_id, 'random_id': 0, 'attachment': wall})
    except:
        print(f'wall_message: ошибка аккаунта - {user_agent}')
        return 0
    return 1


def delete_posts(token: str, user_agent: str, user_id: str, proxy: str, start_posts: int, count_posts: int):
    """
        Функция, которая удаляет посты на стене страницы.
        :param token: Принимает токен аккаунта для работы с VK API.
        :type token: Str.
        :param proxy: Принимает прокси адрес в формате: 'http://login:password@adres:port'.
        :type proxy: Str None.
        :param user_agent: Принимает юзерагент.
        :type user_agent: Str.
        :param user_id: Принимает id пользователя, которому будет отправлен пост
        :type user_id: Str.
        :param start_posts: Id поста, начиная с которого, будут удаляться все посты.
        :type start_posts: Int.
        :param count_posts: Количество постов, которое нужно удалитьcount_posts.
        :type count_posts: Int.
    """
    active_session = requests.Session()
    try:
        active_session.headers.update({'user-agent': user_agent})
    except:
        r = 'Ошибка использования юзерагента. Проверьте, правильно ли вы его указали?'
        print(r)
        return r
    try:
        active_session.proxies.update({"http": proxy, "https": proxy})
    except:
        r = 'Ошибка использования proxy. Проверьте, правильно ли вы указали значение?'
        print(r)
        return r
    api = api_vk.VkApi(token=token, session=active_session)
    for i in range(start_posts, count_posts+1):
        try:
            api.method('wall.delete', {'owner_id': user_id, 'post_id': i})
        except Exception as E:
            print(f'не удалось удалить пост № {i} \n Ошибка - {E}')


def start_sending(accounts: list = list_accounts, proxies: list = list_proxies[0],
                  useragent_value: list = list_useragent, messages: list = list_messages,
                  users: list = list_users, count_messages: int = 20):
    """
        Функция, которая начинает рассылку сообщений по списку, с интервалом от 20 до 40 минут. Сначала все аккаунты
        отправляют первый вариант сообщения из списка, после задержки второй и т.д. При таком виде рассылки, аккаунты
        живут не так долго, как при отправке 'Привет' и переписки после ответа, зато люди сразу видят нужное сообщение.
        Стоит помнить про лимит на отправку сообщений незнакомым пользователям - 20 в сутки.
        :param accounts: Принимает список с информацией об аккаунтах.
            Формат: accounts_list = [{"login": value, "password": value, "id": value, value, "api": value,
            "pts": value, "ban": value},...]
        :type accounts: List.
        :param proxies: Список прокси адресов в формате: ['http://login:password@adres:port', None...]. Рекомендую
        использовать для каждого аккаунта личный прокси, так будет меньше подозрения от антиспам системы. Если же
        в списке меньше прокси, чем токенов рассылающих аккаунтов, то дойдя до крайнего прокси, начнётся повторное
        использование, начиная с первого. Если используется прокси с ротацией ip на каждый запрос, то можно использовать
        список с одной строкой прокси. То же касается отказа от прокси - список с одним None внутри(не рекомендуется).
        :type proxies: List.
        :param useragent_value: Список юзерагентов. Принцип аналогичен proxies: для каждого акка свой и т.д.
        :type useragent_value: List.
        :param messages: Список с текстами сообщений. Формат: ['Сообщение 1','Сообщение 2'...]
        :type messages: List.
        :param users: Список id пользователй, которым будут отправляться сообщения. Формат ['185001805','123456789'...]
        :type users: List.
        :param count_messages: Количество пользователей, которым отправит сообщение каждый аккаунт. Чтобы не вызвать
        подозрения у антиспам системы, можно отправлять не более 20 сообщений незнакомым людям с аккаунта в сутки.
        :type count_messages: Int.
    """
    counter = 0
    user_index = 0
    user_agent_index = 0
    message_index = 0
    proxy_index = 0
    count_user_agent = len(useragent_value)
    count_proxy = len(proxies)
    count_accounts = len(accounts)
    while counter < count_messages:
        for token in accounts:
            result = mess(token['api'], proxies[proxy_index], useragent_value[user_agent_index], messages[message_index],
                          users[user_index])
            print(f'Отправил все сообщения\nУспешно отправленных - {user_index+1}')
            user_agent_index += 1
            if proxy_index+1 == count_proxy:
                proxy_index = 0
            else:
                proxy_index += 1
            if user_agent_index+1 == count_user_agent:
                user_agent_index = 0
            else:
                user_agent_index += 1
            if (accounts.index(token) + 1) == count_accounts * (1 + counter):
                counter += 1
                message_index += 1
                sleep = randint(1200, 2400)
                print(sleep/60)
                time.sleep(sleep)
            if message_index % 10 == 0:
                message_index = 0
            if result == 1:
                user_index += 1
        user_agent_index, proxy_index = 0, 0


def start_sending_hello(accounts: list = list_accounts, proxies: list = list_proxies,
                        useragent_value: list = list_useragent,
                        text: str = 'Привет',
                        users: list = list_users,
                        count_messages: int = 20):
    """
        Функция, которая начинает рассылку одного и того же сообщения с интервалом от 20 до 40 минут. По умолчанию
        отправляется 'Привет', т.к. проверено, что аккаунты дольше живут, если регулярно отправлять именно это сообщение
        аккаунтам, не находящимся в друзьях. Поэтому не рекомендуется менять текст сообщения по умолчанию. Далее можно
        вести основную переписку с теми, кто ответил на наше приветствие.
        :param accounts: Принимает список с информацией об аккаунтах.
            Формат: accounts_list = [{"login": value, "password": value, "id": value, value, "api": value,
            "pts": value, "ban": value},...]
        :type accounts: List.
        :param proxies: Список прокси адресов в формате: ['http://login:password@adres:port', None...]. Рекомендую
        использовать для каждого аккаунта личный прокси, так будет меньше подозрения от антиспам системы. Если же
        в списке меньше прокси, чем токенов рассылающих аккаунтов, то дойдя до крайнего прокси, начнётся повторное
        использование, начиная с первого. Если используется прокси с ротацией ip на каждый запрос, то можно использовать
        список с одной строкой прокси. То же касается отказа от прокси - список с одним None внутри(не рекомендуется).
        :type proxies: List.
        :param useragent_value: Список юзерагентов. Принцип аналогичен proxies: для каждого акка свой и т.д.
        :type useragent_value: List.
        :param users: Список id пользователй, которым будут отправляться сообщения. Формат ['185001805','123456789'...]
        :type users: List.
        :param count_messages: Количество пользователей, которым отправит сообщение каждый аккаунт. Чтобы не вызвать
        подозрения у антиспам системы, можно отправлять не более 20 сообщений незнакомым людям с аккаунта в сутки.
        :type count_messages: Int.
        :param text: Текст сообщения. Не рекомендуется менять, если рассылка по незнакомым для аккаунтов пользователям.
        :type text: Str.
    """
    counter = 0
    user_index = 0
    user_agent_index = 0
    proxy_index = 0
    count_user_agent = len(useragent_value)
    count_proxy = len(proxies)
    count_accounts = len(accounts)
    while counter < count_messages:
        print('while')
        for token in accounts:
            result = mess(token['api'], proxies[proxy_index], useragent_value[user_agent_index], text, users[user_index])
            print(f'\nУспешно отправленных сообщений - {user_index+1}')
            if (accounts.index(token) + 1) == count_accounts * (1 + counter):
                counter += 1
                sleep = randint(1200, 3000)
                print(sleep/60)
                time.sleep(sleep)
            if proxy_index+1 == count_proxy:
                proxy_index = 0
            else:
                proxy_index += 1
            if user_agent_index+1 == count_user_agent:
                user_agent_index = 0
            else:
                user_agent_index += 1
            if result == 1:
                user_index += 1
        user_agent_index = 0
    if counter == count_messages:
        print("удали id до - " + users[user_index])


def proxy_test(user_agent: str, proxy: str):
    """
        Функция, которая проверяет прокси. Если прокси рабочий, то выводит в терминал ip адрес.
        :param proxy: Принимает прокси адрес в формате: 'http://login:password@adres:port'.
        :type proxy: Str None.
        :param user_agent: Принимает юзерагент.
        :type user_agent: Str.

    """
    active_session = requests.Session()
    try:
        active_session.headers.update({'user-agent': user_agent})
    except:
        print('Ошибка использования юзерагента. Проверьте, правильно ли вы его указали?')
    try:
        active_session.proxies.update({"http": proxy, "https": proxy})
    except:
        print('Ошибка использования proxy. Проверьте, правильно ли вы указали значение?')
    print('Proxy: ' + str(proxy) + '\nResponse: ' + str(active_session.get('http://icanhazip.com/').text) + '-------------')


def post(token: str, user_agent: str, user_id: str, proxy: str, message: str = 'Текст поста', attachments: str = ''):
    """
        Функция, которая создаёт пост на стене страницы.
        :param token: Принимает токен аккаунта для работы с VK API.
        :type token: Str.
        :param proxy: Принимает прокси адрес в формате: 'http://login:password@adres:port'.
        :type proxy: Str None.
        :param user_agent: Принимает юзерагент.
        :type user_agent: Str.
        :param user_id: Принимает id пользователя, на чьей стене будет сделан пост
        :type user_id: Str.
        :param message: Текст поста.
        :type message: Str.
        :param attachments: Материал, прикрепляемы к посту(видео, фото, опрос...).
            Формат: '{тип вложения}{id владельца вложения}_{id вложения}'. Пример для видео: video761651406_456239017
        :type attachments: Str.
    """
    active_session = requests.Session()
    try:
        active_session.headers.update({'user-agent': user_agent})
    except:
        r = 'Ошибка использования юзерагента. Проверьте, правильно ли вы его указали?'
        print(r)
        return r
    try:
        active_session.proxies.update({"http": proxy, "https": proxy})
    except:
        r = 'Ошибка использования proxy. Проверьте, правильно ли вы указали значение?'
        print(r)
        return r
    api = api_vk.VkApi(token=token, session=active_session)
    try:
        api.method('wall.post', {'owner_id': user_id, 'message': message, 'attachments': attachments})
    except Exception as E:
        print(f'не удалось создать пост \n {E}')


def change_phote(token: str, user_agent: str, proxy: str):
    """
        Функция, которая меняет главную фотографию страницы(аватарку).
        :param token: Принимает токен аккаунта для работы с VK API.
        :type token: Str.
        :param proxy: Принимает прокси адрес в формате: 'http://login:password@adres:port'.
        :type proxy: Str None.
        :param user_agent: Принимает юзерагент.
        :type user_agent: Str.
    """
    active_session = requests.Session()
    active_session.headers.update({'user-agent': user_agent})
    active_session.proxies.update({"http": proxy, "https": proxy})
    vk_session = api_vk.VkApi(token=token, session=active_session)

    vk = vk_session.get_api()

    url = vk.photos.getOwnerPhotoUploadServer()['upload_url']
    request = requests.post(url, files={'photo': open('Yava.jpg', 'rb')}).json()
    server = request['server']
    hash = request['hash']
    vk.photos.saveOwnerPhoto(server=server, hash=hash, photo=request['photo'])
    posts = vk.wall.get()
    post_id = posts["items"][0]["id"]
    vk.wall.delete(post_id=post_id)


def LPS(token: str, proxy: str, user_agent: str):
    """
        Функция возвращающая pts - Последнее значение параметра new_pts, полученное от Long Poll сервера, используется
        для получения действий, которые хранятся всегда. Нужен, чтобы получить новые сообщения.
        :param token: Принимает токен аккаунта для работы с VK API.
        :type token: Str.
        :param proxy: Принимает прокси адрес в формате: 'http://login:password@adres:port'.
        :type proxy: Str None.
        :param user_agent: Принимает юзерагент.
        :type user_agent: Str.
    """
    active_session = requests.Session()
    active_session.headers.update({'user-agent': user_agent})
    active_session.proxies.update({"http": proxy, "https": proxy})
    api = api_vk.VkApi(token=token, session=active_session)
    try:
        response = api.method('messages.getLongPollServer', {'need_pts': 1})
    except Exception as E:
        print(E)
        if str(E) == "[5] User authorization failed: user is blocked.":
            return 'ban'
        else:
            return 'proxy_fail'
    return str(response['pts'])


def all_LPS(accounts: list, proxies: list, useragent_value: list, filename: str = 'lsp_tokens'):
    """
        Функция создаёт текстовый файл, со словарями на каждый аккаунт, с обновлёнными значениями pts(Последнее значение
        параметра new_pts, полученное от Long Poll сервера, используется для получения действий, которые хранятся
        всегда. Нужен, чтобы получить новые сообщения.) Формат списка как принимаемый параметр accounts.
        :param accounts: Принимает список с информацией об аккаунтах.
            Формат: accounts_list = [{"login": value, "password": value, "id": value, value, "api": value,
            "pts": value, "ban": value},...]
        :type accounts: List.
        :param proxies: Список прокси адресов в формате: ['http://login:password@adres:port', None...]. Рекомендую
        использовать для каждого аккаунта личный прокси, так будет меньше подозрения от антиспам системы. Если же
        в списке меньше прокси, чем токенов рассылающих аккаунтов, то дойдя до крайнего прокси, начнётся повторное
        использование, начиная с первого. Если используется прокси с ротацией ip на каждый запрос, то можно использовать
        список с одной строкой прокси. То же касается отказа от прокси - список с одним None внутри(не рекомендуется).
        :type proxies: List.
        :param useragent_value: Список юзерагентов. Принцип аналогичен proxies: для каждого акка свой и т.д.
        :type useragent_value: List.
        :param filename: Название файла.
        :type filename: Str.
    """
    user_agent_index = 0
    proxy_index = 0
    count_user_agent = len(useragent_value)
    count_proxy = len(proxies)
    for token in accounts:
        try:
            with open(f'{filename}.txt', 'a+') as f:
                f.write("\n" + '{'+f'"login": "{token["login"]}","password": "{token["password"]}","id": "{token["id"]}","api": "{token["api"]}", "pts": "{LPS(token["api"], proxies[proxy_index], useragent_value[user_agent_index])}"'+'},')
            if proxy_index + 1 == count_proxy:
                proxy_index = 0
            else:
                proxy_index += 1
            if user_agent_index + 1 == count_user_agent:
                user_agent_index = 0
            else:
                user_agent_index += 1
        except Exception as E:
            print(E)


def get_all_ts(accounts: list = list_accounts,
               proxies: list = list_proxies,
               useragent_value: list = list_useragent) -> list:
    """
        Функция, возвращающая список из значений pts всех аккаунтов(Последнее значение
        параметра new_pts, полученное от Long Poll сервера, используется для получения действий, которые хранятся
        всегда. Нужен, чтобы получить новые сообщения.) Формат списка: ['10002222', '10001976'...]
        :param accounts: Принимает список с информацией об аккаунтах.
            Формат: accounts_list = [{"login": value, "password": value, "id": value, value, "api": value,
            "pts": value, "ban": value},...]
        :type accounts: List.
        :param proxies: Список прокси адресов в формате: ['http://login:password@adres:port', None...]. Рекомендую
        использовать для каждого аккаунта личный прокси, так будет меньше подозрения от антиспам системы. Если же
        в списке меньше прокси, чем токенов рассылающих аккаунтов, то дойдя до крайнего прокси, начнётся повторное
        использование, начиная с первого. Если используется прокси с ротацией ip на каждый запрос, то можно использовать
        список с одной строкой прокси. То же касается отказа от прокси - список с одним None внутри(не рекомендуется).
        :type proxies: List.
        :param useragent_value: Список юзерагентов. Принцип аналогичен proxies: для каждого акка свой и т.д.
        :type useragent_value: List.
    """
    user_agent_index = 0
    proxy_index = 0
    count_user_agent = len(useragent_value)
    count_proxy = len(proxies)
    pts_list = []
    for token in accounts:
        continue_for = False
        while continue_for == False:
            try:
                pts = LPS(token["api"], proxies[proxy_index], useragent_value[user_agent_index])
                if pts == 'ban':
                    continue_for = True
                    pts_list += ['0']
                elif pts == 'proxy_fail':
                    continue
                else:
                    continue_for = True
                    pts_list += [pts]
                with open('list_pts.txt', 'a+') as f:
                    f.write("\n" + f'"{pts}",')
                if proxy_index + 1 == count_proxy:
                    proxy_index = 0
                else:
                    proxy_index += 1
                if user_agent_index + 1 == count_user_agent:
                    user_agent_index = 0
                else:
                    user_agent_index += 1
            except Exception as E:
                print(E)
            user_agent_index += 1
    print(pts_list)
    return pts_list


def check_new_messages(token: str, pts: str, user_agent: str, proxy: str):
    """
        Функция, которая, в случае успеха, возвращает список с информацией о новых сообщениях и новом значении pts.
        В случае неуспешного запроса, по причине блокировки аккаунта, будет возвращена строка 'baned', при иных ошибках
        'error'.
        Формат списка:
        [
            [
                ['id отправителя', 'текст сообщения', 'id сообщения внутри диалога'],
                ['id отправителя', 'текст сообщения', 'id сообщения внутри диалога'],
                ...
            ],
            'новое значение pts'
        ]
        :param token: Принимает токен аккаунта для работы с VK API.
        :type token: Str.
        :param pts: Последнее значение параметра new_pts, полученное от Long Poll сервера, используется для получения
        действий, которые хранятся всегда. Нужен, чтобы получить новые сообщения. Можно получить функцией LPS().
        :type pts: Str.
        :param proxy: Принимает прокси адрес в формате: 'http://login:password@adres:port'.
        :type proxy: Str None.
        :param user_agent: Принимает юзерагент.
        :type user_agent: Str.
    """
    active_session = requests.Session()
    try:
        active_session.headers.update({'user-agent': user_agent})
    except:
        r = 'Ошибка использования юзерагента. Проверьте, правильно ли вы его указали?'
        print(r)
        return r
    if proxy is not None:
        try:
            active_session.proxies.update({"http": proxy, "https": proxy})
        except:
            r = 'Ошибка использования proxy. Проверьте, правильно ли вы указали значение?'
            print(r)
            return r
    api = api_vk.VkApi(token=token, session=active_session)
    messages = []
    try:
        print()
        response = api.method('messages.getLongPollHistory', {'pts': pts})
        new_pts = response["new_pts"]
        if new_pts == pts:
            return 0
        for i in response["messages"]["items"]:
            if i['out'] == 0:
                # print(str(i['conversation_message_id']) + '=' + str(type(i['conversation_message_id'])))
                messages += [[i['peer_id'], i['text'], i['conversation_message_id']]]
        return [messages, new_pts]
    except Exception as E:
        print(E)
        if str(E) == '[5] User authorization failed: user is blocked.':
            return 'baned'
        return 'error'


def count_dialog_messages(token: str, proxy: str, user_agent: str, user_id: str) -> int or str:
    """
        Функция, которая, выдаёт количество сообщений в диалоге.
        :param token: Принимает токен аккаунта для работы с VK API.
        :type token: Str.
        :param proxy: Принимает прокси адрес в формате: 'http://login:password@adres:port'.
        :type proxy: Str None.
        :param user_agent: Принимает юзерагент.
        :type user_agent: Str.
        :param user_id: Принимает id пользователя, диалог с которым проверяется.
        :type user_id: Str.
    """
    active_session = requests.Session()
    try:
        active_session.headers.update({'user-agent': user_agent})
    except:
        r = 'Ошибка использования юзерагента. Проверьте, правильно ли вы его указали?'
        print(r)
        return r
    if proxy is not None:
        try:
            active_session.proxies.update({"http": proxy, "https": proxy})
        except:
            r = 'Ошибка использования proxy. Проверьте, правильно ли вы указали значение?'
            print(r)
            return r
    api = api_vk.VkApi(token=token, session=active_session)
    try:
        response = api.method('messages.getHistory', {'count': 1, 'user_id': user_id})['count']
    except Exception as E:
        print(E)
        return 'error: count_dialog_messages'
    return response


def check_new_replies(accounts: list = list_accounts, proxies: list = list_proxies,
                      useragent_value: list = list_useragent):
    """
        Функция, которая выводит в терминал информацию о новых сообщениях на всех аккаунтах.
        :param accounts: Принимает список с информацией об аккаунтах.
            Формат: accounts_list = [{"login": value, "password": value, "id": value, value, "api": value,
            "pts": value, "ban": value},...]
        :type accounts: List.
        :param proxies: Список прокси адресов в формате: ['http://login:password@adres:port', None...]. Рекомендую
        использовать для каждого аккаунта личный прокси, так будет меньше подозрения от антиспам системы. Если же
        в списке меньше прокси, чем токенов рассылающих аккаунтов, то дойдя до крайнего прокси, начнётся повторное
        использование, начиная с первого. Если используется прокси с ротацией ip на каждый запрос, то можно использовать
        список с одной строкой прокси. То же касается отказа от прокси - список с одним None внутри(не рекомендуется).
        :type proxies: List.
        :param useragent_value: Список юзерагентов. Принцип аналогичен proxies: для каждого акка свой и т.д.
        :type useragent_value: List.
    """
    user_agent_index = 0
    proxy_index = 0
    count_user_agent = len(useragent_value)
    count_proxy = len(proxies)
    for account in accounts:
        try:
            for i in check_new_messages(account['api'], proxies[proxy_index], useragent_value[user_agent_index], account['pts']):
                if i['out'] == 0 and i['read_state'] == 0:
                    if count_dialog_messages(account['api'], proxies[proxy_index], useragent_value[user_agent_index], i['user_id']) < 4:
                        print(f'Пользователь {i["user_id"]} написал: {i["body"]}')
                    else:
                        print(f'Аккаунту: {account["id"]}\n не в первый раз пользователь {i["user_id"]} написал: {i["body"]}')
        except Exception as E:
            print(E)
        print(user_agent_index)
        if proxy_index + 1 == count_proxy:
            proxy_index = 0
        else:
            proxy_index += 1
        if user_agent_index + 1 == count_user_agent:
            user_agent_index = 0
        else:
            user_agent_index += 1


def replay_to_new_messages(accounts: list = list_accounts, proxies: list = list_proxies,
                           useragent_value: list = list_useragent,
                           answers: list =list_answers, answer: str = 'Ответ на первое сообщение'):
    """
        Функция, которая отвечает на все новые сообщения каждого аккаунта.
        :param accounts: Принимает список с информацией об аккаунтах.
            Формат: accounts_list = [{"login": value, "password": value, "id": value, value, "api": value,
            "pts": value, "ban": value},...]
        :type accounts: List.
        :param proxies: Список прокси адресов в формате: ['http://login:password@adres:port', None...]. Рекомендую
        использовать для каждого аккаунта личный прокси, так будет меньше подозрения от антиспам системы. Если же
        в списке меньше прокси, чем токенов рассылающих аккаунтов, то дойдя до крайнего прокси, начнётся повторное
        использование, начиная с первого. Если используется прокси с ротацией ip на каждый запрос, то можно использовать
        список с одной строкой прокси. То же касается отказа от прокси - список с одним None внутри(не рекомендуется).
        :type proxies: List.
        :param useragent_value: Список юзерагентов. Принцип аналогичен proxies: для каждого акка свой и т.д.
        :type useragent_value: List.
        :param answers: Список с ответами. Отправляться будет случайный из списка.
        :type answers: List.
        :param answer: Ответ на первое сообщение
        :type answers: Str.
    """
    user_agent_index = 0
    proxy_index = 0
    count_user_agent = len(useragent_value)
    count_proxy = len(proxies)
    count_answers = len(answers)
    for account in accounts:
        try:
            for i in check_new_messages(account['api'], proxies[proxy_index], useragent_value[user_agent_index],
                                        account['pts']):
                if i['out'] == 0 and i['read_state'] == 0:
                    if count_dialog_messages(account['api'], proxies[proxy_index], useragent_value[user_agent_index],
                                             i['user_id']) < 4:
                        mess(account['api'], proxies[proxy_index], useragent_value[20],
                             answers[randint(0, count_answers+1)], i['user_id'])
                    else:
                        mess(account['api'], proxies[proxy_index], useragent_value[20],
                             answer,
                             i['user_id'])
        except Exception as E:
            print(E)
        if proxy_index + 1 == count_proxy:
            proxy_index = 0
        else:
            proxy_index += 1
        if user_agent_index + 1 == count_user_agent:
            user_agent_index = 0
        else:
            user_agent_index += 1


# post(accounts[9], useragent_value[9], accounts_id[9], message_for_post)
#
# messages_info = {
#     "response": {
#         "history": [
#             [
#                 4,
#                 24,
#                 17,
#                 761651406
#             ],
#             [
#                 52,
#                 22,
#                 761651406,
#                 0
#             ]
#         ],
#         "messages": {
#             "count": 1,
#             "items": [
#                 {
#                     "date": 1676475115,
#                     "from_id": 761651406,
#                     "id": 24,
#                     "out": 0,
#                     "attachments": [],
#                     "conversation_message_id": 1,
#                     "fwd_messages": [],
#                     "important": false,
#                     "is_hidden": false,
#                     "peer_id": 761651406,
#                     "random_id": 0,
#                     "text": "привет"
#                 }
#             ]
#         },
#         "profiles": [
#             {
#                 "id": 761651406,
#                 "first_name": "Владимир",
#                 "last_name": "Соболев",
#                 "can_access_closed": true,
#                 "is_closed": false
#             }
#         ],
#         "new_pts": 10000075,
#         "from_pts": 10000073,
#         "conversations": [
#             {
#                 "peer": {
#                     "id": 761651406,
#                     "type": "user",
#                     "local_id": 761651406
#                 },
#                 "last_message_id": 24,
#                 "in_read": 0,
#                 "out_read": 24,
#                 "sort_id": {
#                     "major_id": 0,
#                     "minor_id": 24
#                 },
#                 "last_conversation_message_id": 1,
#                 "in_read_cmid": 0,
#                 "out_read_cmid": 1,
#                 "unread_count": 1,
#                 "is_marked_unread": false,
#                 "important": false,
#                 "can_write": {
#                     "allowed": true
#                 },
#                 "can_send_money": false,
#                 "can_receive_money": true
#             }
#         ]
#     }
# }
