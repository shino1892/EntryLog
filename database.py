import sqlite3
import os
from config import DB_PATH

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        idm TEXT NOT NULL PRIMARY KEY,
        num INTEGER NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
        num INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        PRIMARY KEY (num, timestamp)
    )''')

    conn.commit()
    conn.close()

def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("データベースを削除しました。")
    else:
        print("データベースは存在しません。")
    init_db()
    print("データベースを初期化しました。")

def reset_attendance_table():
    """'attendance'テーブルのすべてのレコードを削除する"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM attendance")
        conn.commit()
        print("出席記録テーブルを初期化しました。")
    except Exception as e:
        print(f"エラー: 出席記録テーブルの初期化に失敗しました - {e}")
    finally:
        conn.close()

def get_user_by_idm(idm):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT num FROM users WHERE idm = ?", (idm,))
    result = cursor.fetchone()
    conn.close()
    return result

def add_attendance(num, timestamp):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO attendance (num, timestamp) VALUES (?, ?)", (num, timestamp))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def register_user(idm, num):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (idm, num) VALUES (?, ?)", (idm, num))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idm, num FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_all_attendance():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT users.num, attendance.timestamp
                      FROM attendance
                      JOIN users ON attendance.num = users.num
                      ORDER BY attendance.timestamp DESC''')
    records = cursor.fetchall()
    conn.close()
    return records

def get_attendance_summary():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = '''
        SELECT num, MIN(timestamp), MAX(timestamp) 
        FROM attendance
        GROUP BY num
    '''
    cursor.execute(query)
    records = cursor.fetchall()
    conn.close()
    return records
