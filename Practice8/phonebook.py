import psycopg2
import csv
from config import load_config


def execute_query(sql, params=None, fetch=False):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                if fetch:
                    return cur.fetchall()
                conn.commit()
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None


# добавка или обновка
def insert_or_update_from_console():
    name = input("Введите имя: ").strip()
    phone = input("Введите телефон: ").strip()

    # чек имени
    if not name:
        print("Ошибка: имя не может быть пустым.")
        return

    if name.isdigit():
        print("Ошибка: имя не может состоять из цифр.")
        return

    # чек тф
    if not phone.isdigit():
        print("Ошибка: телефон должен содержать только цифры.")
        return

    if len(phone) != 11:
        print("Ошибка: телефон должен состоять из 11 цифр.")
        return

    sql = "CALL upsert_contact(%s, %s)"
    execute_query(sql, (name, phone))
    print(f"Контакт {name} обработан (добавлен или обновлен).")


# ищем по шабл
def search_contacts_advanced(pattern=""):
    sql = "SELECT * FROM find_contacts(%s)"
    results = execute_query(sql, (pattern,), fetch=True)

    if results:
        for row in results:
            print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[2]}")
    else:
        print("Ничего не найдено.")


# чекаем по страницам
def show_paged_contacts():
    try:
        limit = int(input("Сколько контактов вывести на странице? ").strip())
        offset = int(input("Сколько контактов пропустить? ").strip())
    except ValueError:
        print("Ошибка: введите числа.")
        return

    sql = "SELECT * FROM get_phonebook_paged(%s, %s)"
    results = execute_query(sql, (limit, offset), fetch=True)

    if results:
        for row in results:
            print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[2]}")
    else:
        print("Нет данных для отображения.")


# загрузка CSV
def upload_from_csv_bulk(file_name):
    names = []
    phones = []

    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # пропуск заголовка

            for row in reader:
                if len(row) < 2:
                    continue

                names.append(row[0].strip())
                phones.append(row[1].strip())

        sql = "SELECT * FROM bulk_insert_contacts(%s, %s)"
        rejected = execute_query(sql, (names, phones), fetch=True)

        print("Загрузка завершена.")

        if rejected:
            print("Отклоненные записи (неверный формат телефона):")
            for r in rejected:
                print(f"Имя: {r[0]}, Тел: {r[1]}")
        else:
            print("Все записи успешно обработаны.")

    except FileNotFoundError:
        print("Файл CSV не найден.")
    except Exception as e:
        print(f"Ошибка при загрузке CSV: {e}")


# удаление
def delete_contact_advanced():
    target = input("Введите имя или номер для удаления: ").strip()
    sql = "CALL delete_contact_by_name_or_phone(%s)"
    execute_query(sql, (target,))
    print(f"Запрос на удаление '{target}' выполнен.")


if __name__ == '__main__':
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Добавить/Обновить контакт")
        print("2. Загрузить из CSV")
        print("3. Поиск по шаблону")
        print("4. Просмотр по страницам")
        print("5. Удалить контакт")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == '1':
            insert_or_update_from_console()
        elif choice == '2':
            upload_from_csv_bulk('contacts.csv')
        elif choice == '3':
            filt = input("Введите часть имени или телефона для поиска: ").strip()
            search_contacts_advanced(filt)
        elif choice == '4':
            show_paged_contacts()
        elif choice == '5':
            delete_contact_advanced()
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверный пункт меню.")