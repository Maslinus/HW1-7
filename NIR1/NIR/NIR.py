import sqlite3
from faker import Faker
import random
import os

# Создание экземпляра Faker для генерации данных
fake = Faker('ru_RU')

# Функция для генерации одной строки данных
def generate_row():
    name = fake.name()
    age = random.randint(1, 100)
    gender = random.choice(['M', 'W']) 
    phon_number = generate_phone_number()
    birth_date = fake.date_of_birth(minimum_age=age, maximum_age=age).strftime('%d.%m.%Y')

    return (name, age, gender, birth_date, phon_number)

# Функция для генерации случайного номера
def generate_phone_number():
    area_code = random.randint(100, 999)
    first_part = random.randint(100, 999)
    second_part = random.randint(1000, 9999)
    return f"({area_code}) {first_part}-{second_part}"


# Функция для генерации n строк данных
def generate_rows(n):
    return [generate_row() for _ in range(n)]

# Функция для вставки одной строки данных в таблицу
def insert_row(db_path, row):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO Table_1 (name, age, gender, birth_date, phon_number) VALUES (?, ?, ?, ?, ?)', row)
    conn.commit()
    conn.close()

# Функция для вставки n строк данных в таблицу
def insert_rows(db_path, rows):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.executemany('INSERT INTO Table_1 (name, age, gender, birth_date, phon_number) VALUES (?, ?, ?, ?, ?)', rows)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Указание пути к базе данных
    db_path = 'D:\\Daniar\\Py_project\\Information_security\\NIR.db'

    n = int(input("Enter the number of rows to add: "))

    # Генерация и вставка одной строки данных
    row = generate_row()
    insert_row(db_path, row)

    # Генерация и вставка n строк данных
    rows = generate_rows(n)
    insert_rows(db_path, rows)

    # Вывод данных из базы для проверки
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM Table_1')
    for row in c.fetchall():
        print(row)
    conn.close()
