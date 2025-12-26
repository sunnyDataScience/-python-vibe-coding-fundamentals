# 📊 資料卡
## Taiwan SuperMarket Sales 2025

**一句話描述：** 包含發票編號、日期時間、金額、店鋪、顧客、商品等欄位的表格型交易資料

---

## 基本資訊

- **檔案大小**: 1,000 筆記錄
- **欄位數量**: 28 個欄位
- **時間範圍**: 2025-01-01 至 2025-03-30
- **主要內容**: 每筆記錄包含交易識別碼、時間戳記、金額、店鋪資訊、顧客特徵、商品分類等資訊

---

## 欄位結構

| 欄位名稱 | 資料型態 | 非空值數量 | 唯一值數量 | 備註 |
|---------|---------|-----------|-----------|------|
| **Invoice ID** | String | 1,000 | 1,000 | 無重複值 |
| **Date** | String | 1,000 | 85 | 日期格式 YYYY-MM-DD |
| **Quarter** | String | 1,000 | 1 | 固定值：Q1 |
| **Month_Name** | String | 1,000 | 3 | 三個月份 |
| **Is_Weekend** | Boolean | 1,000 | 2 | True/False |
| **Time** | String | 1,000 | 506 | 時間格式 HH:MM:SS |
| **Shopping_Period** | String | 1,000 | 5 | 5個時段分類 |
| **Store_Name** | String | 1,000 | 67 | 67個不同店鋪 |
| **Branch** | String | 1,000 | 7 | 7個品牌類別 |
| **Store_Size** | String | 1,000 | 3 | 3種規模分類 |
| **City** | String | 1,000 | 6 | 6個城市 |
| **Customer type** | String | 1,000 | 2 | 2種顧客類型 |
| **Membership_Level** | String | 1,000 | 5 | 5個會員等級 |
| **Gender** | String | 1,000 | 2 | 2種性別 |
| **Age_Group** | String | 1,000 | 6 | 6個年齡區間 |
| **Product line** | String | 1,000 | 6 | 6個商品線 |
| **Eco_Premium** | Boolean | 1,000 | 2 | True/False |
| **Unit price** | Float | 1,000 | 989 | 範圍：276.97 - 3,377.28 |
| **Quantity** | Integer | 1,000 | 10 | 範圍：1 - 10 |
| **Tax 5%** | Float | 1,000 | 996 | 範圍：15.25 - 1,678.67 |
| **Sales** | Float | 1,000 | 998 | 範圍：320.36 - 35,252.00 |
| **Payment** | String | 1,000 | 3 | 3種付款方式 |
| **cogs** | Float | 1,000 | 998 | 範圍：305.10 - 33,573.33 |
| **gross margin percentage** | Float | 1,000 | 1 | 固定值：4.76 |
| **gross income** | Float | 1,000 | 996 | 範圍：15.25 - 1,678.67 |
| **Rating** | Float | 1,000 | 61 | 範圍：4.00 - 10.00 |
| **Is_Holiday_Season** | Boolean | 1,000 | 2 | True/False |
| **Is_Promotion** | Boolean | 1,000 | 2 | True/False |

---

## 資料特徵

- **完整性**: 所有欄位無缺失值（1,000/1,000 筆完整）
- **重複值**: Invoice ID 無重複，完全重複記錄數為 0
- **數值範圍**: 
  - Unit price: 276.97 - 3,377.28
  - Quantity: 1 - 10
  - Sales: 320.36 - 35,252.00
  - Rating: 4.00 - 10.00
- **分類分布**: 
  - Branch: 7 個類別
  - Store_Name: 67 個不同店鋪
  - City: 6 個城市
  - Product line: 6 個商品線
  - Shopping_Period: 5 個時段
  - Membership_Level: 5 個等級

---

## 資料品質

✅ **良好**: 
- 無缺失值
- Invoice ID 唯一無重複
- 時間範圍連續（85個不同日期）
- 數值欄位無明顯異常
- 所有記錄完整

⚠️ **注意**: 
- gross margin percentage 為固定值（4.76）
- Quarter 僅包含單一值（Q1）
- Sales 數值範圍跨度較大（320 - 35,252）

🚫 **缺失**: 
- 無明顯缺失或異常問題

---

## 檔案資訊

- **生成時間**: 2025-12-24
- **檔案路徑**: `資料集/Taiwan_SuperMarket_Sales_2025.csv`
- **檔案格式**: CSV（逗號分隔）
- **編碼**: UTF-8
- **總記錄數**: 1,000 筆
- **總欄位數**: 28 個

---

**原則：客觀描述事實，讓資料自己說話。**

