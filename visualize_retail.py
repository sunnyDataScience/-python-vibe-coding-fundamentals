
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import matplotlib.font_manager as fm

# Setup - Enable Chinese Font
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# Paths
base_dir = Path(r'd:\python_workspace\github\-python-vibe-coding-fundamentals\資料集\Online Retail')
input_file = base_dir / 'online_retail_merged.csv'
output_dir = base_dir / 'charts'
output_dir.mkdir(exist_ok=True)

def visualize():
    print("Loading data...")
    df = pd.read_csv(input_file, encoding='ISO-8859-1')
    
    # --- Data Prep (Same as before) ---
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df_clean = df.dropna(subset=['CustomerID'])
    df_clean = df_clean[(df_clean['Quantity'] > 0) & (df_clean['UnitPrice'] > 0)]
    df_clean['TotalSum'] = df_clean['Quantity'] * df_clean['UnitPrice']
    
    snapshot_date = df_clean['InvoiceDate'].max() + dt.timedelta(days=1)
    
    # --- 1. RFM Bubble Chart ---
    print("Generating RFM Chart...")
    rfm = df_clean.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalSum': 'sum'
    }).rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'TotalSum': 'Monetary'})
    
    # Filter for better visualization (remove extreme outliers for plot clarity if needed)
    # But for "At Risk" we need to see everyone.
    
    # Identify At Risk
    cutoff_R = rfm['Recency'].quantile(0.4) # approximate quintile 2
    cutoff_F = rfm['Frequency'].quantile(0.8) # approximate quintile 4
    cutoff_M = rfm['Monetary'].quantile(0.8)
    
    # Logic: High M/F (Top 20%), Low R (Bottom 40% -> Oldest recency) 
    # Actually Recency is days, so High Days = Bad. 
    # R_Score 1-2 means High Recency days.
    # Let's simple plot:
    
    plt.figure(figsize=(12, 8))
    
    # Create segments for coloring
    def get_color(row):
        # Simply: if Recent (Low R) and High Freq -> Green (Champ)
        # If Old (High R) and High Freq -> Red (At Risk)
        if row['Recency'] > 90 and row['Frequency'] > 5:
            return 'red' # At Risk
        elif row['Recency'] <= 90 and row['Frequency'] > 5:
            return 'green' # Loyal/Champ
        else:
            return 'grey'

    colors = rfm.apply(get_color, axis=1)
    
    # Scale Monetary for bubble size
    # Norm size
    sizes = rfm['Monetary'] / rfm['Monetary'].max() * 1000 + 10
    
    plt.scatter(rfm['Recency'], rfm['Frequency'], s=sizes, c=colors, alpha=0.5, edgecolors='w')
    
    plt.title('VIP 流失風險分佈圖 (大小=消費金額)', fontsize=16)
    plt.xlabel('未回購天數 (Recency)', fontsize=12)
    plt.ylabel('消費頻率 (Frequency)', fontsize=12)
    plt.axvline(x=90, color='k', linestyle='--', alpha=0.3)
    plt.text(100, rfm['Frequency'].max()*0.9, '高風險流失區\n(>90天未回購)', color='red', fontsize=12)
    plt.text(10, rfm['Frequency'].max()*0.9, '活躍留存區', color='green', fontsize=12)
    
    # Limit Axes to remove extreme outliers for readability
    plt.xlim(0, 370)
    plt.ylim(0, 100) # Most people < 100 freq
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'rfm_bubble_chart.png', dpi=100)
    plt.close()

    # --- 2. Cohort Heatmap ---
    print("Generating Cohort Heatmap...")
    def get_month(x): return dt.datetime(x.year, x.month, 1)
    df_clean['InvoiceMonth'] = df_clean['InvoiceDate'].apply(get_month)
    df_clean['CohortMonth'] = df_clean.groupby('CustomerID')['InvoiceMonth'].transform('min')
    
    def get_date_int(df, column):
        year = df[column].dt.year
        month = df[column].dt.month
        return year, month

    invoice_year, invoice_month = get_date_int(df_clean, 'InvoiceMonth')
    cohort_year, cohort_month = get_date_int(df_clean, 'CohortMonth')
    years_diff = invoice_year - cohort_year
    months_diff = invoice_month - cohort_month
    df_clean['CohortIndex'] = years_diff * 12 + months_diff + 1
    
    grouping = df_clean.groupby(['CohortMonth', 'CohortIndex'])
    cohort_data = grouping['CustomerID'].apply(pd.Series.nunique).reset_index()
    cohort_counts = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='CustomerID')
    cohort_sizes = cohort_counts.iloc[:, 0]
    retention = cohort_counts.divide(cohort_sizes, axis=0) * 100
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(data=retention, annot=True, fmt='.0f', vmin=0, vmax=50, cmap='Blues')
    plt.title('同類群組留存率熱力圖 (Cohort Analysis)', fontsize=16)
    plt.ylabel('獲客月份', fontsize=12)
    plt.xlabel('月數 (Month)', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'cohort_heatmap.png', dpi=100)
    plt.close()
    
    print(f"Charts saved to {output_dir}")

if __name__ == "__main__":
    visualize()
