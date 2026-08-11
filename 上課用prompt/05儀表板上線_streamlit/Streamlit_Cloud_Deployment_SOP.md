# 🚀 Streamlit 儀表板上線 SOP (標準作業流程)

這份 SOP 將引導您將 AI 生成的 Streamlit 應用程式程式碼，成功部署到 Streamlit Cloud，讓全世界都能看到您的數據產品。

> ⚠️ **開始前請注意兩件事**
> 1. **資料會變成公開的。** 步驟 3 會把整個資料夾推上**公開** GitHub 倉庫，
>    任何人都看得到你的 CSV。請只使用課程提供的練習資料集，
>    **絕對不要放公司實際資料、個資或任何含客戶姓名/電話/Email 的檔案**。
> 2. **檔案大小有限制。** GitHub 單檔上限 100MB，Streamlit Cloud 的免費額度記憶體也有限。
>    本課程的 `資料集/Online Retail/*.csv` 各約 42MB，兩個都推上去會很吃力 —
>    建議先在本機做好聚合、只上傳儀表板真正需要的精簡資料（通常幾 MB 就夠）。

### **步驟 1：專案環境準備**

1.  **創建專案資料夾**：在您的電腦上創建一個新的資料夾，例如 `my-dashboard`。
2.  **放入數據集**：將您的數據集檔案（例如 `Taiwan_SuperMarket_Sales_2025_Practice.csv`）複製到這個資料夾中。
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
