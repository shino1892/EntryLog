import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from config import GOOGLE_JSON_PATH, GOOGLE_SHEET_ID
import database

def authenticate_google_sheets():
    """Google Sheets に認証し、クライアントを返す"""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_JSON_PATH, scope)
    return gspread.authorize(creds)

def send_attendance_to_google_sheets(student_number, min_timestamp, max_timestamp, client):
    """出席データを Google スプレッドシートに送信"""
    min_time = datetime.strptime(min_timestamp, "%Y-%m-%d %H:%M")
    max_time = datetime.strptime(max_timestamp, "%Y-%m-%d %H:%M")
    formatted_min_time = min_time.strftime('%H:%M')
    formatted_max_time = max_time.strftime('%H:%M')
    day = int(min_time.strftime('%d'))
    month = int(min_time.strftime('%m'))
    
    sheet_name = f'{month}月'
    sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(sheet_name)
    records = sheet.get_all_values()
    headers = records[0] if records else []
    
    try:
        col_index = headers.index(f"{day}日 (出席)") + 1
        remarks_col_index = col_index + 1
    except ValueError:
        print(f"{day}日 の列が見つかりません")
        return
    
    for i, row in enumerate(records[1:], start=2):
        if row and row[0] == str(student_number):
            if row[col_index]:
                print(f"生徒番号 {student_number} の {day}日 のデータは既に存在します。スキップします。")
                return  
            sheet.update_cell(i, col_index, formatted_min_time)
            if formatted_min_time != formatted_max_time:
                sheet.update_cell(i, remarks_col_index, formatted_max_time)
            return
    
    new_row = [str(student_number)] + [""] * (len(headers) - 1)
    new_row[col_index - 1] = formatted_min_time
    if formatted_min_time != formatted_max_time:
        new_row[col_index] = formatted_max_time
    sheet.append_row(new_row, value_input_option="USER_ENTERED")

def main():
    client = authenticate_google_sheets()
    attendance_data = database.get_attendance_summary()
    for record in attendance_data:
        send_attendance_to_google_sheets(*record, client)

if __name__ == "__main__":
    main()