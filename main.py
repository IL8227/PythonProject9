import sys
import time
from datetime import datetime
from database import DatabaseManager
from models import Employee, EmployeeBatch
from data_generator import DataGenerator


class EmployeeApp:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.data_generator = DataGenerator()

    def run(self):
        if len(sys.argv) < 2:
            print("Usage: python main.py <mode> [arguments]")
            print(
                "Modes: 1 - create table, 2 - add employee, 3 - show all, 4 - generate data, 5 - benchmark, 6 - optimize")
            return

        mode = sys.argv[1]

        if mode == '1':
            self.create_table()
        elif mode == '2':
            self.add_employee()
        elif mode == '3':
            self.show_all_employees()
        elif mode == '4':
            self.generate_data()
        elif mode == '5':
            self.benchmark_query()
        elif mode == '6':
            self.optimize_database()
        else:
            print(f"Unknown mode: {mode}")

    def create_table(self):
        """Режим 1: Создание таблицы"""
        self.db_manager.create_database()
        self.db_manager.create_table()
        print("Table creation completed")

    def add_employee(self):
        """Режим 2: Добавление сотрудника"""
        if len(sys.argv) != 5:
            print("Usage: python main.py 2 \"Full Name\" YYYY-MM-DD gender")
            return

        full_name = sys.argv[2]
        birth_date = sys.argv[3]
        gender = sys.argv[4].lower()

        try:
            employee = Employee(full_name, birth_date, gender)
            connection = self.db_manager.create_connection()
            if connection:
                employee.save_to_db(connection)
                print(f"Employee added: {employee}")
                connection.close()
        except Exception as e:
            print(f"Error adding employee: {e}")

    def show_all_employees(self):
        """Режим 3: Показать всех сотрудников с уникальным ФИО+дата"""
        connection = self.db_manager.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                SELECT DISTINCT full_name, birth_date, gender 
                FROM employees 
                ORDER BY full_name
                """
                cursor.execute(query)

                results = cursor.fetchall()
                print("Employees (unique by full_name + birth_date):")
                print("-" * 80)

                for row in results:
                    full_name, birth_date, gender = row
                    employee = Employee(full_name, birth_date.strftime('%Y-%m-%d'), gender)
                    age = employee.calculate_age()
                    print(f"{full_name:30} | {birth_date} | {gender:6} | {age:2} years")

                print(f"\nTotal unique employees: {len(results)}")

            except Exception as e:
                print(f"Error retrieving employees: {e}")
            finally:
                cursor.close()
                connection.close()

    def generate_data(self):
        """Режим 4: Генерация тестовых данных"""
        connection = self.db_manager.create_connection()
        if not connection:
            return

        try:
            batch_size = 1000
            total_records = 1000000
            special_records = 100

            print(f"Generating {total_records} random employees...")

            # Генерируем основные записи
            for i in range(0, total_records, batch_size):
                current_batch_size = min(batch_size, total_records - i)
                employees = [self.data_generator.generate_random_employee() for _ in range(current_batch_size)]
                EmployeeBatch.save_batch(connection, employees)

                if (i + current_batch_size) % 10000 == 0:
                    print(f"Generated {i + current_batch_size} records...")

            print(f"Generating {special_records} special employees (male, last name starts with 'F')...")

            # Генерируем специальные записи
            special_employees = self.data_generator.generate_employees_with_f(special_records)
            EmployeeBatch.save_batch(connection, special_employees)

            print("Data generation completed successfully")

        except Exception as e:
            print(f"Error generating data: {e}")
        finally:
            connection.close()

    def benchmark_query(self):
        """Режим 5: Бенчмарк запроса"""
        connection = self.db_manager.create_connection()
        if not connection:
            return

        try:
            cursor = connection.cursor()

            # Замер времени выполнения
            start_time = time.time()

            query = """
            SELECT * FROM employees 
            WHERE gender = 'male' AND full_name LIKE 'F%'
            """
            cursor.execute(query)

            results = cursor.fetchall()
            end_time = time.time()

            execution_time = end_time - start_time

            print(f"Query execution time: {execution_time:.4f} seconds")
            print(f"Records found: {len(results)}")

            # Выводим первые 5 результатов для проверки
            if results:
                print("\nFirst 5 results:")
                for i, row in enumerate(results[:5]):
                    print(f"{i + 1}. {row[1]} | {row[2]} | {row[3]}")

        except Exception as e:
            print(f"Error during benchmark: {e}")
        finally:
            cursor.close()
            connection.close()

    def optimize_database(self):
        """Режим 6: Оптимизация базы данных"""
        print("Optimizing database...")
        self.db_manager.optimize_database()
        print("Optimization completed")


if __name__ == "__main__":
    app = EmployeeApp()
    app.run()