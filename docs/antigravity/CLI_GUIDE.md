# Antigravity CLI（`agy`）入門與 `.agents` 設定手冊

> 本手冊專為初學者設計，說明 **Antigravity CLI（`agy`）** 的核心操作、常見內建指令，以及如何透過專案根目錄的 **`.agents/`** 目錄配置客製化 Agent 環境。

---

## 1. 快速上手

### 1.1 啟動與離開
- **啟動 CLI**：在專案根目錄執行 `agy`
- **開啟指令說明**：輸入 `/help`
- **離開 Session**：輸入 `/exit`（或按 `Ctrl+D` / `Ctrl+C`）
- **登出帳號**：輸入 `/logout`

---

## 2. `.agents` 設定與元件責任

Antigravity CLI 會在啟動時自動讀取專案根目錄下的 **`AGENTS.md`** 與 **`.agents/`** 資料夾。以下是各元件的責任與檔案位置：

```text
my-project/
├── AGENTS.md                   # 專案最高紀律與長期 Prompt 上下文
└── .agents/
    ├── skills/                 # Agent Skills（按需載入的程序知識）
    │   └── <skill-name>/
    │       └── SKILL.md
    ├── agents/                 # Subagent 定義檔
    │   └── <agent-name>/
    │       └── agent.md
    ├── rules/                  # 專案補充規範
    └── mcp_config.json         # MCP (Model Context Protocol) 擴充伺服器設定
```

### 2.1 元件責任對照表

| 元件 / 檔案 | 檔案路徑 | 責任與使用時機 |
|---|---|---|
| **專案契約 (Rules)** | `AGENTS.md` (或 `GEMINI.md`) | 長期 Context 與專案規範。包含專案架構、程式風格、安全底線與測試命令。 |
| **Agent Skills** | `.agents/skills/<name>/SKILL.md` | **按需載入的 SOP 與程序知識**。當 Agent 遇到特定任務時觸發讀取。 |
| **Subagents** | `.agents/agents/<name>/agent.md` | **獨立與隔離 context 的委派工作者**。適合用於耗時的研究、獨立診斷或特定角色作業。 |
| **MCP Config** | `.agents/mcp_config.json` | **外部工具與資料連線**。連接外部資料庫、瀏覽器自動化或 API 伺服器。 |
| **Rules 補充** | `.agents/rules/*.md` | 作為 `AGENTS.md` 的模組化補充文件。 |

---

### 2.2 如何撰寫一個 Agent Skill (`SKILL.md`)

每個 Skill 必須放在專用資料夾內，且檔名固定為 **`SKILL.md`**。
最關鍵的是 **YAML Frontmatter** 必須包含 `name` 與 `description`：

```markdown
---
name: build-check
description: 執行目前專案的語法與編譯檢查。當使用者要求驗證代碼時使用。
---

# Build Check 指南

1. 檢查專案根目錄的契約命令。
2. 執行編譯與檢查命令。
3. 若失敗，回報錯誤細節並給出修改建議。
```

> 🚨 **常見陷阱**：若漏掉 Frontmatter 中的 `description` 欄位，`agy` 會無法在 `/skills` 清單中讀取該 Skill。

---

## 3. 常見通用 Slash Commands（斜線指令）

進入 `agy` 互動介面後，可以在 Prompt 輸入斜線開頭的指令來管理與檢查 Agent 狀態：

### 3.1 狀態與管理面板

| 指令 | 說明 | 預期看到的內容 / 效果 |
|---|---|---|
| **/help** | 開啟指令面板 | 列出所有可用斜線指令與快捷鍵，按 `Esc` 關閉 |
| **/context** | 檢視 Context 上下文 | 顯示目前對話已載入的規則檔 (如 `AGENTS.md`)、系統提示與 Context 檔案清單 |
| **/skills** | 瀏覽 Agent Skills | 展示已載入的專案與全域 Skills 清單與描述 |
| **/agents** | 管理面板 (Agent Manager) | 列出已設定的 Subagents (Identifier, Role, Status) |
| **/mcp** | MCP 狀態面板 | 檢視已連線的 MCP Servers 狀態燈與連線 Log |
| **/hooks** | 檢視 Script Hooks | 列出已生效的 Pre-flight 與 Post-format hooks |
| **/permissions**| 檢視權限面板 | 分頁展示 Allowlist / Denylist / Asklist 設定 |

---

### 3.2 對話與額度管理

| 指令 | 說明 | 預期看到的內容 / 效果 |
|---|---|---|
| **/usage** *(別名 `/quota`)* | 查詢額度用量 | 顯示目前的 Token 使用量與剩餘配額 |
| **/clear** | 清理對話歷史 | 重新重設目前 Session 的對話上下文 |
| **/compact** | 壓縮 Context | 提煉歷史對話以節省 Token 佔用空間 |
| **/logout** | 登出帳號 | 清除本地 OS Keyring / 憑證檔並解除帳號連結 |
| **/exit** *(或 `/quit`)* | 離開 CLI | 結束 `agy` Session 回到系統 Shell |

---

## 4. 學生實戰建議

1. **最小元件原則**：
   不用為了湊齊功能而建立所有元件。簡單的專案只需要 `AGENTS.md`；需要固定操作 Sop 時再加入 `.agents/skills/`。
2. **認清元件責任**：
   - 規範寫在 `AGENTS.md`
   - 重複流程與 SOP 寫在 `.agents/skills/`
   - 外部資料擴充用 `.agents/mcp_config.json`
3. **路徑區隔**：
   `agy` 只讀取 `.agents/` 與根目錄的 `AGENTS.md`，**不會讀取 `.claude/` 目錄**。

---

## 下一步

- 閱讀 [`INSTALL.md`](./INSTALL.md) 了解 Antigravity CLI 的完整安裝與環境驗證。
