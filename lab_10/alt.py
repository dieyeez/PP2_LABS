import psycopg2
from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in {filename}')

    return db


def connect():
    try:
        params = config()
        conn = psycopg2.connect(**params)
        print("Подключение успешно!")
        conn.close()
    except Exception as error:
        print(f"Ошибка подключения: {error}")


connect()
