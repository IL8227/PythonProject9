import random
from datetime import datetime, timedelta
from models import Employee


class DataGenerator:
    def __init__(self):
        self.first_names_male = ['Ivan', 'Petr', 'Sergey', 'Alexey', 'Dmitry', 'Andrey', 'Mikhail', 'Vladimir']
        self.first_names_female = ['Anna', 'Maria', 'Elena', 'Olga', 'Tatiana', 'Natalia', 'Irina', 'Svetlana']
        self.last_names = ['Ivanov', 'Petrov', 'Sidorov', 'Smirnov', 'Kuznetsov', 'Popov', 'Lebedev', 'Kozlov']
        self.middle_names_male = ['Ivanovich', 'Petrovich', 'Sergeevich', 'Alexeevich', 'Dmitrievich']
        self.middle_names_female = ['Ivanovna', 'Petrovna', 'Sergeevna', 'Alexeevna', 'Dmitrievna']

    def generate_random_employee(self):
        """Генерирует случайного сотрудника"""
        gender = random.choice(['male', 'female'])

        if gender == 'male':
            first_name = random.choice(self.first_names_male)
            last_name = random.choice(self.last_names)
            middle_name = random.choice(self.middle_names_male)
        else:
            first_name = random.choice(self.first_names_female)
            last_name = random.choice(self.last_names)
            middle_name = random.choice(self.middle_names_female)

        full_name = f"{last_name} {first_name} {middle_name}"

        # Генерируем случайную дату рождения (от 18 до 65 лет назад)
        end_date = datetime.now() - timedelta(days=365 * 18)
        start_date = end_date - timedelta(days=365 * 47)
        random_days = random.randint(0, (end_date - start_date).days)
        birth_date = start_date + timedelta(days=random_days)

        return Employee(full_name, birth_date.strftime('%Y-%m-%d'), gender)

    def generate_employees_with_f(self, count=100):
        """Генерирует сотрудников с мужским полом и фамилией на 'F'"""
        employees = []
        first_names = ['Fedor', 'Filipp', 'Felix', 'Foma']
        last_names_f = ['Fedorov', 'Fomin', 'Filatov', 'Frolov', 'Fadeev']

        for _ in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names_f)
            middle_name = random.choice(self.middle_names_male)

            full_name = f"{last_name} {first_name} {middle_name}"

            # Генерируем случайную дату рождения
            end_date = datetime.now() - timedelta(days=365 * 18)
            start_date = end_date - timedelta(days=365 * 47)
            random_days = random.randint(0, (end_date - start_date).days)
            birth_date = start_date + timedelta(days=random_days)

            employees.append(Employee(full_name, birth_date.strftime('%Y-%m-%d'), 'male'))

        return employees