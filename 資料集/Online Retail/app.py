
# 導入函式庫
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime as dt

# --- 頁面配置 ---
st.set_page_config(
    page_title="VIP 客戶挽留監控看板",
    page_icon="📊",
    layout="wide"
)

# --- 數據加載 ---
@st.cache_data
def load_data(path):
    """從指定路徑加載數據並進行預處理"""
    try:
        df = pd.read_csv(path, encoding='ISO-8859-1')
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        # 清洗數據
        df_clean = df.dropna(subset=['CustomerID'])
        df_clean = df_clean[(df_clean['Quantity'] > 0) & (df_clean['UnitPrice'] > 0)]
        df_clean['TotalSum'] = df_clean['Quantity'] * df_clean['UnitPrice']
        return df_clean
    except FileNotFoundError:
        st.error(f"找不到檔案: {path}")
        return pd.DataFrame()

# --- 分析邏輯函數 ---
def calculate_rfm(df):
    """計算 RFM 指標與分群"""
    snapshot_date = df['InvoiceDate'].max() + dt.timedelta(days=1)
    
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalSum': 'sum'
    }).rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'TotalSum': 'Monetary'})
    
    # 簡單分群邏輯 (使用固定閾值以便於業務理解，或使用分位數)
    # 這裡沿用分析報告中的邏輯：High M/F (Top 20%), Low R (Bottom 40% -> Oldest recency)
    # 為了演示互動性，我們讓這些閾值在 UI 上可調，或使用預設值
    
    # 判斷 At Risk: Recency > 90 days AND Frequency > 5 (High Value churned)
    def get_segment(row):
        if row['Recency'] > 90 and row['Frequency'] > 5:
            return 'High Risk (高價值流失)'
        elif row['Recency'] <= 90 and row['Frequency'] > 5:
            return 'Loyal (活躍 VIP)'
        elif row['Recency'] <= 90:
            return 'Active (一般活躍)'
        else:
            return 'Lost (已流失)'
            
    rfm['Segment'] = rfm.apply(get_segment, axis=1)
    return rfm

def calculate_cohort(df):
    """計算同類群組留存率"""
    def get_month(x): return dt.datetime(x.year, x.month, 1)
    df = df.copy() # 不要修改原始 cache 的 df
    df['InvoiceMonth'] = df['InvoiceDate'].apply(get_month)
    df['CohortMonth'] = df.groupby('CustomerID')['InvoiceMonth'].transform('min')
    
    def get_date_int(df, column):
        year = df[column].dt.year
        month = df[column].dt.month
        return year, month

    invoice_year, invoice_month = get_date_int(df, 'InvoiceMonth')
    cohort_year, cohort_month = get_date_int(df, 'CohortMonth')
    years_diff = invoice_year - cohort_year
    months_diff = invoice_month - cohort_month
    df['CohortIndex'] = years_diff * 12 + months_diff + 1
    
    grouping = df.groupby(['CohortMonth', 'CohortIndex'])
    cohort_data = grouping['CustomerID'].apply(pd.Series.nunique).reset_index()
    cohort_counts = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='CustomerID')
    cohort_sizes = cohort_counts.iloc[:, 0]
    retention = cohort_counts.divide(cohort_sizes, axis=0) * 100
    return retention

# --- 圖表函數 ---
def create_kpi_cards(rfm_df):
    """創建核心指標卡片"""
    at_risk = rfm_df[rfm_df['Segment'] == 'High Risk (高價值流失)']
    risk_count = len(at_risk)
    risk_revenue = at_risk['Monetary'].sum()
    
    # 假設本月目標是將風險人數控制在 200 以內
    delta_count = 200 - risk_count 
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🚨 高風險 VIP 人數", f"{risk_count} 人", f"{delta_count} (目標差)", delta_color="inverse")
    col2.metric("💸 潛在流失營收", f"£{risk_revenue:,.0f}", "需立即挽回")
    col3.metric("🏆 活躍 VIP 人數", f"{len(rfm_df[rfm_df['Segment'] == 'Loyal (活躍 VIP)'])} 人", "核心資產")

def create_rfm_chart(rfm_df):
    """創建 RFM 互動氣泡圖"""
    # 為了圖表清晰，過濾掉極端值
    plot_df = rfm_df[rfm_df['Monetary'] < rfm_df['Monetary'].quantile(0.99)]
    
    fig = px.scatter(
        plot_df, 
        x='Recency', 
        y='Frequency', 
        size='Monetary', 
        color='Segment',
        hover_name=plot_df.index,
        color_discrete_map={
            'High Risk (高價值流失)': 'red',
            'Loyal (活躍 VIP)': 'green',
            'Active (一般活躍)': 'blue',
            'Lost (已流失)': 'grey'
        },
        title="VIP 價值分佈雷達 (氣泡大小=消費金額)",
        labels={'Recency': '未回購天數', 'Frequency': '消費頻率'}
    )
    # 添加警戒線
    fig.add_vline(x=90, line_dash="dash", line_color="black", annotation_text="90天警戒線")
    st.plotly_chart(fig, use_container_width=True)

def create_cohort_heatmap(retention_df):
    """創建同類群組熱力圖"""
    fig = px.imshow(
        retention_df,
        labels=dict(x="Month Index", y="Cohort Month", color="Retention %"),
        x=retention_df.columns,
        y=retention_df.index.astype(str),
        color_continuous_scale='Blues',
        text_auto='.0f',
        title="同類群組留存率熱力圖 (新客斷層監控)"
    )
    fig.update_layout(xaxis_title="月數 (Month)", yaxis_title="獲客月份")
    st.plotly_chart(fig, use_container_width=True)

# --- 主程式 ---
def main():
    st.title("🛡️ Online Retail: VIP 客戶挽留監控看板")
    st.markdown("### 🎯 核心任務: 搶救 Project Rescue 名單中的 227 位高價值客戶")

    # 加載數據
    data_path = "online_retail_merged.csv" # 相對路徑
    df = load_data(data_path)
    
    if df.empty:
        st.stop()

    # --- 側邊欄篩選器 ---
    st.sidebar.header("🔍 全局篩選")
    country_list = ['All'] + sorted(df['Country'].unique().tolist())
    selected_country = st.sidebar.selectbox("選擇國家/地區", country_list)
    
    # 篩選數據
    if selected_country != 'All':
        df_filtered = df[df['Country'] == selected_country]
    else:
        df_filtered = df

    # 計算指標
    rfm_df = calculate_rfm(df_filtered)
    retention_df = calculate_cohort(df_filtered)

    # --- 渲染儀表板 ---
    
    # 1. 核心指標區
    create_kpi_cards(rfm_df)
    
    st.divider()

    # 2. 主要圖表區 (F型佈局左側) & 3. 待辦名單 (F型佈局右側)
    col_charts, col_b = st.columns([2, 1])
    
    with col_charts:
        st.subheader("📊 風險診斷")
        create_rfm_chart(rfm_df)
        
        st.subheader("📉 留存趨勢")
        create_cohort_heatmap(retention_df)

    with col_b:
        st.subheader("📋 待救援 VIP 名單")
        st.info("請優先聯繫下列「High Risk」客戶")
        
        # 篩選 High Risk
        risk_list = rfm_df[rfm_df['Segment'] == 'High Risk (高價值流失)'].sort_values('Monetary', ascending=False)
        
        # 顯示表格
        st.dataframe(
            risk_list[['Recency', 'Frequency', 'Monetary']].style.format({'Monetary': '£{:.0f}'}),
            use_container_width=True,
            height=600
        )
        
        # 模擬行動按鈕
        if not risk_list.empty:
            top_customer = risk_list.index[0]
            if st.button(f"📧 發送挽回優惠給 Top 1 (ID: {int(top_customer)})"):
                st.success(f"已發送 85折 優惠券給客戶 {int(top_customer)}！")

if __name__ == "__main__":
    main()
