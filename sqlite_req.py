import sqlite3

def main(sql):
    try:
        connection = sqlite3.connect("localsight_db.db")
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return result 
    except Exception as e:
        print(f'{e}')