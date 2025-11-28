from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import mysql.connector
from config import Config


class Employee:
    def __init__(self, full_name: str, birth_date: str, gender: str):
        self.full_name = full_name
        self.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        self.gender = gender.lower()

    def calculate_age(self) -> int:
        """Рассчитывает полный возраст сотрудника"""
        today = date.today()
        return relativedelta(today, self.birth_date).years

    def save_to_db(self, connection):
        """Сохраняет объект сотрудника в базу данных"""
        cursor = connection.cursor()
        query = "INSERT INTO employees (full_name, birth_date, gender) VALUES (%s, %s, %s)"
        values = (self.full_name, self.birth_date, self.gender)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()

    def __str__(self):
        return f"{self.full_name}, {self.birth_date}, {self.gender}, {self.calculate_age()} years"


class EmployeeBatch:
    @staticmethod
    def save_batch(connection, employees: list):
        """Пакетно сохраняет массив объектов сотрудников в базу данных"""
        cursor = connection.cursor()
        query = "INSERT INTO employees (full_name, birth_date, gender) VALUES (%s, %s, %s)"

        # Подготавливаем данные для массовой вставки
        values = [(emp.full_name, emp.birth_date, emp.gender) for emp in employees]

        cursor.executemany(query, values)
        connection.commit()
        cursor.close()