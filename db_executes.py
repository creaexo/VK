""" Команды для создания таблиц. Можно добавляю сюда свои команды для sqlite. """

create_table_accounts = """CREATE TABLE IF NOT EXISTS accounts(
id INTEGER PRIMARY KEY,
login TEXT,
password TEXT,
account_id TEXT,
api TEXT,
pts TEXT,
creation_date INTEGER NULL,
messages_sended INTEGER NULL,
orders_friends INTEGER NULL,
ban BLOB);"""

query_create_table_new_messages = """CREATE TABLE IF NOT EXISTS new_messages(
id INTEGER PRIMARY KEY,
bot_id INTEGER,
vk_id TEXT,
message TEXT,
FOREIGN KEY (bot_id) REFERENCES accounts(id)
);"""
