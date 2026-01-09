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
        i = 0
        for data in df.values:
            if js_data['filter'] not in data[1]:
                df = df.drop(i)

            i += 1

    return df

# 重複排除機能関数
def deduplication(df):
    # 過去記事を取得
    folder_path = os.path.join(os.getcwd(), "output")
    
    files = glob.glob(folder_path + "/*.csv")

    df_old = None
    for file in files:
        if df_old is not None:
            df_old = pd.concat([df_old, pd.read_csv(file)])
        else:
            df_old = pd.read_csv(file)

    # 過去記事と重複する場合は削除
    i = 0
    for data in df.values:
        for data_old in df_old.values:
            if data[1] == data_old[1]:
                df = df.drop(i)
                break

        i += 1

    return df