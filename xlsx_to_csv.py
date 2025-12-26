import pandas as pd
import os

# 文件路径
cards_path = "/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools/cards.xlsx"
logs_path = "/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools/logs.xlsx"
csv_path = "/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools/cards.csv"

# 阈值
H1 = 0.8  # 根据你的需求修改

try:
    # 读取表格
    cards = pd.read_excel(cards_path)
    logs = pd.read_excel(logs_path)
    
    def calc_level(card_id):
        log_subset = logs[logs['card_id'] == card_id]
        if log_subset.empty:
            return "new"
        elif (log_subset['result'] == "wrong").any():
            return "hard"
        elif log_subset['time'].mean() > H1:
            return "hard"
        else:
            return "ok"
    
    # 更新 level 列
    cards['level'] = cards['id'].apply(calc_level)
    
    # 保存 CSV
    cards.to_csv(csv_path, index=False)
    print("CSV 已刷新！")
    
except Exception as e:
    print("出错:", e)
