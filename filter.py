import pandas as pd
import os
import json
import glob

# キーワードフィルタ機能関数
def keyword_filter(df):
    # フィルタリングするキーワード取得
    file_path = os.path.join(os.getcwd(), "setting.json")
    f = open(file_path, 'r', encoding="utf-8")
    js_data = json.load(f)

    # キーワードが未入力の場合はフィルタ機能をスキップ
    if js_data['filter'] != "":
        df = df[df["タイトル"].str.contains(js_data["filter"], na=False)]

    return df

# 重複排除機能関数
def deduplication(df):
    # 過去記事を取得
    folder_path = os.path.join(os.getcwd(), "output")
    
    files = glob.glob(folder_path + "/*.csv")

    if len(files) != 0:
        df_old = None
        for file in files:
            if df_old is not None:
                df_old = pd.concat([df_old, pd.read_csv(file)])
            else:
                df_old = pd.read_csv(file)

        # 過去記事と重複する場合は削除
        df = df[~df["URL"].isin(df_old["URL"])]

    return df