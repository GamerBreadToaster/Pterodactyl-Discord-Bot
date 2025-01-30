import sqlite3
import os
import time

def ctime():
    return f"{time.strftime("%d-%m-%y | %H:%M:%S: ")}"


def get_db_connection():
    # get the data map
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(root_path, "data", "data.db")
    conn = sqlite3.connect(db_path)
    return conn

def create_table():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS servers (
        server_id INTEGER PRIMARY KEY,
        url TEXT,
        api_key TEXT)''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(ctime(), e)

def set_data(table: str, primary_key: int, data_type: str, value: str):
    """
    Sets the data of the server_id.

    :param table: the name of the table you want to use.
    :param primary_key: The primary key that dictates what information you want, for example from the table users use the user_id as the primary key. Input as integer.
    :param data_type: The type of data you want to change.
    :param value: The value of the data you want to change as a str.
    :return: returns nothing if nothing goes wrong, returns None if something does go wrong.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    data_type = data_type.lower()

    # get all table args or something idk how to call it and check if data_type == collums
    cursor.execute(f'PRAGMA table_info({table})')
    all_collums = cursor.fetchall()
    valid_data_types = []
    for collum in all_collums: valid_data_types += [collum[1]]
    if data_type not in valid_data_types:
        print(f"{ctime()}data_type {data_type} not right, returning None")
        return None

    # set the data
    cursor.execute(
        f"INSERT INTO {table} (server_id, {data_type}) VALUES (?, ?) ON CONFLICT(server_id) DO UPDATE SET {data_type} = ?",
        (primary_key, value, value))
    conn.commit()
    conn.close()
    print(f"{ctime()}Set the data from table: '{table}', for id: '{primary_key}', with data_type: '{data_type}' and value: '{value}'")
    return

def check_data(server_id: int):
    """
    Checks if there is data present in the database of the user and makes a database entry if there isn't

    :param server_id: The server id. Input as integer
    """

    # data checker
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM servers WHERE server_id = ?', (server_id,))
    all_collums = cursor.fetchall()
    if not all_collums == []: all_collums = all_collums[0]
    else: all_collums = [None]
    conn.close()

    if None in all_collums:
        create_table()
        set_data("servers", server_id, "url", "https://example.nice.com/")
        set_data("servers", server_id, "api_key", "view_api_key_at_profile_in_pte")

def get_data(table: str, primary_key: int, data_type: str):
    """
    Gets the amount of money a user has from the main json file.

    :param table: The name of the table you want the information from.
    :param primary_key: The primary key that dictates what information you want.
    :param data_type: The type of data you want.
    :return: The data. will return None if wrong data_type used.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    data_type = data_type.lower()

    # get all table args or something idk how to call it and check if data_type == collums
    cursor.execute(f'PRAGMA table_info({table})')
    all_collums = cursor.fetchall()
    valid_data_types = []
    for collum in all_collums: valid_data_types += [collum[1]]
    if data_type not in valid_data_types:
        print(f"{ctime()}Data_type {data_type} not right, returning None")
        return None

    # checking the data
    check_data(primary_key)

    # get data and return it
    cursor.execute(f"SELECT {data_type} FROM {table} WHERE server_id = ?", (primary_key,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        print(f"{ctime()}Data returned is not present or doesn't exist, or user_id doesn't exist. Returning None")
        return None
    print(f"{ctime()}Got the data from table: '{table}', for id: '{primary_key}', with data_type: '{data_type}' and returned value: '{result[0]}'")
    return result[0]

def main():
    pass

if __name__ == "__main__":
    main()