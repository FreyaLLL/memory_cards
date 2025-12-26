import pandas as pd
import time
import os

excel_path = "/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools/cards.xlsx"
csv_path = "/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools/cards.csv"

last_mtime = 0

while True:
    try:
        mtime = os.path.getmtime(excel_path)
        if mtime != last_mtime:
            last_mtime = mtime
            df = pd.read_excel(excel_path, sheet_name="cards")
            df.to_csv(csv_path, index=False)
            print("CSV 已更新！")
    except Exception as e:
        print("出错:", e)
    time.sleep(5)
