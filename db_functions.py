""" Здесь собраны все функции управления фермой аккаунтов, которые взаимодействуют с базой данных. """

import sqlite3
from db_executes import create_table_accounts
from functions import *


def sqlite_execute(db_name: str = 'db/database.db', execute: str = create_table_accounts):
    """
        Функция создания таблицы.
        :param db_name: Путь к файлу с базой данных и его название. Нужно, чтоб все папки, указанные в пути были созданы.
        :type db_name: Str.
        :param execute: Принимает SQLite запрос
        :type execute: Str.
    """
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(execute)


def sqlite_add_new_account(login: str, password: str, account_id: str, api: str, pts: str,
                           creation_date: int or str = 'Null', messages_sended: int or str = 'Null',
                           orders_friends: int or str = 'Null', ban: int = 0,
                           db_name: str = 'db/database.db', table: str = 'accounts'):
    """
        Функция добавления нового аккаунта в таблицу.
        :param login: Логин аккаунта. Номер телефона или почта без '+' вначале.
        :type login: Str.
        :param password: Пароль от аккаунта.
        :type password: Str.
        :param account_id: Id аккаунта.
        :type account_id: Str.
        :param api: API token аккаунта. Можно получить здесь: https://vkhost.github.io/.
        :type api: Str.
        :param pts: Последнее значение параметра new_pts, полученное от Long Poll сервера, используется
        для получения действий, которые хранятся всегда. Нужен, чтобы получить новые сообщения.
        :type pts: Str.
        :param creation_date: Дата и время создания аккаунта в формате UNIX. Чтоб не заполнять, нужно передать строку:
        'Null', которая является значением поумолчанию.
        :type creation_date: Int or Str.
        :param messages_sended: Сколько сообщений было отправлено аккаунтом.. Чтоб не заполнять, нужно передать строку:
        'Null', которая является значением поумолчанию.
        :type messages_sended: Int or Str.
        :param orders_friends: Сколько запросов в друзья было отправлено аккаунтом.. Чтоб не заполнять, нужно передать строку:
        'Null', которая является значением поумолчанию.
        :type orders_friends: Int or Str.
        :param ban: 1 - если аккаунт забанен, 0 - если нет.
        :type ban: Int.
        :param db_name: Путь к файлу с базой данных и его название. Нужно, чтоб все папки, указанные в пути были созданы.
        :type db_name: Str.
        :param table: Название таблицы.
        :type table: Str.
    """
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(f"""INSERT INTO {table}(login, password, account_id, api, pts, creation_date, messages_sended, orders_friends, ban) VALUES ('{login}', '{password}', '{account_id}', '{api}', '{pts}', {creation_date}, {messages_sended}, {orders_friends}, {ban});""")


def update_cell(column: str, column_new_value, cell_condition_value, db_name: str = 'db/database.db',
                table: str = 'accounts', cell_condition: str = 'id'):
    """
        Функция обновления ячейки таблицы.
        :param column: Название столбца, в котором находится изменяемая ячейка.
        :type column: Str.
        :param column_new_value: Новое значение, записывающееся в ячейку.
        :type column_new_value: Str or int.
        :param db_name: Путь к файлу с базой данных и его название. Нужно, чтоб все папки, указанные в пути были созданы.
        :type db_name: Str.
        :param table: Название таблицы.
        :type table: Str.
        :param cell_condition: Название столбца, по которому будет выполняться условие поиска конкретной ячейки.
        :type cell_condition: Str.
        :param cell_condition_value: Значение, по которому найдётся конкретная ячейка.
        :type cell_condition_value: Str or int or None.
    """
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(f"UPDATE {table} SET {column} = {column_new_value} WHERE {cell_condition} = {cell_condition_value};")


def update_many_cells(record_list: list, db_name: str = 'db/database.db', table: str = 'accounts', column: str = 'pts',
                      condition: str = 'id') -> str:
    """
        Функция обновления сразу нескольких ячеек таблицы.
        :param record_list: Принимает список со старыми значениями ячеек, и на какие значения их менять.
            Формат: record_list = [('Новое значение', Старое значение), ('Новое значение', Старое значение)...]
        :type record_list: List.
        :param db_name: Путь к файлу с базой данных и его название. Нужно, чтоб все папки, указанные в пути были созданы.
        :type db_name: Str.
        :param table: Название таблицы.
        :type table: Str.
        :param column: Название столбца, в котором находится изменяемая ячейка.
        :type condition: Str.
        :param condition: Название столбца, по которому будет выполняться условие поиска конкретной ячейки.
        :type column: Str.
    """
    try:
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            sqlite_update_query = f"UPDATE {table} SET {column} = ? WHERE {condition} = ?;"
            cursor.executemany(sqlite_update_query, record_list)
        return 'completed'
    except Exception as E:
        print(E)
        return 'failed'


def update_all_table(record_list: list, db_name: str = 'db/database.db', table: str = 'accounts', column: str = 'pts',
                     condition: str = 'id'):
    """
        Функция обновления сразу всех ячеек столбца. По умолчанию меняет значения по порядку возрастания id, что стоит
        учитывать при составлении record_list, поэтому же не рекомендуется менять значение condition.
        :param record_list: Принимает список с новыми значениями.
            Формат: record_list = ['Новое значение', 'Новое значение', 'Новое значение'...]
        :type record_list: List.
        :param db_name: Путь к файлу с базой данных и его название. Нужно, чтоб все папки, указанные в пути были созданы.
        :type db_name: Str.
        :param table: Название таблицы.
        :type table: Str.
        :param column: Название столбца, в котором находятся изменяемые ячейки.
        :type column: Str.
        :param condition: Название столбца, по которому будет выполняться условие поиска конкретной ячейки.
        Не рекомендуется изменять значение по умолчанию.
        :type condition: Str.
    """
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        q = 1
        for i in record_list:
            cursor.execute(f"UPDATE {table} SET {column} = {i} WHERE {condition} = {q};")
            q += 1
            print(i)


def take_value_from_table(db_name: str = 'db/db.db', table: str = 'accounts') -> list:
    """
        Функция, которая берёт данные из таблицы в БД и возвращает их в виде списка из словарей. Настроена под формат,
        который используется в ДБ по умолчанию. Если решите изменить его, придётся менять и эту функцию.
        :param db_name: Путь к файлу с базой данных и его название. Нужно, чтоб все папки, указанные в пути были созданы.
        :type db_name: Str.
        :param table: Название таблицы.
        :type table: Str.
    """
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        bots_data = []
        for row in cursor.fetchall():
            bots_data.append({"id": row[0], "login": row[1], "password": row[2], "account_id": row[3], "api": row[4],
                              "pts": row[5], "ban": row[9]})
    return bots_data


def change_all_pts_from_db():
    """
    Функция, которая обновляет pts у всех аккаунтов.
    """
    accounts = take_value_from_table()
    pts = get_all_ts(tokens=accounts)
    update_all_table(pts, table='accounts', column='pts')


def start_sending_hello_db(tokens: list, db_name: str = 'db/db.db', table: str = 'accounts', proxies: list = list_proxies,
                           second_proxies: list = list_proxies2, useragent_value: list = list_useragent, users: list = list_users,
                           count_messages: int = 20, text: str = 'Привет', answers: list =list_answers):
    """
        Функция, которая начинает рассылку одного и того же сообщения с интервалом от 20 до 40 минут. По умолчанию
        отправляется 'Привет', т.к. проверено, что аккаунты дольше живут, если регулярно отправлять именно это сообщение
        аккаунтам, не находящимся в друзьях. Поэтому не рекомендуется менять текст сообщения по умолчанию. Далее можно
        вести основную переписку с теми, кто ответил на наше приветствие.
        :param tokens: Принимает список с информацией об аккаунтах. Для получения списка из БД используется функция:
        take_value_from_table
            Формат: record_list = [{"id": value, "login": value, "password": value, "account_id": value, "api": value,
            "pts": value, "ban": value}, {"id":...]
        :type tokens: List.
        :param db_name: Путь к файлу с базой данных и его название. Нужно, чтоб все папки, указанные в пути были созданы.
        :type db_name: Str.
        :param table: Название таблицы.
        :type table: Str.
        :param proxies: Список прокси адресов в формате: ['http://login:password@adres:port', None...]. Рекомендую
        использовать для каждого аккаунта личный прокси, так будет меньше подозрения от антиспам системы. Если же
        в списке меньше прокси, чем токенов рассылающих аккаунтов, то дойдя до крайнего прокси, начнётся повторное
        использование, начиная с первого. Если используется прокси с ротацией ip на каждый запрос, то можно использовать
        список с одной строкой прокси. То же касается отказа от прокси - список с одним None внутри(не рекомендуется).
        :type proxies: List.
        :param second_proxies: Запасной список прокси, если вдруг основной не будет работать.
        :type second_proxies: List.
        :param useragent_value: Список юзерагентов. Принцип аналогичен proxies: для каждого акка свой и т.д.
        :type useragent_value: List.
        :param users: Список id пользователй, которым будут отправляться сообщения. Формат ['185001805','123456789'...]
        :type users: List.
        :param count_messages: Количество пользователей, которым отправит сообщение каждый аккаунт. Чтобы не вызвать
        подозрения у антиспам системы, можно отправлять не более 20 сообщений незнакомым людям с аккаунта в сутки.
        :type count_messages: Int.
        :param text: Текст сообщения. Не рекомендуется менять, если рассылка по незнакомым для аккаунтов пользователям.
        :type text: Str.
        :param answers: Во время действия программы происходит проверка на новые сообщения, вдруг кто ответил на наше
        приветствие. Если да, то в ответ отправляется один из вариантов ответов, предоставленных в этом листе.
        :type answers: List.
    """
    counter = 0
    user_index = 0
    user_agent_index = 0
    proxy_index = 0
    count_user_agent = len(useragent_value)
    count_proxy = len(proxies)
    count_tokens = len(tokens)
    count_answers = len(answers)
    while counter < count_messages:
        for token in tokens:
            if token['ban'] == 1:
                print('BANED')
                continue
            result = mess(token['api'], proxies[proxy_index], useragent_value[user_agent_index],
                          text, users[user_index])
            if result == 0:
                user_index += 1
                continue
            while result == 2:
                result = mess(token['api'], second_proxies[proxy_index], useragent_value[user_agent_index],
                              text, users[user_index])
            print(f'Успешно отправленных - {user_index+1}')

            new_messages = check_new_messages(token['api'], token['pts'], useragent_value[user_agent_index],
                                              proxy=proxies[proxy_index])
            if new_messages == 'error':
                print('error check new messages')
                continue
            elif new_messages == 'baned':
                update_cell(db_name=db_name, table=table, column="ban", column_new_value=1,
                            cell_condition='id', cell_condition_value=token['id'])
            elif new_messages != 0:
                for message_value in new_messages[0]:
                    if message_value[2] == 2:
                        mess(token['api'], proxies[proxy_index], useragent_value[user_agent_index],
                             answers[randint(0, count_answers+1)],
                             str(message_value[0]))
                        time.sleep(randint(20, 60))
                    if (str(message_value[0]) != '2000000001' and str(message_value[0]) != '2000000002'
                            and str(message_value[0]) != '-22822305'):
                        print(message_value)
                        try:
                            with sqlite3.connect(db_name) as db:
                                cursor = db.cursor()
                                print('try insert')
                                cursor.execute(
                                    f"""INSERT INTO messages(bot_id, vk_id, message) VALUES ({token["id"]}, "{str(message_value[0])}", "{str(message_value[1])}");""")
                                cursor.close()
                                print('end insert')
                        except Exception as E:
                            print(E)
                try:
                    update_cell(db_name=db_name, table=table, column="pts", column_new_value=new_messages[1],
                                cell_condition='id', cell_condition_value=token['id'])
                except Exception as E:
                    print(E)
            if proxy_index+1 == count_proxy:
                proxy_index = 0
            else:
                proxy_index += 1
            if user_agent_index+1 == count_user_agent:
                user_agent_index = 0
            else:
                user_agent_index += 1
            if (tokens.index(token) + 1) == count_tokens * (1 + counter):
                counter += 1
                sleep = randint(1200, 2400)
                print(sleep/60)
                time.sleep(sleep)
            if result == 1:
                user_index += 1
        user_agent_index, proxy_index = 0, 0
        tokens = take_value_from_table(db_name=db_name, table=table)
    print(users[user_index])





# change_all_ts_from_db()