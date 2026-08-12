# Claude Code（`claude`）入門與 `.claude` 設定手冊

> 本手冊專為初學者設計，說明 **Claude Code** 的核心操作、課堂上真正會用到的斜線指令，
> 以及如何用專案根目錄的 **`CLAUDE.md`** 與 **`.claude/`** 配置 agent 環境。
>
> 安裝與環境驗證見 [`INSTALL.md`](./INSTALL.md)。指令清單依官方 commands 文件。

---

## 1. 快速上手

### 1.1 啟動與離開

| 動作 | 做法 |
| :--- | :--- |
| **啟動** | 在專案根目錄執行 `claude` |
| **開啟指令說明** | 輸入 `/help` |
| **離開 session** | 輸入 `/exit`（或 `/quit`、`Ctrl+D`） |
| **登出帳號** | 輸入 `/logout` |
| **看目前狀態與模型** | 輸入 `/status` |

### 1.2 三個一開始就該知道的操作

| 你想做的事 | 指令 | 為什麼重要 |
| :--- | :--- | :--- |
| **確認契約載入了** | `/context` | 看 `Memory files` 有沒有列出 `CLAUDE.md`。沒有的話 agent 不知道資料集契約，會開始猜欄位名 |
| **對話變長、開始失憶** | `/compact` | 壓縮歷史對話釋出 context。跑完一個完整分析階段之後很適合做一次 |
| **換個題目重來** | `/clear` | 開一段空 context 的新對話。**做完階段 01 要開始階段 02 時，用這個比讓對話一直長下去乾淨** |

> 💡 `/clear` 會清掉對話，但 `CLAUDE.md` 與 `AGENTS.md` 的契約**每次都會重新載入**，不用擔心。

### 1.3 非互動模式（跑批次用）

```bash
claude -p "讀 AGENTS.md 第 3 節，然後產出 online_retail_09_10.csv 的數據卡"
```

`-p` 是 headless 模式，適合寫成腳本。要接續上一段對話用 `--continue`，要挑一段舊對話用 `--resume`。

---

## 2. `CLAUDE.md` 與 `.claude` 設定

Claude Code 啟動時會從**當前目錄往上走到 repo 根目錄**，沿路載入設定。

```text
your-project/
├── CLAUDE.md                   # 專案指令（本 repo 用它 import AGENTS.md）
├── AGENTS.md                   # 跨工具契約（Claude Code 透過 import 讀到）
├── .mcp.json                   # 專案層級 MCP server 設定
└── .claude/
    ├── CLAUDE.md               # 專案指令的另一個合法位置
    ├── rules/                  # 模組化規範，可用 paths: 限定觸發時機
    │   └── <topic>.md
    ├── skills/                 # 按需載入的 SOP
    │   └── <skill-name>/
    │       └── SKILL.md
    ├── agents/                 # Subagent 定義
    │   └── <agent-name>.md
    └── settings.json           # 權限、環境變數等專案設定
```

### 2.1 元件責任對照表

| 元件 / 檔案 | 檔案路徑 | 責任與使用時機 |
| :--- | :--- | :--- |
| **專案契約** | `CLAUDE.md`（或 `.claude/CLAUDE.md`） | **每次 session 都會全文載入。** 放需要一直記得的事實：專案架構、命名慣例、「永遠要做 X」的規則 |
| **模組化規範** | `.claude/rules/<topic>.md` | `CLAUDE.md` 長太大時的拆分去處。加 `paths:` frontmatter 可讓它只在 Claude 碰到符合的檔案時才載入 |
| **Agent Skills** | `.claude/skills/<name>/SKILL.md` | **按需載入的程序知識與 SOP。** 資料夾名稱就是你打的 `/指令` |
| **Subagents** | `.claude/agents/<name>.md` | **獨立 context 的委派工作者。** 適合會產生大量中間輸出、但你只要結論的工作 |
| **MCP 設定** | `.mcp.json` | 外部工具與資料連線 |
| **專案設定** | `.claude/settings.json` | 權限規則、環境變數、自動更新頻道等 |
| **個人偏好** | `~/.claude/CLAUDE.md`、`~/.claude/rules/`、`~/.claude/skills/` | 跨所有專案的個人設定，不進版控 |

> **`CLAUDE.md` 依官方建議控制在 200 行以內。** 太長會吃掉 context，也降低遵循度。
> 判斷準則：**是「事實」就寫 `CLAUDE.md`，是「多步驟流程」就寫成 skill。**

### 2.2 本 repo 的實際接法（重要）

**依官方文件（原文）**：「Claude Code reads `CLAUDE.md`, not `AGENTS.md`.」

本 repo 的契約寫在 `AGENTS.md`（給四款 agent 共用），所以根目錄的 `CLAUDE.md` 是一個薄封裝：

```markdown
# CLAUDE.md

本專案的作業規範寫在 AGENTS.md（Antigravity / Claude Code / Codex 共用同一份）。

@AGENTS.md

---

## Claude Code 專屬補充
（只寫 AGENTS.md 沒有、且與 Claude Code 環境相關的部分）
```

這正是官方示範的接法。**你不需要自己建立它，本 repo 已經有了。**

> 🚨 **不要把 `AGENTS.md` 的內容複製一份到 `CLAUDE.md`。**
> 兩份會慢慢走鐘，然後你會遇到「Claude 說 A、Codex 說 B」而找不到原因。
> 單一真相源永遠是 `AGENTS.md`。

### 2.3 如何撰寫一個 Skill（`SKILL.md`）

每個 skill 是一個資料夾，進入點檔名固定為 **`SKILL.md`**，
YAML frontmatter 必須有 `name` 與 `description`：

```markdown
---
name: data-card
description: 為指定資料集產出標準化數據卡。當使用者要求描述、profiling 或認識一個新資料集時使用。
---

# 數據卡產出流程

1. 先讀專案根目錄 `AGENTS.md` 第 3 節的資料集契約，確認編碼與欄位名。
2. 實際讀檔計算：總行數、每欄 dtype／缺失率／唯一值數。
3. 主動檢查主鍵唯一性、恆定欄位、不合理負值、衍生欄位自洽。
4. profiling 程式碼存到 `scripts/profile_<資料集>.py`，數據卡寫到 `reports/data_card_<資料集>.md`。
5. **數據卡裡不得出現任何未經計算的數字。**
```

存成 `.claude/skills/data-card/SKILL.md` 之後，輸入 `/data-card` 就會觸發，
或是 Claude 判斷你的需求相關時自己載入。

| Frontmatter 欄位 | 必填 | 說明 |
| :--- | :--- | :--- |
| `name` | ✅ | skill 名稱 |
| `description` | ✅ | **決定 Claude 何時自動載入它**，寫清楚觸發時機 |
| `allowed-tools` | ❌ | 這個 skill 觸發的那一輪可以免詢問使用的工具 |
| `disallowed-tools` | ❌ | 這個 skill 生效期間要移除的工具 |

> 💡 `.claude/commands/<name>.md` 與 `.claude/skills/<name>/SKILL.md` 都會產生 `/<name>` 指令，
> 兩者行為相同。skill 多了「可以放輔助檔案」與「Claude 可自行判斷載入」兩項能力。

### 2.4 Subagent

```markdown
---
name: number-auditor
description: 稽核報告中的每一個量化陳述，逐項重算。交付分析報告前使用。
tools: Read, Glob, Grep, Bash
model: sonnet
---

你是資料稽核員。你的工作不是幫報告講得更好聽，而是找出站不住腳的數字。
每個數字都先假設它是錯的，直到你親手用**另一種算法**把它算出來為止。
```

存成 `.claude/agents/number-auditor.md`（專案）或 `~/.claude/agents/`（跨專案）。

> 🚨 **`name` 在整棵樹裡要唯一。** 同一個目錄下兩個檔案宣告同樣的 `name`，
> Claude Code 只會載入其中一個，而且是由檔案系統讀取順序決定的 —— 不是你能預測的那個。

---

## 3. 課堂上真正會用到的斜線指令

Claude Code 內建的指令很多，以下只列跑分析流程會用到的。完整清單輸入 `/help`。

### 3.1 狀態與設定

| 指令 | 說明 | 什麼時候用 |
| :--- | :--- | :--- |
| **`/context`** | 視覺化目前 context 使用量，並列出載入的 memory files | **每次進到新 repo 先跑一次**，確認契約有載入 |
| **`/memory`** | 編輯 `CLAUDE.md` 並管理自動記憶 | 想改契約時，比自己找檔案快 |
| **`/status`** | 顯示 session 狀態與目前模型 | 想確認在用哪個模型 |
| **`/model`** | 切換模型並存成預設 | 想換一顆模型當稽核員時 |
| **`/config`** | 開設定介面（別名 `/settings`） | 調主題、自動更新頻道等 |
| **`/doctor`** | 跑一次設定健檢並修問題 | 有東西怪怪的但說不上來 |
| **`/permissions`** | 管理工具權限的 allow / ask / deny | 一直被權限提示打斷時 |

### 3.2 對話管理

| 指令 | 說明 | 什麼時候用 |
| :--- | :--- | :--- |
| **`/clear`** | 開一段空 context 的新對話（別名 `/new`） | **換階段時用。** 階段 01 做完要開始階段 02+ |
| **`/compact`** | 摘要壓縮對話以釋出 context | 對話很長但還想接著同一條線做 |
| **`/resume`** | 回到先前的對話 | 昨天做到一半 |
| **`/rewind`** | 把程式碼與對話一起回捲到某個檢查點 | agent 改壞了東西 |
| **`/undo`** | 復原上一次變更 | 同上，但只要退一步 |
| **`/export`** | 把目前對話匯出成純文字 | 要把分析過程交出去當佐證 |
| **`/usage`** | 顯示本 session 的 token 用量與花費（別名 `/cost`） | 想知道跑一次完整分析要多少 |

### 3.3 擴充與委派

| 指令 | 說明 |
| :--- | :--- |
| **`/init`** | 分析 codebase 並產生起始 `CLAUDE.md`。已存在時改為提出改進建議 |
| **`/skills`** | 管理自訂 skills |
| **`/agents`** | 管理 subagent 設定 |
| **`/mcp`** | 管理 MCP server 連線與 OAuth |
| **`/hooks`** | 檢視工具事件的 hook 設定 |
| **`/import`** | 把其他 coding agent 的設定匯入 Claude Code（支援 `codex`、`gemini`） |

> 💡 **`/import codex`** 對本教材的讀者特別有用：如果你已經先裝了 Codex 並設定好，
> 這個指令會把指令檔、MCP server、subagent 與 skill 帶過來。
> 依官方文件需要 Claude Code v2.1.213 以上。

---

## 4. 學生實戰建議

1. **最小元件原則。**
   走完六階段分析流程，你**只需要 `AGENTS.md` ＋ 本 repo 已有的 `CLAUDE.md`**。
   不用建 skills、不用建 subagent。等到你發現自己第三次貼同一段指令，再把它寫成 skill。

2. **認清元件責任。**
   - 「這個資料集的 `CustomerID` 有 20.5% 缺失」→ 事實 → `AGENTS.md`
   - 「產數據卡要照這五個步驟做」→ 流程 → `.claude/skills/`
   - 「稽核報告數字時要換一種算法重算」→ 角色 → `.claude/agents/`

3. **每個階段開一段新對話。**
   分析流程的六個階段各自有明確的輸入與產出。用 `/clear` 分段，
   把上一階段的產出**當成文字貼進去**（或指向 `reports/` 裡的檔案），
   比讓一段對話從階段 00 一路長到階段 05 可靠得多 —— 後者到後面會開始忘記前面算過什麼。

4. **路徑區隔。**
   `claude` 只讀 `CLAUDE.md` 與 `.claude/`，**不會讀 `.agents/`（Antigravity）
   或 `~/.codex/`（Codex）**。跨工具共用的東西一律放 `AGENTS.md`。

5. **驗收數字的時候，換一顆模型。**
   用 `/model` 切換，或乾脆換一款 agent 來跑
   [`04報告呈現/報告數字驗算.md`](../../上課用prompt/04報告呈現/報告數字驗算.md)。
   同一顆模型自己審自己，會對自己的產出評分偏高。

---

## 下一步

- 安裝與環境驗證 → [`INSTALL.md`](./INSTALL.md)
- 選擇其他 agent、四款對照 → [`../README.md`](../README.md)
- 回到分析主線 → [`上課用prompt/index.html`](../../上課用prompt/index.html)
