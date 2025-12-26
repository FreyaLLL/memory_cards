import pandas as pd
import subprocess
import os

# 文件路径
cards_path = "/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools/cards.xlsx"
logs_path = "/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools/logs.xlsx"
csv_path = "/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools/cards.csv"

# 阈值
H1 = 0.8  # 可根据需求修改

try:
    # 读取表格
    cards = pd.read_excel(cards_path)
    logs = pd.read_excel(logs_path)

    # 计算 level
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

    cards['level'] = cards['id'].apply(calc_level)

    # 保存 CSV
    cards.to_csv(csv_path, index=False)
    print("CSV 已刷新！")

    # Git 操作
    os.chdir("/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools/")
    
    # 添加 CSV
    subprocess.run(["git", "add", "cards.csv"], check=True)

    # 提交（如果没有变化，不会报错）
    try:
        subprocess.run(["git", "commit", "-m", "自动更新 cards.csv"], check=True)
    except subprocess.CalledProcessError:
        print("没有新的更改，无需提交")

    # 拉取远程最新，防止冲突
    subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)

    # 推送
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("CSV 已自动同步到 GitHub！")

except Exception as e:
    print("出错:", e)
