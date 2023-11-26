"""
    Этот скрипт запускает функции создания таблиц для аккаунтов и сообщений. Автоматически создаёт файл с базой данных,
    если он ещё не создан. Главное, чтоб все папки, указанные db_name были созданы.
"""
from db_executes import query_create_table_new_messages, create_table_accounts
from db_functions import sqlite_execute

if __name__ == '__main__':
    sqlite_execute(db_name='db/database.db', execute=create_table_accounts)
    print('Таблица аккаунтов создана')
    sqlite_execute(db_name='db/database.db', execute=query_create_table_new_messages)
    print('Таблица новых сообщений создана')