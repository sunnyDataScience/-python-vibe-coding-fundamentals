import pandas as pd
import numpy as np
import random

df = pd.read_csv('../../資料集/Taiwan_SuperMarket_Sales_2025.csv')

print(f"原始數據集形狀: {df.shape}")
print(f"原始數據集欄位: {df.columns.tolist()}")

np.random.seed(42)
random.seed(42)

missing_configs = {
    'Customer type': 0.03,
    'Membership_Level': 0.05,
    'Age_Group': 0.02,
    'Rating': 0.04,
    'Unit price': 0.01,
    'Quantity': 0.02,
    'Store_Size': 0.03,
    'Gender': 0.02,
    'Eco_Premium': 0.03,
    'Is_Promotion': 0.02
}

for column, missing_ratio in missing_configs.items():
    if column in df.columns:
        n_missing = int(len(df) * missing_ratio)
        missing_indices = np.random.choice(df.index, n_missing, replace=False)
        df.loc[missing_indices, column] = np.nan
        print(f"在 {column} 欄位加入了 {n_missing} 個缺失值")

outlier_columns = ['Unit price', 'Quantity', 'Sales', 'Tax 5%', 'Rating']

for column in outlier_columns:
    if column in df.columns:
        original_values = df[column].dropna()

        if column == 'Unit price':
            n_outliers = 15
            outlier_indices = np.random.choice(df[df[column].notna()].index, n_outliers, replace=False)

            for idx in outlier_indices[:8]:
                df.loc[idx, column] = np.random.uniform(10000, 50000)

            for idx in outlier_indices[8:]:
                df.loc[idx, column] = np.random.uniform(0.1, 10)

        elif column == 'Quantity':
            n_outliers = 10
            outlier_indices = np.random.choice(df[df[column].notna()].index, n_outliers, replace=False)

            for idx in outlier_indices[:5]:
                df.loc[idx, column] = np.random.randint(100, 500)

            for idx in outlier_indices[5:]:
                df.loc[idx, column] = np.random.randint(-10, 0)

        elif column == 'Sales':
            n_outliers = 12
            outlier_indices = np.random.choice(df[df[column].notna()].index, n_outliers, replace=False)

            for idx in outlier_indices[:6]:
                df.loc[idx, column] = np.random.uniform(100000, 500000)

            for idx in outlier_indices[6:]:
                df.loc[idx, column] = np.random.uniform(-5000, 0)

        elif column == 'Tax 5%':
            n_outliers = 8
            outlier_indices = np.random.choice(df[df[column].notna()].index, n_outliers, replace=False)

            for idx in outlier_indices:
                df.loc[idx, column] = np.random.uniform(5000, 20000)

        elif column == 'Rating':
            n_outliers = 20
            outlier_indices = np.random.choice(df[df[column].notna()].index, n_outliers, replace=False)

            for idx in outlier_indices[:10]:
                df.loc[idx, column] = np.random.uniform(15, 100)

            for idx in outlier_indices[10:15]:
                df.loc[idx, column] = np.random.uniform(-10, 0)

            for idx in outlier_indices[15:]:
                df.loc[idx, column] = 999

        print(f"在 {column} 欄位加入了離群值")

duplicate_count = 30
duplicate_indices = np.random.choice(df.index, duplicate_count, replace=False)
duplicates = df.loc[duplicate_indices].copy()

for i, row in duplicates.iterrows():
    if np.random.random() > 0.5:
        col_to_modify = np.random.choice(['Unit price', 'Quantity', 'Rating'])
        if col_to_modify in duplicates.columns:
            duplicates.loc[i, col_to_modify] = duplicates.loc[i, col_to_modify] * np.random.uniform(0.9, 1.1)

df = pd.concat([df, duplicates], ignore_index=True)
print(f"加入了 {duplicate_count} 筆重複資料（部分有細微差異）")

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

output_path = '../../資料集/Taiwan_SuperMarket_Sales_2025_Practice.csv'
df.to_csv(output_path, index=False, encoding='utf-8-sig')

print("\n=== 數據集處理完成 ===")
print(f"最終數據集形狀: {df.shape}")
print(f"保存路徑: {output_path}")

print("\n=== 缺失值統計 ===")
missing_stats = df.isnull().sum()
missing_stats = missing_stats[missing_stats > 0]
for col, count in missing_stats.items():
    print(f"{col}: {count} 個缺失值 ({count/len(df)*100:.2f}%)")

print("\n=== 離群值範例 ===")
for column in outlier_columns:
    if column in df.columns:
        values = df[column].dropna()
        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = values[(values < lower_bound) | (values > upper_bound)]
        if len(outliers) > 0:
            print(f"{column}: 發現 {len(outliers)} 個離群值")
            print(f"  正常範圍: [{lower_bound:.2f}, {upper_bound:.2f}]")
            print(f"  離群值範例: {outliers.head(3).tolist()}")