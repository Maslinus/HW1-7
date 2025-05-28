import sqlite3
from faker import Faker
import random
import os
import shutil
import time
import matplotlib.pyplot as plt

#   �������� ���������� Faker ��� ��������� ������.
fake = Faker('ru_RU')

#   ������� ��� �������� "���������" - ����� ���� ������ � ����� ������.
def create_sandbox(db_path, sandbox_path):
    shutil.copyfile(db_path, sandbox_path)

#   ����� ��� ������ � ��������.
class TableManager:
    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name

    # ������� ��� ��������� ���������� ������
    def generate_phone_number():
        area_code = random.randint(100, 999)
        first_part = random.randint(100, 999)
        second_part = random.randint(1000, 9999)
        return f"({area_code}) {first_part}-{second_part}"
    
    # ������� ��� ��������� n ����� ������
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

    # ������� ��� ������� n ����� ������ � ������� / ���� ������
    def insert_rows(self, rows):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.executemany(f'INSERT INTO {self.table_name} (name, age, gender, birth_date, phon_number) VALUES (?, ?, ?, ?, ?)', rows)

    #   ������� ��� ������� �������.
    def clear_table(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(f'DELETE FROM {self.table_name}')

    #   ������� ��� ���������� ������������� ������� � ��������� ������� ��� ����������.
    def execute_query_with_timing(self, query):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            start_time = time.time()  # ����� ������� ������ ���������� �������
            c.execute(query)  # ���������� �������
            end_time = time.time()  # ����� ������� ��������� ���������� �������
            execution_time = end_time - start_time  # ���������� ������� ���������� �������
            return execution_time

if __name__ == "__main__":
    #   �������� ���� � ���� ������.
    db_path = r'D:\\Daniar\\Py_project\\Information_security\\NIR.db'
    sandbox_path = r'D:\\Daniar\\Py_project\\Information_security\\NIR_sandbox.db'

    #   �������� "���������".
    create_sandbox(db_path, sandbox_path)

    #   ������ ���������� ����� � ������� ��� ���������.
    num_rows = int(input("Enter the number of rows to generate: "))
    table_choice = input("Enter the name of the table to generate (Table_1 or Table_2): ")

    #   ��������� � ������� ��������� ���������� ����� ������.
    table_manager = TableManager(sandbox_path, table_choice)
    rows = table_manager.generate_rows(num_rows)
    table_manager.insert_rows(rows)

    #   ��������� ������� ��������� ������ ��� ��������� ��������� �����.
    generation_times = []
    for n in range(1, num_rows + 1):
        start_time = time.time()
        rows = table_manager.generate_rows(n)
        table_manager.insert_rows(rows)
        end_time = time.time()
        generation_times.append(end_time - start_time)

    #   ���������� ������� ������� ��������� ������.
    plt.subplot(2, 1, 1)
    plt.plot(range(1, num_rows + 1), generation_times, marker='o')
    plt.title('Data generation time depending on the number of rows')
    plt.xlabel('Number of lines')
    plt.ylabel('Query execution time (seconds)')
    plt.grid(True)

    #   ������ ���������� ������������� ������� � ���������� ������� ����������.
    query = "SELECT COUNT(*) FROM Table_1"
    execution_time = table_manager.execute_query_with_timing(query)

    #   ��������� ������� ���������� ������� ��� ��������� ��������� �����.
    query_times = []
    for n in range(1, num_rows + 1):
        query = f"SELECT COUNT(*) FROM {table_choice}"
        start_time = time.time()
        table_manager.execute_query_with_timing(query)
        end_time = time.time()
        query_times.append(end_time - start_time)

    #   ���������� ������� ������� ���������� ��������.
    plt.subplot(2, 1, 2)
    plt.plot(range(1, num_rows + 1), query_times, marker='o')
    plt.title('Data generation time depending on the number of rows')
    plt.xlabel('Number of lines')
    plt.ylabel('Query execution time (seconds)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

