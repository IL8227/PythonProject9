import mysql.connector
from mysql.connector import Error
from config import Config


class DatabaseManager:
    def __init__(self):
        self.config = Config()

    def create_connection(self):
        """Создает соединение с базой данных"""
        try:
            connection = mysql.connector.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                database=self.config.DB_NAME
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def create_database(self):
        """Создает базу данных если она не существует"""
        try:
            connection = mysql.connector.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config.DB_NAME}")
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error creating database: {e}")

    def create_table(self):
        """Создает таблицу employees"""
        connection = self.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                create_table_query = """
                CREATE TABLE IF NOT EXISTS employees (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(255) NOT NULL,
                    birth_date DATE NOT NULL,
                    gender ENUM('male', 'female') NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(create_table_query)
                connection.commit()
                print("Table 'employees' created successfully")
            except Error as e:
                print(f"Error creating table: {e}")
            finally:
                cursor.close()
                connection.close()

    def optimize_database(self):
        """Создает индексы для оптимизации запросов"""
        connection = self.create_connection()
        if connection:
            try:
                cursor = connection.cursor()

                # Создаем составной индекс для быстрого поиска по полу и фамилии
                cursor.execute("""
                    CREATE INDEX idx_gender_full_name 
                    ON employees (gender, full_name)
                """)

                # Индекс только по полу
                cursor.execute("""
                    CREATE INDEX idx_gender 
                    ON employees (gender)
                """)

                # Индекс по первой букве фамилии
                cursor.execute("""
                    CREATE INDEX idx_full_name_prefix 
                    ON employees (full_name(1))
                """)

                connection.commit()
                print("Database optimized with indexes")
            except Error as e:
                print(f"Error optimizing database: {e}")
            finally:
                cursor.close()
                connection.close()