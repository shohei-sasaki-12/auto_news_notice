# auto_news_notice（自動ニュース取得・通知ツール）

Yahoo!ニュース（ITカテゴリ）から最新ニュースを取得し、指定キーワードでフィルタした上で
CSV保存し、メールで通知するツールです。

- Webスクレイピング（requests + BeautifulSoup）
- pandasによるデータ整形・重複排除
- CSV出力 + メール通知（SMTP）

---

## 機能

- ニュース一覧ページから記事情報を取得
  - 取得日時 / タイトル / URL / 公開日時
- キーワードフィルタ（setting.json で指定）
- 過去に保存したCSVと比較して重複記事を除外
- 当日分の結果を `output/YYYY-MM-DD.csv` として保存
- 保存完了後にメール通知（Gmail SMTP）

---

## ディレクトリ構成

```
auto_news_notice/
├─ main.py
├─ scraper.py
├─ filter.py
├─ notifier.py
├─ setting.json
└─ output/
   └─ YYYY-MM-DD.csv
```

---

## 必要環境

- Windows（動作確認環境）
- Python 3.10+（推奨）
- ライブラリ
  - requests
  - beautifulsoup4
  - pandas

---

## セットアップ

### 1) ライブラリインストール

```bash
pip install requests beautifulsoup4 pandas
```

### 2) 設定ファイルの編集

`setting.json` を編集します。

```json
{
  "filter": "",
  "source_adr": "",
  "destination_adr": "",
  "password": ""
}
```

- `filter`：タイトルに含まれるキーワード（空文字の場合はフィルタしない）
- `source_adr`：送信元メールアドレス（Gmail想定）
- `destination_adr`：通知先メールアドレス
- `password`：SMTPログイン用パスワード  
  ※ Gmail の場合は「アプリパスワード」を推奨

---

## 使い方（実行方法）

```bash
python main.py
```

実行すると以下を行います。

1. Yahoo!ニュース（IT）からニュースを取得
2. キーワードフィルタ
3. 過去CSVと比較して重複除外
4. `output/` にCSV保存
5. 保存完了メール通知

---

## 出力形式（CSV）

`output/YYYY-MM-DD.csv` が作成されます。

| 取得日時 | タイトル | URL | 公開日時 |
|---|---|---|---|

---

## 注意事項

- 本ツールは学習目的のミニプロジェクトです。
- スクレイピング対象サイトのHTML構造変更により取得できなくなる可能性があります。
- アクセス頻度・利用規約・robots.txt 等に配慮して利用してください。

---

## 今後の改善案

- キーワードを複数指定（AND / OR）できるように拡張
- ログレベル（INFO / WARN / ERROR）の整理
- 定期実行（タスクスケジューラ）対応