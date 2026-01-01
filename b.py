import pandas as pd
import os
from datetime import datetime

# ======================
# 路径配置
# ======================
BASE_DIR = "/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools"

CARDS_FILE = f"{BASE_DIR}/cards.csv"
LOGS_FILE  = f"{BASE_DIR}/logs.csv"
BACKUP_DIR = f"{BASE_DIR}/backups"

os.makedirs(BACKUP_DIR, exist_ok=True)

# ======================
# 备份 cards.csv
# ======================
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_path = f"{BACKUP_DIR}/cards_backup_{ts}.csv"
pd.read_csv(CARDS_FILE).to_csv(backup_path, index=False)
print(f"🗂 已备份 cards.csv → {backup_path}")

# ======================
# 读取数据
# ======================
cards = pd.read_csv(CARDS_FILE)
logs  = pd.read_csv(LOGS_FILE)

# 防止列名手滑
cards.columns = cards.columns.str.strip()
logs.columns  = logs.columns.str.strip()

# ======================
# level 计算逻辑（最终版）
# ======================
def calc_level(df):
    if df.empty:
        return "new"
    if (df["result"] == "forget").any():
        return "hard"
    if df["time"].mean() > 1.5:
        return "hard"
    return "ok"

# ======================
# 按 card_id 更新 level
# ======================
cards = cards.set_index("id")

for card_id, group in logs.groupby("card_id"):
    if card_id in cards.index:
        cards.at[card_id, "level"] = calc_level(group)

cards.reset_index(inplace=True)

# ======================
# 写回 cards.csv
# ======================
cards.to_csv(CARDS_FILE, index=False)
print("✅ 已根据 logs.csv 更新 level")

print("🎉 学习状态更新完成（B 脚本）")
