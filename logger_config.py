import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = 'error.log'

def setup_logger():
    # ロガーの作成
    logger = logging.getLogger('attendance_system')
    logger.setLevel(logging.ERROR)

    # ログのフォーマットを定義
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
        'Traceback:\n%(exc_info)s\n' + '-'*80 + '\n'
    )

    # ファイルハンドラの設定 (ログローテーション対応)
    # 1MBごとにファイルを分け、5世代までバックアップを保持
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)

    # ロガーにハンドラを追加
    logger.addHandler(file_handler)

    return logger

# グローバルロガーのインスタンス
error_logger = setup_logger()

