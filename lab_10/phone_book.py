import csv
import psycopg2


def connect():
    return psycopg2.connect(
        database="suppliers",
        user="postgres",
        password="Ggg123ddd",
        host="localhost",
        port="5432"
    )


def insert_from_console():
    conn = connect()
    cur = conn.cursor()

    while True:
        name = input("Enter name (or 'stop' to finish): ")
        if name.lower() == "stop":
            break
        phone = input("Enter phone: ")
        cur.execute(
            "INSERT INTO PhoneBook (first_name, phone_number) VALUES (%s, %s)",
            (name, phone)
        )

    conn.commit()
    cur.close()
    conn.close()


def insert_from_csv(file_path):
    conn = connect()
    cur = conn.cursor()
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO PhoneBook (first_name, phone_number) VALUES (%s, %s)",
                (row['first_name'], row['phone_number'])
            )
    conn.commit()
    cur.close()
    conn.close()


def update_phone(name, new_phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE PhoneBook SET phone_number = %s WHERE first_name = %s", (new_phone, name))
    conn.commit()
    cur.close()
    conn.close()


def update_name(old_name, new_name):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE PhoneBook SET first_name = %s WHERE first_name = %s",
        (new_name, old_name)
    )
    conn.commit()
    cur.close()
    conn.close()


def search_by_name(name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM PhoneBook WHERE first_name = %s", (name,))
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("User not found.")

    cur.close()
    conn.close()


def search_by_phone(phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM PhoneBook WHERE phone_number = %s", (phone,))
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("Phone not found.")

    cur.close()
    conn.close()


def delete_by_name(name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM PhoneBook WHERE first_name = %s", (name,))
    conn.commit()
    cur.close()
    conn.close()


def delete_by_phone(phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM PhoneBook WHERE phone_number = %s",
        (phone,)
    )
    conn.commit()
    cur.close()
    conn.close()


def insert_from_csv_new(file_path):
    conn = connect()
    cur = conn.cursor()
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT INTO PhoneBook (first_name, phone_number)
                VALUES (%s, %s)
                ON CONFLICT (first_name)
                DO UPDATE SET phone_number = EXCLUDED.phone_number
            """, (row['first_name'], row['phone_number']))
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert from console")
        print("2. Insert from CSV (only add)")
        print("3. Insert from CSV (add or update)")
        print("4. Update phone by name")
        print("5. Update name")
        print("6. Search by name")
        print("7. Search by phone")
        print("8. Delete by name")
        print("9. Delete by phone")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            path = input("Enter CSV file path: ")
            insert_from_csv(path)
        elif choice == "3":
            path = input("Enter CSV file path: ")
            insert_from_csv_new(path)
        elif choice == "4":
            name = input("Enter name: ")
            new_phone = input("Enter new phone: ")
            update_phone(name, new_phone)
        elif choice == "5":
            old_name = input("Enter current name: ")
            new_name = input("Enter new name: ")
            update_name(old_name, new_name)
        elif choice == "6":
            name = input("Enter name: ")
            search_by_name(name)
        elif choice == "7":
            phone = input("Enter phone number: ")
            search_by_phone(phone)
        elif choice == "8":
            name = input("Enter name to delete: ")
            delete_by_name(name)
        elif choice == "9":
            phone = input("Enter phone to delete: ")
            delete_by_phone(phone)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
