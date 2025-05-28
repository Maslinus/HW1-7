import sqlite3
from faker import Faker
import random
import os
import shutil
import time

# Создание экземпляра Faker для генерации данных
fake = Faker('ru_RU')

# Функция для создания "песочницы" - копии базы данных и схемы таблиц
def create_sandbox(db_path, sandbox_path):
    shutil.copyfile(db_path, sandbox_path)

# Класс для работы с таблицей
class TableManager:
    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name

    # Функция для генерации случайного номера
    def generate_phone_number():
        area_code = random.randint(100, 999)
        first_part = random.randint(100, 999)
        second_part = random.randint(1000, 9999)
        return f"({area_code}) {first_part}-{second_part}"
    
    # Функция для генерации n строк данных
    def generate_rows(self, n):
        rows = []
        for _ in range(n):
            name = fake.name()
            age = random.randint(1, 100)
            gender = random.choice(['M', 'W'])
            birth_date = fake.date_of_birth(minimum_age=age, maximum_age=age).strftime('%d.%m.%Y')
            phon_number = TableManager.generate_phone_number()

            rows.append((name, age, gender, birth_date, phon_number))
        return rows

    # Функция для вставки n строк данных в таблицу / авто коммит
    def insert_rows(self, rows):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.executemany(f'INSERT INTO {self.table_name} (name, age, gender, birth_date, phon_number) VALUES (?, ?, ?, ?, ?)', rows)

    # Функция для очистки таблицы
    def clear_table(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(f'DELETE FROM {self.table_name}')

    # Функция для выполнения произвольного запроса и измерения времени его выполнения
    def execute_query_with_timing(self, query):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            start_time = time.time()  # Замер времени начала выполнения запроса
            c.execute(query)  # Выполнение запроса
            end_time = time.time()  # Замер времени окончания выполнения запроса
            execution_time = end_time - start_time  # Вычисление времени выполнения запроса
            print(f"Query execution time: {execution_time:.6f} seconds")

# Пример использования функций
if __name__ == "__main__":
    # Указание пути к базе данных
    db_path = r'D:\\Daniar\\Py_project\\Information_security\\NIR.db'
    sandbox_path = r'D:\\Daniar\\Py_project\\Information_security\\NIR_sandbox.db'

    # Создание "песочницы"
    create_sandbox(db_path, sandbox_path)

    # Запрос количества строк и таблицы для генерации
    num_rows = int(input("Enter the number of rows to generate: "))
    table_choice = input("Enter the name of the table to generate (Table_1 or Table_2): ")

    # Генерация и вставка заданного количества строк данных
    table_manager = TableManager(sandbox_path, table_choice)
    rows = table_manager.generate_rows(num_rows)
    table_manager.insert_rows(rows)

    # Вывод данных из базы для проверки
    with sqlite3.connect(sandbox_path) as conn:
        c = conn.cursor()
        c.execute(f'SELECT * FROM {table_choice}')
        for row in c.fetchall():
            print(row)

    # Удаление всех данных из таблицы
    table_manager.clear_table()

    # Пример выполнения произвольного запроса с измерением времени выполнения
    query = "SELECT COUNT(*) FROM Table_1"
    table_manager.execute_query_with_timing(query)

