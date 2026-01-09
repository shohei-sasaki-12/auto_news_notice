import datetime
import os
import smtplib
from email.mime.text import MIMEText
import json

# CSV出力関数
def output_csv(df):
   # CSV出力（関数化予定）
    dt_now = datetime.datetime.now()
    file_name = dt_now.strftime('%Y-%m-%d.csv')
    folder_path = os.path.join(os.getcwd(), "output")
    file_path = os.path.join(folder_path, file_name)

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)   # outputフォルダ作成
        
    df.to_csv(file_path, index=False)

    # メール通知
    notice_mail(dt_now, file_name)    

# メール通知関数
def notice_mail(dt_now, file_name):
    # メール通知設定を取得
    file_path = os.path.join(os.getcwd(), "setting.json")
    f = open(file_path, 'r', encoding="utf-8")
    js_data = json.load(f)

    port = 587
    smtp_server = "smtp.gmail.com"
    login = js_data['source_adr']   # SMTPサーバ ログインユーザ名
    password = js_data['password']  # SMTPサーバ ログインパスワード

    sender_email = login                            # 送信元アドレス
    receiver_email = js_data['destination_adr']     # 送信先アドレス

    # プレーンテキストの内容
    text = dt_now.strftime('%Y/%m/%dのニュースを取得しました。\nファイル名：') + file_name

    # MIMETextオブジェクトの作成
    message = MIMEText(text, "plain")
    message["Subject"] = dt_now.strftime('%Y/%m/%d ニュース取得')
    message["From"] = sender_email
    message["To"] = receiver_email

    # メールの送信
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()  # 接続を安全に保つ
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
