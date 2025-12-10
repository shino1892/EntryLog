import time
import sys
import spidev
from felica import get_felica_idm
import database
from logger_config import error_logger
from grove.gpio import GPIO

# FelicaのIDmを処理
def process_card(idm):
    try:
        result = database.get_user_by_idm(idm)
    except Exception as e:
        error_logger.error("Failed to get user from database.", exc_info=True)
        print("Error: Failed to read from the database.")
        # 音声で致命的なエラーが発生したことを通知「ピーピー」
        buzzer(0.2,2)
        # TODO: LEDを黄色表示
        return

    if result:
        num = result[0]  # 出席番号を取得
        timestamp = time.strftime("%Y-%m-%d %H:%M")
        if database.add_attendance(num, timestamp):
            print(f"Recorded timestamp for student number {num} ({timestamp})") # TODO: 音で通知「ピッ」
            buzzer(0.1,1)
        else:
            print(f"Student number {num} already has an attendance record.")
    else:
        print("Unregistered card. Please register the user first.") # TODO: 音で通知「ピッピッ」
        buzzer(0.1,2)

# ユーザー登録
def register_user_flow():
    idm = ""
    print("Please scan your Felica card.")
    while idm == "" or idm == "0000000000000000":
        try:
            idm = get_felica_idm()
        except Exception as e:
            error_logger.error("Failed to get Felica IDm.", exc_info=True)
            print("Error: Failed to read the card reader. Please check the connection.")
            return # 登録フローを中断してメインメニューに戻る

    while True:
        num_str = input(f"Enter the student number to register (IDm: {idm}): ")
        if num_str.isdigit():
            num = int(num_str)
            break
        else:
            print("Error: Student number must be numeric.")

    try:
        if database.register_user(idm, num):
            print(f"Registered IDm {idm} to student number {num}!")
        else:
            print("This IDm is already registered.")
    except Exception as e:
        error_logger.error("Failed to register user to database.", exc_info=True)
        print("Error: Failed to write to the database.")

def buzzer(time, cnt):
    buzzer = GPIO(5, GPIO.OUT)

    for i in range(cnt):
        buzzer.write(1)
        time.sleep(time)
        buzzer.write(0)
        time.sleep(0.5)

def send_color(r, g, b, brightness):
    r = int(r * brightness)
    g = int(g * brightness)
    b = int(b * brightness)
    prefix = 0xC0 | ((255 - r) >> 2 & 0x30) | ((255 - g) >> 2 & 0x0C) | ((255 - b) >> 2 & 0x03)
    spi.xfer2([prefix, b, g, r] + [0x00]*4)

def led_off():
    r, g, b = 0,0,0
    prefix = 0xC0 | ((255 - r) >> 2 & 0x30) | ((255 - g) >> 2 & 0x0C) | ((255 - b) >> 2 & 0x03)
    spi.xfer2([prefix, b, g, r] + [0x00]*4)

def led_on(r, g, b, time):
    if(time == 0):
        send_color(r, g, b, 0.1)
    else:
        send_color(r, g, b, 0.1)
        time.sleep(time)
        led_off()
    
# メインメニュー
def main_loop(spi):
    try:
        database.init_db()
    except Exception as e:
        error_logger.error("Failed to initialize the database.", exc_info=True)
        print("Fatal error: Could not initialize the database. Exiting program.")
        # 音声でカードリーダーのエラーを通知「ピーピー」
        buzzer(0.2,2)
        # LEDを赤色表示
        led_on(255, 0, 0, 0)
        sys.exit(1)

    while True:
        print("\nAttendance Management System")
        print("1. Student Registration Mode")
        print("2. Attendance Recording Mode")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            register_user_flow()
        elif choice == "2":
            # LEDを緑色表示
            led_on(0, 255, 0, 0)
            print("Please scan your Felica card (Press Ctrl+C to exit)")
            try:
                while True:
                    try:
                        idm = get_felica_idm()
                        if idm != "" and idm != '0000000000000000':
                            process_card(idm)
                            time.sleep(2)
                    except Exception as e:
                        error_logger.error("Failed to get Felica IDm.", exc_info=True)
                        print("\nError: Failed to read the card reader. Retrying in 5 seconds.")
                        # 音声でカードリーダーのエラーを通知「ピッピーー」
                        buzzer(0.1,1)
                        buzzer(0.2,1)
                        # 5秒間を黄色表示
                        led_on(0, 255, 255, 5)
                        time.sleep(5)

            except KeyboardInterrupt:
                print("\nExiting attendance recording mode.")
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid input.")

if __name__ == "__main__":
    try:
        spi = spidev.SpiDev()
        spi.open(0,0)
        spi.max_speed_hz = 1000000
        spe.mode = 0b00
        main_loop(spi)
    except Exception as e:
        # 予期せぬすべてのエラーをここで捕捉
        error_logger.error("An unexpected error occurred. Exiting program.", exc_info=True)
        print("\nAn unexpected error occurred. See error.log for details.")
        print("Exiting program.")
        # TODO: 音声で致命的なエラーが発生したことを通知「ピーピーピーーーー」
        buzzer(0.2,2)
        buzzer(0.5,1)
        # LEDを赤色表示
        led_on(255, 0, 0, 0)
        sys.exit(1)
