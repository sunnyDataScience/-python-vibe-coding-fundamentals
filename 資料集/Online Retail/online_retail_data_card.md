# 數據卡：Online Retail Dataset

**1. 數據集總覽**
- **數據來源**: `online_retail_merged.csv`
- **最後更新時間**: 2025-12-26
- **數據維度**: 1,067,371 行 x 8 列

**2. 數據列詳解**

| Column Name | Data Type | Missing % | Unique Values | Description | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `InvoiceNo` | object | 0.0% | 53628 | 發票編號 (若以 'C' 開頭表示取消) | `489434` |
| `StockCode` | object | 0.0% | 5305 | 產品代碼 | `85048` |
| `Description` | object | 0.4% | 5698 | 產品名稱/描述 | `15CM CHRISTMAS GLASS BALL 20 LIGHTS` |
| `Quantity` | int64 | 0.0% | 1057 | 交易數量 (負數表示退貨) | `12` |
| `InvoiceDate` | object | 0.0% | 47635 | 發票日期與時間 | `12/1/2009 7:45` |
| `UnitPrice` | float64 | 0.0% | 2807 | 單價 (英鎊) | `6.95` |
| `CustomerID` | float64 | 22.8% | 5942 | 客戶編號 | `13085.0` |
| `Country` | object | 0.0% | 43 | 客戶所在國家 | `United Kingdom` |

**3. 初步數據品質評估**
- **缺失值**: 以下欄位包含缺失值: Description, CustomerID。特別是 `Description` 或 `CustomerID` 可能影響分析。
- **異常值/特殊業務邏輯**: `Quantity` 包含負值，通常代表退貨或取消訂單，需在總量分析時特別注意。
- **異常值**: `UnitPrice` 包含 0 或負值，可能是贈品、壞帳調整或數據錄入錯誤。

**4. 探索性分析建議**
1.  **RFM 模型分析**: 利用 `CustomerID`, `InvoiceDate`, `UnitPrice` * `Quantity` 進行 Recency, Frequency, Monetary 分析，識別高價值客戶。
2.  **銷售趨勢分析**: 觀察按月/週/日的銷售趨勢，識別季節性波動 (例如聖誕節前的銷量)。
3.  **產品關聯分析 (購物籃分析)**: 分析同一 `InvoiceNo` 中常一起被購買的 `StockCode`，挖掘關聯規則。
4.  **退貨分析**: 深入分析 `Quantity` 為負的交易特徵，找出高退貨率的產品或客戶。
