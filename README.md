# EntryLog - Felica Attendance System

Felica カード（学生証など）を使用して出席管理を行う Python ベースのシステムです。
Raspberry Pi zero 2w 等のデバイスに PaSoRi（Felica リーダー）を接続して動作させることを想定しています。
記録されたデータは SQLite データベースに保存され、Google スプレッドシートへ同期することが可能です。

## 機能

- **出席記録**: Felica カードをタッチするだけで出席時刻を記録。
- **ユーザー登録**: 新しいカードをスキャンし、学生番号と紐付けて登録。
- **Google スプレッドシート連携**: 出席データをクラウド上のスプレッドシートに自動反映。
- **サーバー連携**: 出席ログやカード登録情報を外部サーバーへ送信（API 連携）。
- **ローカル DB**: SQLite を使用した堅牢なデータ管理。
- **音声フィードバック**: 操作成功時やエラー時にブザー音で通知。

## 必要要件

### ハードウェア

- Raspberry Pi zero 2w(または互換性のある Linux デバイス)
- Sony PaSoRi (RC-S380) - Felica リーダー
- Grove Base Hat & Grove Buzzer (オプション: 音声通知用)

### ソフトウェア

- Python 3.12.3
- `libpafe` (Felica 制御用 C ライブラリ)
- Google Cloud Platform サービスアカウント (スプレッドシート連携用)

## インストール

1.  **リポジトリのクローン**

    ```bash
    git clone <repository-url>
    cd entry_log
    ```

2.  **依存ライブラリのインストール**

    ```bash
    pip install -r requirements.txt
    ```

3.  **libpafe のセットアップ**
    環境に合わせて `libpafe` をインストールし、ライブラリファイル（`.so` や `.dll`）へのパスを確認してください。

## 設定

プロジェクトルートに `.env` ファイルを作成し、以下の環境変数を設定してください。

```ini
DB_PATH=attendance.db
LIBPAFE_PATH=/usr/local/lib/libpafe.so
GOOGLE_JSON_PATH=service_account.json
GOOGLE_SHEET_ID=your_google_sheet_id
API_URL=http://your-api-server.com
```

- `DB_PATH`: SQLite データベースの保存先パス。
- `LIBPAFE_PATH`: インストールした `libpafe` ライブラリへのパス。
- `GOOGLE_JSON_PATH`: Google Cloud Console からダウンロードしたサービスアカウントの JSON キーファイルのパス。
- `GOOGLE_SHEET_ID`: 同期先の Google スプレッドシートの ID（URL に含まれる文字列）。
- `API_URL`: 連携先の API サーバーのベース URL。

## 使い方

### メインプログラムの実行

```bash
python main.py
```

起動すると、以下のメニューが表示されます。

1.  **Student Registration Mode**: 学生証（Felica カード）と学生番号を紐付けて登録します。
2.  **Attendance Recording Mode**: 出席記録モードを開始します。カードをかざすと出席時刻が記録されます。
3.  **Exit**: プログラムを終了します。

運用時は、まず `1` を選択してユーザー登録を行い、その後 `2` を選択して出席記録の待機状態にします。

### データの同期

データベースに蓄積された出席データを Google スプレッドシートに送信するには、以下のスクリプトを実行します。

```bash
python sendDBtoSS.py
```

定期的に実行したい場合は、cron などでスケジュール設定することをお勧めします。

## ディレクトリ構造

- `main.py`: アプリケーションのエントリーポイント。
- `database.py`: データベース操作モジュール。
- `felica.py`: Felica カード読み取りモジュール。
- `sendDBtoSS.py`: Google スプレッドシート同期スクリプト。
- `config.py`: 環境変数読み込み設定。
- `debug/`: デバッグ用スクリプト群。
