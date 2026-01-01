import pandas as pd
import subprocess
import os
import sys

# ======================
# 路径配置
# ======================
BASE_DIR = "/Users/wanglingli/Library/Mobile Documents/com~apple~CloudDocs/myTools"

CARDS_XLSX = f"{BASE_DIR}/cards.xlsx"
CARDS_CSV  = f"{BASE_DIR}/cards.csv"

def run(cmd):
    subprocess.run(cmd, check=True)

try:
    # ======================
    # Git：先同步
    # ======================
    print("🔄 同步远端仓库")
    os.chdir(BASE_DIR)
    run(["git", "pull", "--rebase", "origin", "main"])

    # ======================
    # 读取 Excel
    # ======================
    print("📖 读取 cards.xlsx")
    cards = pd.read_excel(CARDS_XLSX)
    cards.columns = cards.columns.str.strip()

    # ======================
    # 清洗数据
    # ======================
    print("🧹 清洗数据")

    def clean(x):
        return str(x).strip() if pd.notna(x) else ""

    for col in ["front", "back", "tag", "group"]:
        cards[col] = cards[col].apply(clean)

    # 丢弃无效卡片
    cards = cards[(cards["front"] != "") & (cards["back"] != "")].copy()

    # ======================
    # 重建 id（核心）
    # ======================
    print("🔢 重建连续 id")
    cards = cards.reset_index(drop=True)
    cards["id"] = range(1, len(cards) + 1)

    # 如果没有 level 列，才初始化为 new
    if "level" not in cards.columns:
        cards["level"] = "new"


    # ======================
    # 固定列顺序
    # ======================
    cards = cards[["id", "front", "back", "tag", "level", "group"]]

    # ======================
    # 导出 CSV
    # ======================
    cards.to_csv(CARDS_CSV, index=False, encoding="utf-8")
    print(f"✅ 生成 cards.csv")

    # ======================
    # Git：提交 & 推送
    # ======================
    run(["git", "add", "cards.csv"])

    try:
        run(["git", "commit", "-m", "更新 cards.csv（来自 cards.xlsx）"])
    except subprocess.CalledProcessError:
        print("ℹ️ 无变化，跳过 commit")

    run(["git", "push", "origin", "main"])
    print("🚀 已推送到 GitHub")

    print("🎉 A 脚本完成")

except Exception as e:
    print("❌ 出错：", e)
    sys.exit(1)
