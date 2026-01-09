import requests
from bs4 import BeautifulSoup
import time
import re
import datetime
import pandas as pd

# web情報取得関数
def get_web_info(url):
    ret = None
    retry_num = 3   # リトライ回数
    retry_time = 5  # リトライ間隔
    time_out = 10   # タイムアウト秒数

    try:
        # User-Agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        for i in range(retry_num):
            res = requests.get(url, headers=headers, timeout=time_out)

            if res.status_code == 200:
                ret = res
                break
            else:
                print(f"エラー発生。{retry_time}秒後にリトライします。")
                time.sleep(retry_time)

    except requests.exceptions.RequestException as e:
        print(f"エラー発生。{retry_time}秒後にリトライします。")
        time.sleep(retry_time)

    return ret

# web情報抽出関数
def extract_web_info(res):
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.find_all("li") 

    get_time = []
    title = []
    link = []
    release_time = []
    df = None
    for item in items:
        a = item.find("a", href=re.compile("/news.yahoo.co.jp/pickup/"))

        if not a:
            continue

        # 取得日時
        dt_now = datetime.datetime.now()
        get_time.append(dt_now.strftime('%Y/%m/%d %H:%M'))

        # タイトル
        title.append(a.text)

        # 記事URL
        link.append(a.attrs['href'])

        # 公開日時取得
        release_time_res = get_web_info(a.attrs['href'])
        release_time_res.encoding = "utf-8"
        release_time_soup = BeautifulSoup(release_time_res.text, "html.parser")
        date_str = release_time_soup.find("time").get_text(strip=True)
        date_str = date_str.split("(")[0] + date_str.split(")")[1]  # 曜日を除去
        dt = datetime.datetime.strptime(
            f"{datetime.datetime.now().year}/{date_str}",
            "%Y/%m/%d %H:%M"
        )
        release_time.append(dt.strftime("%Y/%m/%d %H:%M"))

    df = pd.DataFrame({"取得日時":get_time, "タイトル":title, "URL":link, "公開日時":release_time})

    return df
