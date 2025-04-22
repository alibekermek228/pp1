import psycopg2
import csv

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    database="phonebook",
    user="postgres",
    password="postgres",
    port="5432"
)
cur = conn.cursor()

# Создание таблицы
def create_table():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL
        )
    ''')
    conn.commit()

# Ввод записи вручную
def insert_from_console():
    name = input("Введите имя: ")
    phone = input("Введите номер: ")
    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    print("Запись добавлена")

# Загрузка из CSV
def insert_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()
    print("CSV-записи загружены!")

# Обновление записи
def update_entry():
    name = input("Введите имя пользователя для обновления: ")
    new_phone = input("Введите новый номер телефона: ")
    cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, name))
    conn.commit()
    print("Данные успешно обновлены!")

# Поиск по имени или номеру
def query_phonebook():
    query_type = input("Фильтровать по name/phone: ")
    if query_type not in ['name', 'phone']:
        print("Ошибка: можно фильтровать только по name или phone")
        return
    value = input("Введите значение для поиска: ")
    query = f"SELECT * FROM phonebook WHERE {query_type} ILIKE %s"
    cur.execute(query, ('%' + value + '%',))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Удаление записи
def delete_data():
    by = input("Удалить по name/phone? ")
    if by not in ['name', 'phone']:
        print("Ошибка: можно удалять только по name или phone")
        return
    value = input("Введите значение для удаления: ")
    cur.execute(f"DELETE FROM phonebook WHERE {by} = %s", (value,))
    conn.commit()
    print("Запись удалена!")

# Главное меню
def main():
    create_table()
    while True:
        print("\nМеню:")
        print("1 - Добавить запись (вручную)")
        print("2 - Загрузить из CSV")
        print("3 - Обновить запись")
        print("4 - Поиск")
        print("5 - Удалить запись")
        print("0 - Выход")
        choice = input("Выбор: ")

        if choice == '1':
            insert_from_console()
        elif choice == '2':
            file_path = input("Введите путь к CSV файлу: ")
            insert_from_csv(file_path)
        elif choice == '3':
            update_entry()
        elif choice == '4':
            query_phonebook()
        elif choice == '5':
            delete_data()
        elif choice == '0':
            break
        else:
            print("Неверный выбор!")

    cur.close()
    conn.close()

# Запуск
if __name__ == "__main__":
    main()
