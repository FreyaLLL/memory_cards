import pandas as pd
import os
from datetime import datetime

# 路径配置
CARDS_FILE = "/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools/cards.csv"
LOGS_FILE = "/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools/logs.csv"
BACKUP_DIR = "/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools/backups"

os.makedirs(BACKUP_DIR, exist_ok=True)

# 备份 cards.csv
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(BACKUP_DIR, f"cards_backup_{timestamp}.csv")
pd.read_csv(CARDS_FILE).to_csv(backup_file, index=False)
print(f"已备份 cards.csv 到 {backup_file}")

# 读取 CSV
cards = pd.read_csv(CARDS_FILE)
logs = pd.read_csv(LOGS_FILE)

# 确保 time 是 datetime 类型
logs["time"] = pd.to_datetime(logs["time"], errors="coerce")

# 使用最后一次练习结果更新卡片的 level
last_logs = logs.sort_values("time").drop_duplicates("card_id", keep="last")

# 更新 cards 的 level
cards.set_index("id", inplace=True)
for _, row in last_logs.iterrows():
    card_id = row["card_id"]
    result = row["result"]
    if card_id in cards.index:
        cards.at[card_id, "level"] = result

cards.reset_index(inplace=True)
cards.to_csv(CARDS_FILE, index=False)
print("已根据 logs.csv 更新 cards.csv 的 level 字段！")
