import scraper
import filter
import notifier

### メイン処理 ###
url = "https://news.yahoo.co.jp/categories/it"

res = scraper.get_web_info(url) # web情報取得

if res is not None:
    df = scraper.extract_web_info(res)  # web情報抽出
    df = filter.keyword_filter(df)      # キーワードフィルタ
    df = filter.deduplication(df)       # 過去記事重複排除

    if df.empty:
        print("取得件数0件。処理終了。")
    else:
        notifier.output_csv(df)             # csv出力 & メール通知
        print("ニュース情報取得成功。")

else:
    print("ニュース情報取得失敗。")