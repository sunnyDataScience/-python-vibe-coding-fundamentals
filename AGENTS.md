# AGENTS.md

> AI coding agent 的專案作業說明。Antigravity、Claude Code、Codex、Cursor 都讀這一份。
> `CLAUDE.md` 只是指向本檔的薄封裝，**內容不要重複寫兩份**。

---

## 1. 這是什麼專案

**數據分析教學 repo。** 核心是一套六階段的分析工作流，教學員用 AI 協助完成
「從模糊的商業問題 → 到數字站得住腳的報告 → 到持續監控的儀表板」。

**讀者是學員，不是工程師。** 產出的程式碼以「看得懂、能重跑」為第一優先，
不要用進階語法炫技，不要為了少三行而犧牲可讀性。變數命名與註解用中文沒問題。

---

## 2. 目錄地圖

```
├── 上課用prompt/                # ★ 專案核心：分析 Prompt 武器庫（六階段 00~05）
│   └── 分析師武器庫.md           # ← 總索引，要理解分析流程從這裡讀
├── pandas數據分析工具教學/       # Pandas 講義 + 參考解答 (.ipynb)
├── 資料集/                      # 課程資料集（見第 3 節契約）— 唯讀，不要修改
├── scripts/                     # 可重跑的分析腳本
│   └── visualize_retail.py      # RFM + Cohort 參考實作（見第 7 節）
├── charts/                      # 圖表產出
├── docs/
│   ├── antigravity/             # Antigravity CLI 安裝與 .agents 設定手冊
│   └── course/                  # 延伸閱讀（LLM 工程通則）
└── README.md
```

> 本 repo 原本還有 `python基礎語法/` 入門教材，已於 2026-08 移除，
> 專案核心收斂到數據分析。舊教材保存在 git 歷史 `de2eea0`。

---

## 3. 資料集契約

**動任何分析前先讀這一節。憑印象寫欄位名是本專案最常見的錯誤來源。**

### 3.1 Online Retail（英國禮品電商交易明細）

| 檔案 | 筆數 | 時間範圍 |
| :--- | ---: | :--- |
| `資料集/Online Retail/online_retail_09_10.csv` | 525,461 | 2009-12-01 ~ 2010-12-09 |
| `資料集/Online Retail/online_retail_10_11.csv` | 541,910 | 2010-12-01 ~ 2011-12-09 |

**讀取方式**（兩個檔案都帶 UTF-8 BOM）：

```python
df = pd.read_csv(path, encoding="utf-8-sig")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="%m/%d/%Y %H:%M")
```

> ❌ 不要用 `encoding="ISO-8859-1"`。BOM 會被吃進第一個欄位名，
> 變成 `ï»¿InvoiceNo`，後續 `df["InvoiceNo"]` 直接 `KeyError`。

**欄位**（8 欄，兩檔相同）：

| 欄位 | dtype | 說明與地雷 |
| :--- | :--- | :--- |
| `InvoiceNo` | object | 訂單編號。**`C` 開頭 = 退貨單**（09_10: 10,206 筆／10_11: 9,288 筆） |
| `StockCode` | object | 商品代碼（約 4,000~4,600 種） |
| `Description` | object | 商品名稱，0.27~0.56% 缺失 |
| `Quantity` | int64 | 數量。**退貨為負值**（09_10: 12,326 筆負值／10_11: 10,624 筆） |
| `InvoiceDate` | object | 字串 `M/D/YYYY H:MM`，**需自行轉 datetime** |
| `UnitPrice` | float64 | 單價。**有 `<= 0` 的異常記錄**（09_10: 3,690 筆／10_11: 2,517 筆） |
| `CustomerID` | float64 | 客戶編號。**20.5%(09_10) / 24.9%(10_11) 缺失**，且型別是 float 不是 int |
| `Country` | object | 約 92% 為 United Kingdom，其餘 37~39 國 |

> ⚠️ **欄位命名陷阱**：UCI 官網另一個版本用 `Price` 與 `Customer ID`（有空格）。
> **本專案的 CSV 不是那個版本**，一律是 `UnitPrice` 與 `CustomerID`。

**做客戶分析（RFM / Cohort / 留存）前的標準清洗**，每一步都要在產出中說明理由：

```python
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]   # 剔除退貨單
df = df.dropna(subset=["CustomerID"])                        # 無客戶ID無法歸戶
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]        # 剔除異常量價
df["TotalSum"] = df["Quantity"] * df["UnitPrice"]
```

> ⚠️ 兩個檔案的時間範圍**重疊** 2010-12-01 ~ 2010-12-09，
> 且該區間的資料是**完全重複**的（兩檔各 22,523 筆，內容一致）。
> 直接 `pd.concat` 會讓這 9 天的營收與交易數變成兩倍。
> 合併前必須去重：`df.drop_duplicates(subset=["InvoiceNo","StockCode","Quantity","InvoiceDate","UnitPrice"])`

### 3.2 Taiwan SuperMarket Sales 2025（練習用，含刻意注入的髒資料）

`資料集/SuperMarket_Sales_2025/Taiwan_SuperMarket_Sales_2025_Practice.csv`
1,030 列 × 28 欄，2025-01-01 ~ 2025-03-30（**全部落在 Q1**，`Quarter` 欄無區辨力）。

**這是「資料清洗練習」用的資料集，髒資料是故意的。** 已知問題：

| 問題 | 實測 |
| :--- | :--- |
| 缺失值（多欄） | `Membership_Level` 4.95%、`Rating` 3.88%、`Store_Size` / `Customer type` 3.11%、`Eco_Premium` 2.91%、`Gender` / `Quantity` 2.04%、`Age_Group` / `Is_Promotion` 1.94%、`Unit price` 0.97% |
| 主鍵不唯一 | `Invoice ID` 1,000 個唯一值 / 1,030 列，60 列涉及重複；其中 10 列為完整重複列 |
| 恆定欄位 | `gross margin percentage` 全表只有 `4.76190476` 一個值 |
| 負數量 | `Quantity` 有 5 筆負值（最小 -9） |
| 極端值 | `Quantity` 有 5 筆 > 100（最大 472） |
| **衍生欄位不自洽** | `cogs ≠ Unit price × Quantity`：999 個可比對列中有 **240 列**不符；`Sales ≠ cogs × 1.05` 有 12 列；`Tax 5% ≠ cogs × 0.05` 有 8 列 |

> ⚠️ 因為金額欄彼此矛盾，**做金額分析前必須先選定一個可信來源**（通常用 `Sales`），
> 並在產出中明確寫出「本次分析以 `Sales` 為準，因為 X」。不要默默混用。

**主要維度欄位**：`Branch`(7: 全聯/大潤發/好市多/家樂福/愛買/楓康/美廉社)、
`City`(6 都)、`Product line`(6)、`Payment`(3: 現金/信用卡/電子支付)、
`Membership_Level`(5)、`Age_Group`(6)、`Shopping_Period`(5: 早晨/午餐/下午/晚餐/夜間)、
`Store_Size`(3)、`Month_Name`(中文「一月/二月/三月」)。
`Is_Weekend` / `Is_Holiday_Season` 是 bool；`Is_Promotion` / `Eco_Premium` 因含 NaN 而是 object。

---

## 4. 分析工作鐵律

這是本專案最重要的一節。**違反這幾條的產出一律視為未完成。**

### 4.1 數字不得杜撰

- 報告、數據卡、洞察裡出現的**每一個數字**，都必須是你**實際跑程式碼算出來**的。
- 不准從資料集的公開描述、記憶、或「常見的量級」推估。
- 不確定就直接說不確定，或去把它算出來。**寫一個看起來合理的數字是最嚴重的錯誤。**
- `04報告呈現/分析報告製作.md` 模板裡的百分比（15%、40%、60%、75%）**全部是佔位符**，
  絕對不可以原樣保留，也不可以改成另一個沒算過的數字。

### 4.2 每個結論都要可重跑

- 分析程式碼存成檔案（見第 5 節），不要只在對話裡跑完就丟。
- 腳本要能從乾淨環境重跑並得到相同結果：不依賴手動步驟、不依賴已存在的中間檔。
- 報告中的關鍵數字，要能指出是哪支腳本的哪一段算出來的。

### 4.3 清洗決策要寫出來，不要默默做掉

每一次 `dropna` / 過濾 / 填補，都要記錄：**剔除了多少列（絕對數 + 佔比）、為什麼、對結論有什麼影響**。

```python
before = len(df)
df = df.dropna(subset=["CustomerID"])
print(f"剔除無 CustomerID：{before - len(df):,} 列 ({(before-len(df))/before:.1%})")
```

樣本從 52 萬掉到 40 萬卻沒人提，是分析報告最常見的隱形謊言。

### 4.4 先看資料，再談結論

拿到新問題的順序永遠是：**讀 AGENTS.md 契約 → 實際載入看一眼 → 才開始寫分析**。
不要憑欄位名猜語意，尤其是第 3.2 節那些互相矛盾的金額欄。

### 4.5 統計主張要誠實

- 相關不等於因果。用「與 X 相關」，不要寫「X 導致 Y」，除非真的做了因果設計。
- 小樣本分群要標註每群的 n。1,030 列切 6×7 個交叉組合後，每格可能只剩個位數。
- 報漲跌幅時同時給基期絕對值。「成長 200%」從 2 變 6 沒有意義。

---

## 5. 產出慣例

分析產物放在專案根目錄的這三個資料夾（不存在就建立）：

```
reports/     # Markdown 產出：數據卡、分析報告、驗算紀錄
charts/      # 圖檔 (.png)
scripts/     # 可重跑的分析腳本 (.py)
```

命名：`reports/data_card_online_retail.md`、`scripts/rfm_online_retail.py`、
`charts/rfm_bubble.png` — 全小寫、底線分隔、帶上資料集名稱。

**不要修改 `資料集/` 底下的原始檔案。** 清洗後的資料另存到 `reports/` 或 `scripts/` 旁邊的
輸出路徑，原始資料保持唯讀。

---

## 6. 執行環境

- Python 3.10、pandas 2.3、matplotlib 3.10、seaborn 0.13、plotly 6.8（已安裝，可直接用）
- 平台為 **Linux**。路徑一律用 `pathlib.Path` 搭配**相對於專案根目錄**的相對路徑，
  不要寫死 `d:\...` 這類 Windows 絕對路徑。

**matplotlib 中文字型**（不設定的話中文全部變成豆腐方塊）：

```python
plt.rcParams["font.sans-serif"] = ["Noto Sans CJK TC"]   # 本機實際可用的中文字型
plt.rcParams["axes.unicode_minus"] = False
```

> ❌ 不要用 `Microsoft JhengHei` / `SimHei` — 那是 Windows 字型，本機沒有。

---

## 7. 參考實作：`scripts/visualize_retail.py`

**這支腳本是本專案的程式碼範本。** 寫新的分析腳本時照它的結構走。

```bash
python scripts/visualize_retail.py     # 從專案根目錄或任何目錄執行皆可
```

它示範了本檔要求的每一件事：

| 規範 | 在腳本中的做法 |
| :--- | :--- |
| 路徑不寫死 | `PROJECT_ROOT = Path(__file__).resolve().parent.parent`，從任何 cwd 執行都對 |
| 正確讀檔 | `encoding="utf-8-sig"`，並用 `DEDUP_KEYS` 處理兩檔重疊期的重複交易 |
| 清洗留紀錄 | `clean_for_customer_analysis()` 印出每一步的剔除列數、佔比、理由與最終保留率 |
| 交付前驗證 | `verify_rfm()` 用 `assert` 檢查分群完整性、營收加總、並以第二種算法交叉驗算 |
| 中文字型 | `setup_chinese_font()` 依序疊上系統實際安裝的字型，讓 matplotlib 逐字後備 |
| 產出落地 | 圖存到 `charts/`，腳本放 `scripts/`，原始資料唯讀 |

> 💡 字型那段有個容易踩的坑：`Droid Sans Fallback` 有中文但**沒有英文與數字**，
> 單獨指定它會讓座標軸數字整排消失。所以要給的是一整串後備清單，不是單一字型名。

**歷史備註**：這支腳本原本放在專案根目錄且無法執行（寫死 Windows 絕對路徑、
讀取不存在的 `online_retail_merged.csv`、用 `ISO-8859-1` 讀 BOM 檔導致首欄名損壞、
指定 Linux 上不存在的 `Microsoft JhengHei`）。已於 2026-08 重寫並移入 `scripts/`。

---

## 8. 與 Prompt 武器庫的關係

`上課用prompt/` 那六個階段是**給人用的教學模板**，本檔是**給你（agent）用的工作規範**。
當使用者說「用階段 02+ 幫我跑分析」時：

1. 讀 `上課用prompt/分析師武器庫.md` 找到對應階段的檔案
2. 照該檔的〈模式 B：AI Coding〉指令執行
3. 全程遵守本檔第 4 節的鐵律與第 5 節的產出慣例

模板與本檔衝突時，**以本檔為準**（模板是為聊天視窗寫的，有些假設在 agent 環境不成立）。
