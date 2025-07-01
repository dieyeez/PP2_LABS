import psycopg2
import csv

conn = psycopg2.connect(
    dbname="suppliers",
    user="postgres",
    password="ainiddin31",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def init_db():
    # Таблица
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone VARCHAR(20) NOT NULL
        );
    """)

    # Функция: поиск по шаблону
    cur.execute("""
    CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
    RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR) AS $$
    BEGIN
        RETURN QUERY
        SELECT id, first_name, phone
        FROM phonebook
        WHERE first_name ILIKE '%' || pattern || '%'
           OR phone ILIKE '%' || pattern || '%';
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Процедура: добавить или обновить пользователя
    cur.execute("""
    CREATE OR REPLACE PROCEDURE add_or_update_user(p_name TEXT, p_phone TEXT)
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
            UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
        ELSE
            INSERT INTO phonebook (first_name, phone) VALUES (p_name, p_phone);
        END IF;
    END;
    $$;
    """)

    # Процедура: массовое добавление с валидацией
    cur.execute("""
    CREATE OR REPLACE PROCEDURE add_many_users(name_list TEXT[], phone_list TEXT[])
    LANGUAGE plpgsql
    AS $$
    DECLARE
        i INT := 1;
        invalid_phones TEXT[] := '{}';
    BEGIN
        WHILE i <= array_length(name_list, 1) LOOP
            IF phone_list[i] ~ '^[0-9]+$' THEN
                CALL add_or_update_user(name_list[i], phone_list[i]);
            ELSE
                invalid_phones := array_append(invalid_phones, phone_list[i]);
            END IF;
            i := i + 1;
        END LOOP;
        RAISE NOTICE 'Invalid phone numbers: %', invalid_phones;
    END;
    $$;
    """)

    # Функция: пагинация
    cur.execute("""
    CREATE OR REPLACE FUNCTION get_phonebook_page(p_limit INT, p_offset INT)
    RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR) AS $$
    BEGIN
        RETURN QUERY
        SELECT id, first_name, phone
        FROM phonebook
        ORDER BY id
        LIMIT p_limit OFFSET p_offset;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Процедура: удаление по имени или номеру
    cur.execute("""
    CREATE OR REPLACE PROCEDURE delete_user(p_identifier TEXT)
    LANGUAGE plpgsql
    AS $$
    BEGIN
        DELETE FROM phonebook
        WHERE first_name = p_identifier OR phone = p_identifier;
    END;
    $$;
    """)

    conn.commit()
    print("Database initialized.")

def insert_from_csv():
    filename = input("Path to CSV file: ")
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        names, phones = [], []
        for row in reader:
            names.append(row[0])
            phones.append(row[1])
    cur.execute("CALL add_many_users(%s, %s)", (names, phones))
    conn.commit()
    print("Data inserted from CSV.")

def insert_from_input():
    name = input("Insert name: ")
    phone = input("Insert phone number: ")
    cur.execute("CALL add_or_update_user(%s, %s)", (name, phone))
    conn.commit()
    print("Data inserted.")

def update_user():
    name = input("Insert name to update: ")
    phone = input("New phone: ")
    cur.execute("CALL add_or_update_user(%s, %s)", (name, phone))
    conn.commit()
    print("User updated.")

def query_data():
    print("1. Show all")
    print("2. Search by pattern")
    print("3. Paginated view")
    choice = input("Choice: ")

    if choice == '1':
        cur.execute("SELECT * FROM phonebook")
    elif choice == '2':
        pattern = input("Insert pattern: ")
        cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
    elif choice == '3':
        limit = int(input("Limit: "))
        offset = int(input("Offset: "))
        cur.execute("SELECT * FROM get_phonebook_page(%s, %s)", (limit, offset))
    else:
        print("Invalid choice.")
        return

    rows = cur.fetchall()
    for row in rows:
        print(row)

def delete_user():
    ident = input("Enter name or phone to delete: ")
    cur.execute("CALL delete_user(%s)", (ident,))
    conn.commit()
    print("User deleted.")

def menu():
    init_db()
    while True:
        print("\n=== PHONEBOOK MENU ===")
        print("1. Add users from CSV")
        print("2. Add user manually")
        print("3. Update user phone")
        print("4. Search users")
        print("5. Delete user")
        print("0. Exit")

        choice = input("Choice: ")

        if choice == '1':
            insert_from_csv()
        elif choice == '2':
            insert_from_input()
        elif choice == '3':
            update_user()
        elif choice == '4':
            query_data()
        elif choice == '5':
            delete_user()
        elif choice == '0':
            break
        else:
            print("Wrong choice.")

    cur.close()
    conn.close()
    print("Program exited.")

if __name__ == "__main__":
    menu()
