import pandas as pd
import subprocess
import os
import sys

# ======================
# 路径配置
# ======================
BASE_DIR = "/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools"

cards_path = f"{BASE_DIR}/cards.xlsx"
logs_path  = f"{BASE_DIR}/logs.xlsx"
csv_path   = f"{BASE_DIR}/cards.csv"

# ======================
# 参数
# ======================
H1 = 0.8  # 平均时间阈值

def run(cmd):
    subprocess.run(cmd, check=True)

try:
    # ======================
    # Git：先同步
    # ======================
    print("🔄 同步远端仓库（pull --rebase）")
    os.chdir(BASE_DIR)
    run(["git", "pull", "--rebase", "origin", "main"])

    # ======================
    # 读取 Excel
    # ======================
    print("📖 读取 Excel…")
    cards = pd.read_excel(cards_path)
    logs  = pd.read_excel(logs_path)

    cards.columns = cards.columns.str.strip()
    logs.columns  = logs.columns.str.strip()

    # ======================
    # 清洗 cards
    # ======================
    print("🧹 清洗 cards 数据…")

    def clean_str(x):
        return str(x).strip() if pd.notna(x) else ""

    for col in ["front", "back", "tag", "group"]:
        if col in cards.columns:
            cards[col] = cards[col].apply(clean_str)
        else:
            cards[col] = ""

    cards = cards[(cards["front"] != "") & (cards["back"] != "")].copy()

    # ======================
    # 计算 level
    # ======================
    print("🧠 计算 level…")

    if "id" not in cards.columns:
        raise ValueError("cards.xlsx 中缺少 id 列")

    def calc_level(card_id):
        subset = logs[logs["card_id"] == card_id]
        if subset.empty:
            return "new"
        if (subset["result"] == "wrong").any():
            return "hard"
        if subset["time"].mean() > H1:
            return "hard"
        return "ok"

    cards["level"] = cards["id"].apply(calc_level)

    # ======================
    # 重建 id（关键）
    # ======================
    print("🔢 重建连续 id…")
    cards = cards.reset_index(drop=True)
    cards["id"] = range(1, len(cards) + 1)

    # ======================
    # 固定列顺序
    # ======================
    cards = cards[["id", "front", "back", "tag", "level", "group"]]

    # ======================
    # 导出 CSV
    # ======================
    cards.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"✅ CSV 已生成：{csv_path}")

    # ======================
    # Git：提交 & 推送
    # ======================
    print("📦 提交 cards.csv")
    run(["git", "add", "cards.csv"])

    try:
        run(["git", "commit", "-m", "自动清洗并更新 cards.csv"])
    except subprocess.CalledProcessError:
        print("ℹ️ cards.csv 无变化，跳过 commit")

    print("🚀 推送到 GitHub")
    run(["git", "push", "origin", "main"])

    print("🎉 全流程完成")

except Exception as e:
    print("❌ 出错了：", e)
    sys.exit(1)
