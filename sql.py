import sqlite3
from datetime import date
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occured")

def delete_all_records():
    delete_all = "DELETE FROM scores where id != 0"
    execute_query(connection, delete_all)

def add_entry(connection, player, score):
    # create_entries = "INSERT INTO scores VALUES ({}, {}, {});".format(name, score, date.today())
    create_entries = """INSERT INTO scores (name, score, date) VALUES ('{}', {}, '{}');""".format(player, score, date.today())
    execute_query(connection, create_entries)

def create_score_table(connection):
    create_score_table = """
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        score INTEGER NOT NULL,
        date DATE
    );
    """
    execute_query(connection, create_score_table)

def show_table(connection):
    select_scores = "SELECT * from scores"
    scores = execute_read_query(connection, select_scores)

    for score in scores:
        print(score)

def show_top_ten(connection):
    query = "SELECT name, score, date from scores ORDER BY score ASC, date DESC LIMIT 10"
    top_ten = execute_read_query(connection, query)
    return top_ten

# connection = create_connection("leader_board.db")
# create_score_table(connection)


# add_entry(connection, 'Lei', 5)
# add_entry(connection, 'Joshua', 77)
# add_entry(connection, 'Cathy', 13)
# add_entry(connection, 'Melody', 99)
# add_entry(connection, 'Frank', 50)
# add_entry(connection, 'Jonathan', 18)
# add_entry(connection, 'Papa', 1)
# add_entry(connection, 'Baby Shark', 3)
# add_entry(connection, 'PeePeePooPoo Man', 40)
# add_entry(connection, 'Ben', 13)
# add_entry(connection, 'Jason', 11)
# add_entry(connection, 'Tim', 22)
# add_entry(connection, 'Greg', 10)

# delete_all_records()



# show_top_ten(connection)
