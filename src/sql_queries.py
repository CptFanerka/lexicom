import sqlite3
import random
import time
from prettytable import PrettyTable


def print_table(cursor, table_name):
    query = f'SELECT * FROM {table_name} LIMIT 5'
    cursor.execute(query)
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = [i[0] for i in cursor.description]
    for row in rows:
        table.add_row(row)

    print(table)


db_connection = sqlite3.connect('lexicom_database.db')

cursor = db_connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS short_names (name TEXT, status INTEGER)')
short_names_list = [(f'nazvanie{i}', random.randint(0, 1)) for i in range(1, 700001)]
cursor.executemany('INSERT INTO short_names VALUES (?, ?)', short_names_list)
db_connection.commit()
print('short_names table filled with data')

cursor.execute('CREATE TABLE IF NOT EXISTS full_names (name TEXT, status INTEGER)')
extensions = ['mp3', 'avi', 'mov', 'mkv', 'wav', 'jpg', 'png', 'gif']
full_names_list = [(f'nazvanie{i}.{random.choice(extensions)}', None)
                   for i in range(1, 500001)]
cursor.executemany('INSERT INTO full_names (name, status) VALUES (?, ?)', full_names_list)
db_connection.commit()
print('full_names table filled with data')

start_time = time.time()
db_connection.execute('CREATE INDEX IF NOT EXISTS short_names_name_index ON short_names (name)')
db_connection.execute('CREATE INDEX IF NOT EXISTS full_names_name_index ON full_names (name)')
db_connection.commit()
print('indexes created')

print_table(cursor=cursor, table_name='short_names')
print_table(cursor=cursor, table_name='full_names')

"""
EXAMPLE
full_names.name = nazvanie1.mp3 (length=13)

instr(full_names.name, \'.\') ---> 10
substr(full_names.name, instr(full_names.name, \'.\'))) ---> .mp3
length(substr(full_names.name, instr(full_names.name, \'.\')))) == length(.mp3) ---> 4
substr(full_names.name, 1, length(13-4)) ---> nazvanie1

UPDATE full_names
SET status =
(SELECT status FROM short_names
WHERE 'nazvanie1' = short_names.name)
"""
cursor.execute('UPDATE full_names \
               SET status = \
               (SELECT status FROM short_names \
                WHERE substr(full_names.name, 1, \
                        length(full_names.name)-length(substr(full_names.name, instr(full_names.name, \'.\')))) \
                        = short_names.name)')
db_connection.commit()
end_time = time.time()

print(f"time spent: {end_time - start_time} seconds")
print_table(cursor=cursor, table_name='full_names')

db_connection.close()
