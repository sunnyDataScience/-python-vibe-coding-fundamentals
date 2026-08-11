# 🚀 Streamlit 儀表板上線 SOP (標準作業流程)

這份 SOP 將引導您將 AI 生成的 Streamlit 應用程式程式碼，成功部署到 Streamlit Cloud，讓全世界都能看到您的數據產品。

> ⚠️ **開始前請注意兩件事**
> 1. **資料會變成公開的。** 步驟 3 會把整個資料夾推上**公開** GitHub 倉庫，
>    任何人都看得到你的 CSV。請只使用課程提供的練習資料集，
>    **絕對不要放公司實際資料、個資或任何含客戶姓名/電話/Email 的檔案**。
> 2. **檔案大小有限制。** GitHub 單檔上限 100MB，Streamlit Cloud 的免費額度記憶體也有限。
>    本課程的 `資料集/Online Retail/*.csv` 各約 42MB，直接推上去會很吃力 —
>    所以有了下面的**步驟 0**，先把資料聚合成幾 MB 的精簡版再帶走。

### **步驟 0：準備精簡資料集**

儀表板部署用的是**另一個獨立的輕量倉庫**，不是本課程這個 repo。
所以第一件事是把要帶過去的資料瘦身。

1.  **確認資料量**：`資料集/Online Retail/*.csv` 各約 42MB —— 這種大小不該進部署倉庫。
    `Taiwan_SuperMarket_Sales_2025_Practice.csv` 只有 228KB，可以直接用。
2.  **需要瘦身時，寫一支聚合腳本**放到本專案的 `scripts/`（沿用 `AGENTS.md` 第 5 節的慣例），
    把儀表板真正需要的欄位與粒度算好再輸出。常見做法：
    - 按「日 × 國家 × 產品類別」聚合，而不是保留每一筆交易明細
    - 只留藍圖裡實際用到的欄位
    - 客戶層級的表（如 RFM 結果）另存一份，通常只有幾千列
3.  **驗證瘦身結果**：聚合後的總營收、總筆數要對得上原始資料 —— 這一步等同於一次小型的
    「報告數字驗算」，不要瘦完就直接用。

> 💡 模式 B 的使用者：直接叫 agent「依這份藍圖，從 `資料集/...` 產出部署用的精簡 CSV，
> 腳本放 `scripts/`，並驗證聚合前後總額一致」。它會連驗算一起做掉。

### **步驟 1：專案環境準備**

1.  **創建專案資料夾**：在您的電腦上創建一個新的資料夾，例如 `my-dashboard`。
    **放在本課程 repo 之外**，它會是一個獨立的 Git 倉庫。
2.  **放入數據集**：把步驟 0 產出的**精簡** CSV 複製到這個資料夾中。
3.  **生成程式碼**：使用 `Streamlit_App_Generator_Prompt.md` 模板，將您的設計藍圖和數據集資訊填入，讓 AI 生成 `app.py` 和 `requirements.txt` 的程式碼。
4.  **創建檔案**：在 `my-dashboard` 資料夾中，創建 `app.py` 和 `requirements.txt` 兩個檔案，並將 AI 生成的對應程式碼分別貼入。

### **步驟 2：本地測試與驗證**

1.  **打開終端機**：在您的 `my-dashboard` 資料夾中打開一個終端機或命令提示字元。
2.  **創建虛擬環境** (強烈建議)：
    ```bash
    python -m venv venv
    ```
3.  **激活虛擬環境**：
    -   Windows: `.\venv\Scripts\activate`
    -   macOS/Linux: `source venv/bin/activate`
4.  **安裝依賴套件**：
    ```bash
    pip install -r requirements.txt
    ```
5.  **運行應用**：
    ```bash
    streamlit run app.py
    ```
6.  **驗證**：您的瀏覽器應該會自動打開一個新分頁，顯示您的儀表板。請在本地與所有篩選器和圖表互動，確保一切運作正常。

### **步驟 3：部署到 Streamlit Cloud**

> ✅ **推上去之前，逐項打勾**（推出去就收不回來了，快取與 fork 都可能留存）
> - [ ] 資料夾裡沒有公司實際資料、個資、客戶姓名／電話／Email
> - [ ] 沒有 `.env`、API key、資料庫連線字串或任何密碼
> - [ ] CSV 是步驟 0 的精簡版，不是 42MB 的原始檔
> - [ ] 本地 `streamlit run app.py` 跑得起來，篩選器與圖表都正常
> - [ ] `requirements.txt` 列的套件與 `app.py` 實際 import 的一致

1.  **註冊 GitHub 帳號**：如果您還沒有，請先註冊一個 [GitHub](https://github.com/) 帳號。
2.  **創建 GitHub 倉庫**：在 GitHub 上創建一個新的**公開 (Public)** 倉庫，例如 `my-dashboard-app`。
3.  **將專案推送到 GitHub**：
    -   回到您電腦上的 `my-dashboard` 資料夾和終端機。
    -   **初始化 Git**：
        ```bash
        git init
        ```
    -   **創建 `.gitignore`** (可選，但推薦)：創建一個名為 `.gitignore` 的檔案，並寫入以下內容，以避免上傳虛擬環境等不必要的檔案。
        ```
        venv/
        __pycache__/
        *.pyc
        ```
    -   **添加、提交與推送** (請將 `YourUsername` 和 `YourRepoName` 換成您自己的)：
        ```bash
        git add .
        git commit -m "Initial commit: Add dashboard app files"
        git branch -M main
        git remote add origin https://github.com/YourUsername/YourRepoName.git
        git push -u origin main
        ```
4.  **註冊 Streamlit Cloud**：前往 [share.streamlit.io](https://share.streamlit.io/) 並使用您的 GitHub 帳號登入。
5.  **部署新應用**：
    -   登入後，點擊右上角的 "New app" 按鈕。
    -   在 "Deploy an app" 頁面，選擇您剛剛創建的 GitHub 倉庫。
    -   確認 `Branch` 是 `main`，`Main file path` 是 `app.py`。
    -   點擊 "Deploy!" 按鈕。
6.  **等待與分享**：Streamlit Cloud 會自動開始安裝依賴並部署您的應用。幾分鐘後，您的儀表板就會上線，並擁有一個公開的 URL，您可以將其分享給任何人！
