import json
import csv
from connect import get_connection

def show_menu():
    print("\n" + "=" * 40)
    print("           PHONEBOOK")
    print("=" * 40)
    print("1.  Show all contacts")
    print("2.  Delete contact")
    print("3.  Search contacts")
    print("4.  Search by email")
    print("5.  Filter by group")
    print("6.  Sort contacts")
    print("7.  Export JSON")
    print("8.  Import JSON")
    print("9.  Import CSV")
    print("10. Pagination")
    print("11. Add phone")
    print("12. Add contact")
    print("13. Move to group")
    print("0.  Exit")
    print("=" * 40)

#показ фулл
def show_all():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
    SELECT
        c.name,
        c.email,
        c.birthday,
        g.name AS group_name,
        p.phone,
        p.type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
""")
    
    rows = cur.fetchall()
    
    print("\n" + "=" * 100)
    print(f"{'Name':<15} {'Email':<25} {'Birthday':<12} {'Group':<10} {'Phone':<15} {'Type':<10}")
    print("=" * 100)
    
    for r in rows:
        name = r[0] or ""
        email = r[1] or ""
        birthday = str(r[2]) if r[2] else ""
        group = r[3] or ""
        phone = r[4] or ""
        phone_type = r[5] or ""

        print(f"{name:<15} {email:<25} {birthday:<12} {group:<10} {phone:<15} {phone_type:<10}")

    print("=" * 100)
    conn.close()

#удаление
def delete_contact():
    name = input("Name to delete: ")
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
    
    if cur.fetchone() is None:
        print("Contact not found")
    else:
        cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
        conn.commit()
        print("Deleted successfully")
    
    conn.close()

#  поиск
def search_contacts(query):
    conn = get_connection()
    cur = conn.cursor()
    # исполняет функцию с запросом и выдает все схожие резултаты с "query", и сохраняет все рузльтаты в rows как лист
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()

    print_contacts(rows)

    conn.close()

def search_email():
    email = input("Email: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM contacts
        WHERE email ILIKE %s
    """, (f"%{email}%",))

    print_contacts(cur.fetchall())

    conn.close()


# фильтрует по группе
def filter_by_group(group):
    conn = get_connection()
    cur = conn.cursor()
    # мы просим найти в таблице групп ту строку id которой совпадает с group_id у контакта
    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))
    # проходимся по каждой найденной строке по очереди и выводим
    for row in cur.fetchall():
        print(row)

    conn.close()


# сорт
def sort_contacts(option):
    conn = get_connection()
    cur = conn.cursor()

    if option == "name":
        cur.execute("SELECT * FROM contacts ORDER BY name")
    elif option == "birthday":
        cur.execute("SELECT * FROM contacts ORDER BY birthday")
    elif option == "date":
        cur.execute("SELECT * FROM contacts ORDER BY created_at")

    for row in cur.fetchall():
        print(row)

    conn.close()


# эксп в json
def export_json():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name as group_name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """)
    contacts = cur.fetchall()
    
    result = []
    for c in contacts:
        contact_id, name, email, birthday, group_name = c
        
        # получаем все телефоны этого контакта
        cur.execute(
            "SELECT phone, type FROM phones WHERE contact_id = %s",
            (contact_id,)
        )
        phones = [{"phone": p[0], "type": p[1]} for p in cur.fetchall()]
        
        result.append({
            "name": name,
            "email": email,
            "birthday": str(birthday) if birthday else None,
            "group": group_name,
            "phones": phones
        })
    
    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    conn.close()
    print("Exported to contacts.json")



# импорт из json
def import_json():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.json", encoding="utf-8") as f:
        data = json.load(f)

    for contact in data:
        name = contact["name"]
        email = contact["email"]
        birthday = contact["birthday"]
        group = contact["group"]
        phones = contact.get("phones", [])

        # проверка существования
        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists. skip/overwrite: ")
            if choice == "skip":
                continue
            cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        # группа
        gid = None
        if group:
            cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
            result = cur.fetchone()
            if result:
                gid = result[0]
            else:
                cur.execute(
                    "INSERT INTO groups(name) VALUES (%s) RETURNING id",
                    (group,)
                )
                gid = cur.fetchone()[0]

        # контакт
        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, email, birthday, gid))
        contact_id = cur.fetchone()[0]

        # все телефоны
        for p in phones:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, p["phone"], p["type"]))

    conn.commit()
    conn.close()
    print("Import completed")



# пагинация
def paginate():
    conn = get_connection()
    cur = conn.cursor()

    page = 0
    limit = 5

    while True:
        cur.execute(
            "SELECT * FROM get_phonebook_paged(%s, %s)",
            (limit, page * limit)
)

        rows = cur.fetchall()
        if not rows:
            print("No more data")
            break

        for r in rows:
            print(
        f"ID: {r[0]} | "
        f"Name: {r[1]} | "
        f"Email: {r[2]} | "
        f"Birthday: {r[3]} | "
        f"Group: {r[4]}"
    )

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            page += 1
        elif cmd == "prev" and page > 0:
            page -= 1
        else:
            break

    conn.close()

def import_csv():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.csv", newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["name"]
            email = row["email"]
            birthday = row["birthday"]
            group = row["group"]
            phone = row["phone"]
            phone_type = row["type"]

            cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
            exists = cur.fetchone()

            if exists:
                choice = input(f"{name} exists. skip/overwrite: ")

                if choice == "skip":
                    continue
                else:
                    cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

            cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
            gid = cur.fetchone()

            if gid is None:
                cur.execute(
                    "INSERT INTO groups(name) VALUES (%s) RETURNING id",
                    (group,)
                )
                gid = cur.fetchone()[0]
            else:
                gid = gid[0]

            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (name, email, birthday, gid))

            contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, phone, phone_type))

    conn.commit()
    conn.close()
    
    print("\n" + "=" * 40)
    print("CSV import completed successfully!")
    print("=" * 40 + "\n")

def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL add_phone(%s,%s,%s)",
        (name, phone, ptype)
    )

    conn.commit()
    conn.close()

def add_contact():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")
    phone = input("Phone: ")
    phone_type = input("Phone type (mobile/home/work): ")

    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
    gid = cur.fetchone()

    if gid is None:
        cur.execute(
            "INSERT INTO groups(name) VALUES (%s) RETURNING id",
            (group,)
        )
        gid = cur.fetchone()[0]
    else:
        gid = gid[0]

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (name, email, birthday, gid))

    contact_id = cur.fetchone()[0]
  
    cur.execute("""
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
    """, (contact_id, phone, phone_type))

    conn.commit()
    conn.close()

    print("Contact added")

def print_contacts(rows):
    print("\n" + "-"*60)
    print(f"{'Name':<20} {'Email':<25} {'Phone':<15}")
    print("-"*60)

    for r in rows:
        name = str(r[0])
        email = str(r[1])
        phone = str(r[2]) if len(r) > 2 else ""

        print(f"{name:<20} {email:<25} {phone:<15}")

    print("-"*60)

def move_to_group():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Contact name: ")
    group = input("New group: ")

    try:
        cur.execute(
            "CALL move_to_group(%s, %s)",
            (name, group)
        )

        conn.commit()
        print("Contact moved successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()

def main():
    while True:
        show_menu()
        choice = input("Choose option: ")

        if choice == "1":
            show_all()

        elif choice == "2":
            delete_contact()

        elif choice == "3":
            query = input("Search: ")
            search_contacts(query)

        elif choice == "4":
            search_email()

        elif choice == "5":
            group = input("Group: ")
            filter_by_group(group)

        elif choice == "6":
            option = input("Sort by (name/birthday/date): ")
            sort_contacts(option)

        elif choice == "7":
            export_json()
            print("Export done")

        elif choice == "8":
            import_json()
            print("Import done")

        elif choice == "9":
            import_csv()

        elif choice == "10":
            paginate()

        elif choice == "11":
            add_phone()

        elif choice == "12":
            add_contact()

        elif choice == "13":
            move_to_group()

        elif choice == "0":
            print("Exit programme")
            break

        else:
            print("Invalid option")




if __name__ == "__main__":
    main()