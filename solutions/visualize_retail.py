"""Online Retail 資料集：RFM 分群 + Cohort 留存分析視覺化。

⚠️ 這是【參考解答】—— 對應商業場景模擬案例的「案例一：尋找沈睡的鯨魚」。
   建議先自己走完階段 02+（`上課用prompt/02數據分析/分析執行_AI_Coding.md`），
   卡住或做完之後再回來對照。詳見 solutions/README.md。

它同時是本專案的**程式碼範本**，示範一條完整的路徑：
    資料集/ → 分析腳本 → 圖表產出

執行方式（在專案根目錄）：
    python solutions/visualize_retail.py

產出：
    solutions/charts/rfm_bubble_chart.png   VIP 流失風險分佈圖
    solutions/charts/cohort_heatmap.png     同類群組留存率熱力圖

本腳本刻意遵守 AGENTS.md 第 4 節的分析鐵律：
    - 每一步清洗都印出影響列數與佔比（不做隱形的資料裁切）
    - 產圖前先自我驗證（分群完整性、金額加總）
    - 路徑一律相對於專案根目錄，可從任何工作目錄執行

注意：你自己寫的分析腳本應該放在 `scripts/`、圖表存到 `charts/`
（AGENTS.md 第 5 節的慣例）。本檔放在 solutions/ 是因為它是解答，不是通例。
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 無 GUI 環境（CI、遠端主機）也能存圖

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# --- 路徑設定：一律從腳本位置往上推導專案根目錄，不寫死絕對路徑 ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "資料集" / "Online Retail"
CHART_DIR = SCRIPT_DIR / "charts"   # 解答的圖表跟解答放一起，不污染學員的 charts/

# 兩個年度檔在 2010-12-01~12-09 完全重複，合併時用這組欄位去重（見 AGENTS.md 第 3.1 節）
DEDUP_KEYS = ["InvoiceNo", "StockCode", "Quantity", "InvoiceDate", "UnitPrice"]

# 流失風險的判定門檻
RECENCY_RISK_DAYS = 90  # 超過這麼多天沒回購視為高風險
FREQUENT_ORDERS = 5     # 訂單數超過這個值視為高頻客戶


def setup_chinese_font() -> None:
    """設定中文字型，避免圖表中文變成豆腐方塊。

    這裡不是「挑一個」而是「把所有裝得到的候選依序排好」：
    matplotlib 會逐字往後找，前面的字型缺某個字時自動用後面的補。
    例如 Droid Sans Fallback 有中文但**沒有英文與數字**，
    單獨使用會讓座標軸數字消失 — 放在清單最後當補漏用剛好。
    """
    candidates = [
        "Noto Sans CJK TC",      # Linux（繁體優先）
        "Noto Sans CJK SC",
        "Noto Sans CJK JP",      # 同一套 Noto CJK，含完整漢字
        "Microsoft JhengHei",    # Windows
        "PingFang TC",           # macOS
        "Heiti TC",
        "WenQuanYi Zen Hei",
        "Droid Sans Fallback",   # 最後的補漏（缺英數，不可單獨使用）
    ]
    installed = {f.name for f in fm.fontManager.ttflist}
    available = [name for name in candidates if name in installed]

    if not available:
        print("[字型] ⚠️ 找不到任何中文字型，圖表中文會顯示為方塊")
        return

    plt.rcParams["font.sans-serif"] = available + plt.rcParams["font.sans-serif"]
    plt.rcParams["axes.unicode_minus"] = False
    print(f"[字型] 主要使用 {available[0]}"
          + (f"（備援：{', '.join(available[1:])}）" if len(available) > 1 else ""))


def load_retail_data() -> pd.DataFrame:
    """讀取兩個年度檔並合併去重。

    注意 encoding 必須是 utf-8-sig：檔案帶 UTF-8 BOM，
    用 ISO-8859-1 讀會讓第一個欄位名變成 'ï»¿InvoiceNo'，後續取欄位直接 KeyError。
    """
    frames = []
    for csv_path in sorted(DATA_DIR.glob("online_retail_*.csv")):
        part = pd.read_csv(csv_path, encoding="utf-8-sig")
        print(f"[載入] {csv_path.name}: {len(part):,} 列")
        frames.append(part)

    if not frames:
        raise FileNotFoundError(f"在 {DATA_DIR} 找不到 online_retail_*.csv")

    merged = pd.concat(frames, ignore_index=True)
    before = len(merged)
    merged = merged.drop_duplicates(subset=DEDUP_KEYS)
    print(f"[合併] {before:,} 列 → 去重後 {len(merged):,} 列 "
          f"（移除重疊期間的 {before - len(merged):,} 筆重複交易）")

    merged["InvoiceDate"] = pd.to_datetime(merged["InvoiceDate"], format="%m/%d/%Y %H:%M")
    return merged


def clean_for_customer_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """做客戶層級分析前的標準清洗，並印出每一步的影響。

    樣本量在清洗中大幅縮水卻沒人提，是分析報告最常見的隱形謊言 —
    所以這裡把每一刀都攤開來講。
    """
    original = len(df)
    log = []

    def record(step: str, cleaned: pd.DataFrame, reason: str) -> pd.DataFrame:
        removed = len(df_state[0]) - len(cleaned)
        log.append((step, removed, removed / original, len(cleaned), reason))
        df_state[0] = cleaned
        return cleaned

    df_state = [df]

    step1 = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
    record("剔除退貨單 (InvoiceNo 以 C 開頭)", step1, "退貨非有效消費，會扭曲 Frequency")

    step2 = step1.dropna(subset=["CustomerID"])
    record("剔除 CustomerID 缺失", step2, "無客戶編號無法歸戶到個人")

    step3 = step2[(step2["Quantity"] > 0) & (step2["UnitPrice"] > 0)]
    clean = record("剔除非正數的量或價", step3, "0 或負值多為調整分錄，非真實交易")

    print("\n[清洗紀錄]")
    print(f"{'步驟':<34}{'剔除':>10}{'佔原始':>9}{'剩餘':>11}  理由")
    print(f"{'原始資料':<34}{'-':>10}{'-':>9}{original:>11,}  -")
    for step, removed, pct, remaining, reason in log:
        print(f"{step:<34}{removed:>10,}{pct:>8.1%}{remaining:>11,}  {reason}")

    retained = len(clean) / original
    print(f"\n[樣本影響] 清洗後保留原始資料的 {retained:.1%}"
          f"（{original:,} → {len(clean):,} 列）")
    if retained < 0.7:
        print("           ⚠️ 已剔除超過三成資料，解讀結論時務必說明此限制")

    clean = clean.copy()
    clean["TotalSum"] = clean["Quantity"] * clean["UnitPrice"]
    return clean


def build_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """計算每位客戶的 Recency / Frequency / Monetary。"""
    # 以資料集最後一筆交易的隔天當作觀測基準日
    snapshot = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    print(f"\n[RFM] 觀測基準日：{snapshot:%Y-%m-%d}")

    rfm = df.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda s: (snapshot - s.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("TotalSum", "sum"),
    )
    print(f"[RFM] 共 {len(rfm):,} 位客戶")
    return rfm


def classify_segment(row: pd.Series) -> str:
    """依 Recency / Frequency 把客戶分成三群。"""
    is_frequent = row["Frequency"] > FREQUENT_ORDERS
    is_dormant = row["Recency"] > RECENCY_RISK_DAYS

    if is_frequent and is_dormant:
        return "高風險流失"
    if is_frequent and not is_dormant:
        return "活躍留存"
    return "一般客戶"


def verify_rfm(df: pd.DataFrame, rfm: pd.DataFrame) -> None:
    """交付前的自我驗證：對不起來就直接讓程式失敗，不要默默出圖。"""
    print("\n[自我驗證]")

    expected_customers = df["CustomerID"].nunique()
    assert len(rfm) == expected_customers, "RFM 客戶數與清洗後資料不符"
    print(f"  分群完整性：RFM {len(rfm):,} 位 = 清洗後 {expected_customers:,} 位 ✅")

    diff = abs(rfm["Monetary"].sum() - df["TotalSum"].sum())
    assert diff < 0.01, f"營收加總不符，差異 {diff}"
    print(f"  營收加總：RFM 合計 {rfm['Monetary'].sum():,.0f} = 明細合計 ✅")

    # 交叉驗算：用另一種算法重算高風險客群人數
    by_apply = (rfm["Segment"] == "高風險流失").sum()
    by_filter = len(rfm[(rfm["Frequency"] > FREQUENT_ORDERS)
                        & (rfm["Recency"] > RECENCY_RISK_DAYS)])
    assert by_apply == by_filter, "兩種算法的高風險人數不一致"
    print(f"  交叉驗算：高風險客群 {by_apply:,} 位（兩種算法一致）✅")


def plot_rfm_bubble(rfm: pd.DataFrame, output: Path) -> None:
    """RFM 泡泡圖：X=未回購天數、Y=消費頻率、泡泡大小=消費金額。"""
    palette = {"高風險流失": "#d62728", "活躍留存": "#2ca02c", "一般客戶": "#b0b0b0"}
    sizes = rfm["Monetary"] / rfm["Monetary"].max() * 1000 + 10

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(
        rfm["Recency"], rfm["Frequency"],
        s=sizes, c=rfm["Segment"].map(palette),
        alpha=0.5, edgecolors="w",
    )

    at_risk = rfm[rfm["Segment"] == "高風險流失"]
    revenue_share = at_risk["Monetary"].sum() / rfm["Monetary"].sum()

    # 主標題直接講結論，副標題才說明圖怎麼看（圖表選型.md 的建議做法）
    fig.suptitle(
        f"高風險流失客群：{len(at_risk):,} 位客戶，佔歷史營收 {revenue_share:.1%}",
        fontsize=16, fontweight="bold",
    )
    ax.set_title(
        "VIP 流失風險分佈圖（泡泡大小 = 累計消費金額）",
        fontsize=11, color="#555555", pad=10,
    )
    ax.set_xlabel("未回購天數 (Recency)　→ 越右邊越久沒回來", fontsize=12)
    ax.set_ylabel("消費頻率 (Frequency)　→ 越上面買越多次", fontsize=12)

    ax.axvline(x=RECENCY_RISK_DAYS, color="k", linestyle="--", alpha=0.4)
    ax.axhline(y=FREQUENT_ORDERS, color="k", linestyle="--", alpha=0.4)
    ax.text(RECENCY_RISK_DAYS + 10, 92, f"高風險流失區\n(>{RECENCY_RISK_DAYS}天未回購且高頻)",
            color=palette["高風險流失"], fontsize=11)
    ax.text(10, 92, "活躍留存區", color=palette["活躍留存"], fontsize=11)
    # 這條標註落在密集的灰色點帶裡，加白底才看得清楚
    ax.text(200, 2.2, f"一般客戶（訂單數 ≤ {FREQUENT_ORDERS}）",
            color="#606060", fontsize=10,
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=2))

    # 限制軸範圍以維持可讀性（少數極端值會壓縮主要分佈）
    ax.set_xlim(0, 400)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)
    fig.tight_layout(rect=(0, 0, 1, 0.96))  # 留出 suptitle 的空間，避免與副標題重疊
    fig.savefig(output, dpi=100)
    plt.close(fig)
    print(f"  已存檔 {output.relative_to(PROJECT_ROOT)}")


def build_cohort_retention(df: pd.DataFrame) -> pd.DataFrame:
    """依「首次購買月份」分群，計算各群後續每個月的留存率 (%)。"""
    data = df.copy()
    data["InvoiceMonth"] = data["InvoiceDate"].dt.to_period("M")
    data["CohortMonth"] = data.groupby("CustomerID")["InvoiceMonth"].transform("min")
    # CohortIndex = 1 代表獲客當月，2 代表次月，依此類推
    data["CohortIndex"] = (
        (data["InvoiceMonth"] - data["CohortMonth"]).apply(lambda x: x.n) + 1
    )

    counts = data.pivot_table(
        index="CohortMonth", columns="CohortIndex",
        values="CustomerID", aggfunc="nunique",
    )
    cohort_sizes = counts.iloc[:, 0]

    # 驗證：每位客戶只屬於一個 cohort，各 cohort 首月人數加總應等於總客戶數
    assert cohort_sizes.sum() == df["CustomerID"].nunique(), "Cohort 人數加總不符"
    print(f"  Cohort 完整性：{len(counts)} 個獲客月份，人數加總 = 總客戶數 ✅")

    retention = counts.divide(cohort_sizes, axis=0) * 100
    retention.index = retention.index.astype(str)
    return retention


def plot_cohort_heatmap(retention: pd.DataFrame, output: Path) -> None:
    """留存率熱力圖：一列一個獲客月份，一欄一個生命週期月數。"""
    plt.figure(figsize=(16, 9))
    sns.heatmap(
        retention, annot=True, fmt=".0f", vmin=0, vmax=50,
        cmap="Blues", annot_kws={"size": 7}, cbar_kws={"label": "留存率 (%)"},
    )
    plt.title("同類群組留存率熱力圖 (Cohort Analysis)", fontsize=16)
    plt.ylabel("獲客月份", fontsize=12)
    plt.xlabel("第幾個月（1 = 獲客當月）", fontsize=12)
    plt.tight_layout()
    plt.savefig(output, dpi=100)
    plt.close()
    print(f"  已存檔 {output.relative_to(PROJECT_ROOT)}")


def main() -> None:
    setup_chinese_font()
    CHART_DIR.mkdir(exist_ok=True)

    df = load_retail_data()
    df_clean = clean_for_customer_analysis(df)

    rfm = build_rfm(df_clean)
    rfm["Segment"] = rfm.apply(classify_segment, axis=1)
    verify_rfm(df_clean, rfm)

    print("\n[產圖]")
    plot_rfm_bubble(rfm, CHART_DIR / "rfm_bubble_chart.png")
    retention = build_cohort_retention(df_clean)
    plot_cohort_heatmap(retention, CHART_DIR / "cohort_heatmap.png")

    print("\n[客群摘要]")
    summary = rfm.groupby("Segment").agg(
        客戶數=("Monetary", "size"),
        平均未回購天數=("Recency", "mean"),
        營收合計=("Monetary", "sum"),
    )
    summary["營收佔比"] = (summary["營收合計"] / summary["營收合計"].sum() * 100).round(1)
    summary["平均未回購天數"] = summary["平均未回購天數"].round(1)
    summary["營收合計"] = summary["營收合計"].round(0)
    print(summary.to_string(formatters={
        "客戶數": lambda x: f"{x:,}",
        "營收合計": lambda x: f"{x:,.0f}",
        "營收佔比": lambda x: f"{x:.1f}%",
    }))


if __name__ == "__main__":
    main()
