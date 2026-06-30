import psycopg2
import csv
from config import load_config


def execute_query(sql, params=None, fetch=False):
    config = load_config()

    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()

        cur.execute(sql, params)

        result = None
        if fetch:
            result = cur.fetchall()

        conn.commit()

        cur.close()
        conn.close()

        return result

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None


# добв контакс с консоли
def insert_from_console():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")

    sql = """
    INSERT INTO phonebook(name, phone)
    VALUES (%s, %s);
    """

    execute_query(sql, (name, phone))
    print("Контакт добавлен!")


#загрузить данные цсв
def upload_from_csv(file_name):

    sql = """
    INSERT INTO phonebook(name, phone)
    VALUES (%s, %s);
    """

    try:
        with open(file_name, 'r', encoding='utf-8') as f:

            reader = csv.reader(f)

            next(reader)  

            for row in reader:

                if not row:
                    continue

                execute_query(sql, row)

        print(f"Данные из {file_name} загружены.")

    except FileNotFoundError:
        print("Файл CSV не найден.")


#обнова контакта
def update_contact(contact_id, new_name=None, new_phone=None):

    if new_name:
        execute_query(
            "UPDATE phonebook SET name = %s WHERE id = %s",
            (new_name, contact_id)
        )

    if new_phone:
        execute_query(
            "UPDATE phonebook SET phone = %s WHERE id = %s",
            (new_phone, contact_id)
        )

    print("Данные обновлены.")


#поиск
def search_contacts(filter_text=""):

    sql = """
    SELECT *
    FROM phonebook
    WHERE name ILIKE %s
    OR phone LIKE %s
    """

    results = execute_query(
        sql,
        (f'%{filter_text}%', f'{filter_text}%'),
        fetch=True
    )

    if results:
        for row in results:
            print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
    else:
        print("Контакты не найдены.")


#показ
def show_all_contacts():

    sql = "SELECT * FROM phonebook ORDER BY id"

    results = execute_query(sql, fetch=True)

    if results:
        print("\n----- Контакты -----")
        for row in results:
            print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
    else:
        print("Телефонная книга пуста.")


#удалить
def delete_contact(target):

    sql = """
    DELETE FROM phonebook
    WHERE name = %s
    OR phone = %s
    """

    execute_query(sql, (target, target))

    print("Контакт удален.")


if __name__ == '__main__':

    while True:

        print("\n====== PHONEBOOK ======")
        print("1. Добавить контакт")
        print("2. Загрузить из CSV")
        print("3. Обновить контакт")
        print("4. Поиск контакта")
        print("5. Показать все контакты")
        print("6. Удалить контакт")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            insert_from_console()

        elif choice == '2':
            upload_from_csv("contacts.csv")

        elif choice == '3':
            show_all_contacts()
            contact_id = int(input("Введите ID контакта: "))
            new_name = input("Новое имя (Enter - оставить): ")
            new_phone = input("Новый телефон (Enter - оставить): ")

            update_contact(contact_id, new_name or None, new_phone or None)

        elif choice == '4':
            text = input("Введите имя или начало номера: ")
            search_contacts(text)

        elif choice == '5':
            show_all_contacts()

        elif choice == '6':
            target = input("Введите имя или телефон: ")
            delete_contact(target)

        elif choice == '0':
            print("До свидания!")
            break

        else:
            print("Неверный выбор.")