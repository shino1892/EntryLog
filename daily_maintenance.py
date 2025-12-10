import os
import shutil
import datetime
import database
from config import DB_PATH

BACKUP_FOLDER = 'backups'

def run_daily_maintenance():
    """Perform database backup and reset attendance records"""
    print("Starting daily maintenance...")

    # 1. データベースのバックアップ
    try:
        # バックアップフォルダが存在しない場合は作成
        os.makedirs(BACKUP_FOLDER, exist_ok=True)

        # バックアップファイル名の生成
        date_str = datetime.date.today().strftime('%Y-%m-%d')
        backup_filename = f'attendance_{date_str}.db'
        backup_path = os.path.join(BACKUP_FOLDER, backup_filename)

        if not os.path.exists(DB_PATH):
            print(f"Error: Database file '{DB_PATH}' not found. Skipping backup.")
        else:
            shutil.copy2(DB_PATH, backup_path)
            print(f"Database backed up to '{backup_path}'.")
    except Exception as e:
        print(f"Error: Failed to back up database - {e}")

    # 2. 出席記録テーブルの初期化
    database.reset_attendance_table()

    print("Daily maintenance completed.")

if __name__ == "__main__":
    run_daily_maintenance()
