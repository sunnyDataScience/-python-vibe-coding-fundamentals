# Codex CLI（`codex`）入門與 `AGENTS.md` 設定手冊

> 本手冊專為初學者設計，說明 **Codex CLI** 的核心操作、課堂上真正會用到的斜線指令，
> 以及 Codex 如何讀取 `AGENTS.md`。
>
> 安裝與環境驗證見 [`INSTALL.md`](./INSTALL.md)。
> 指令清單依官方 developer-commands 文件與 `codex --help`（**本機實測** `codex-cli 0.146.0`）。

---

## 1. 快速上手

### 1.1 啟動與離開

| 動作 | 做法 |
| :--- | :--- |
| **啟動** | 在專案根目錄執行 `codex` |
| **直接帶著問題啟動** | `codex "幫我看一下 AGENTS.md 第 3 節"` |
| **列出斜線指令** | 在輸入框打 `/` |
| **離開** | `/exit`（別名 `/quit`），或按 `Ctrl+C` |
| **登出** | `/logout`，或在 shell 跑 `codex logout` |

### 1.2 上課會用到的啟動旗標

```bash
codex -s workspace-write -a on-request
```

| 旗標 | 意思 | 為什麼分析課要用 |
| :--- | :--- | :--- |
| `-s workspace-write` | 沙箱允許寫入工作目錄 | 不開這個，agent 存不了 `scripts/`、`reports/`、`charts/` |
| `-a on-request` | 由模型決定何時要你核准 | 預設較嚴格時，每個指令都要按核准會跑不動 |
| `-m <model>` | 指定模型 | 想換一顆模型當稽核員 |
| `-C <dir>` | 指定工作根目錄 | 你人在別的地方但想對這個 repo 動手 |
| `--search` | 開啟即時網路搜尋 | 需要查外部資料時（分析課用不太到） |

> 完整可選值見 [`INSTALL.md` 第 3 節](./INSTALL.md#3-兩個上課前該先懂的設定)。
> 🚨 不要用 `--dangerously-bypass-approvals-and-sandbox`。

### 1.3 非互動模式（跑批次用）

```bash
codex exec "讀 AGENTS.md 第 3 節，產出 online_retail_09_10.csv 的數據卡到 reports/"
```

`exec`（別名 `e`）是非互動模式。相關子命令：

| 子命令 | 用途（依 `codex --help`） |
| :--- | :--- |
| `codex exec` | 非互動執行 |
| `codex review` | 非互動跑一次 code review |
| `codex resume` | 接續先前的互動 session（預設出現選單，`--last` 直接接最近一次） |
| `codex fork` | 從先前的 session 分岔出一條新的 |
| `codex apply` | 把 agent 產出的最新 diff 用 `git apply` 套到工作目錄 |
| `codex archive` / `unarchive` / `delete` | 封存／解封存／永久刪除已存的 session |
| `codex stats`／`codex features` | 用量統計／檢視 feature flag |

---

## 2. Codex 怎麼讀專案契約

### 2.1 讀取與合併順序

依官方 `agents-md` 指南：

```text
【全域】 ~/.codex/AGENTS.override.md   ← 存在就讀它
         ~/.codex/AGENTS.md           ← 否則讀這個

【專案】 從 project root（通常是 git root）往下走到你的 cwd，
         沿路每一層依序找：
           1. AGENTS.override.md
           2. AGENTS.md
           3. project_doc_fallback_filenames 設定的備援檔名
```

**合併方式**：由 root 往下串接，用空行相連。
**越靠近 cwd 的檔案越晚出現，所以會覆蓋前面的指引。**

| 規則 | 值 |
| :--- | :--- |
| 空檔案 | 跳過 |
| 合併總大小上限 | `project_doc_max_bytes`，預設 **32 KiB**；達到上限就停止加入 |

> 🚨 **超過上限的部分是被靜默丟掉的，不會有任何警告。**
> 在 monorepo 或多層 `AGENTS.md` 的情境下要特別小心。

### 2.2 本 repo 的情況

**不需要任何設定。** 本 repo 根目錄就有 `AGENTS.md`，Codex 原生讀得到。

```text
ai-data-analysis-workshop/
├── AGENTS.md          ← Codex 直接讀這份（資料集契約 + 分析鐵律）
├── CLAUDE.md          ← 這是給 Claude Code 用的轉接層，Codex 不理它
└── 上課用prompt/
```

驗收方式見 [`../README.md`](../README.md#3-裝完之後先做這個驗收) 第 3 節。

### 2.3 個人偏好放哪裡

想加「我自己的習慣」但不想動到 repo 的共用契約，建立 `~/.codex/AGENTS.md`：

```markdown
# 我的個人偏好

- 產出的中文用繁體，不要簡體。
- 圖表標題一律寫成能直接看出結論的句子，不要寫「各類別銷售額」這種標題。
- 每次做完清洗，主動把剔除列數與佔比列成表。
```

它會跟專案的 `AGENTS.md` 合併，**專案的排在後面所以優先權較高**。

> 💡 想暫時蓋掉全域設定又不想刪檔，建 `~/.codex/AGENTS.override.md`，用完刪掉即可還原。

---

## 3. 課堂上真正會用到的斜線指令

依官方 developer-commands 文件。完整清單在互動介面打 `/` 就會列出。

### 3.1 對話管理

| 指令 | 說明（官方原文轉述） | 什麼時候用 |
| :--- | :--- | :--- |
| **`/clear`** | 清空終端機並開始新對話 | **換階段時用。** 階段 01 做完要開始階段 02+ |
| **`/compact`** | 摘要目前可見對話以釋出 token | 對話很長但還想接著同一條線做 |
| **`/rename`** | 重新命名目前對話 | 一天跑好幾條分析線時 |
| **`/diff`** | 用 diff 檢視變更 | agent 改完檔案，你要看它到底動了什麼 |
| **`/copy`** | 複製最近一次完成的 Codex 輸出 | 要把洞察摘要貼到下一階段的 `CONTEXT` |
| **`/archive`** | 封存目前 session 並離開 | 這條線先擱著 |
| **`/exit`** | 離開（別名 `/quit`） | — |

### 3.2 設定與擴充

| 指令 | 說明（官方原文轉述） |
| :--- | :--- |
| **`/permissions`** | 設定 Codex 可以不問就做哪些事 |
| **`/init`** | 產生 `AGENTS.md` 骨架（🚨 **本 repo 已經有了，不要在這裡跑**） |
| **`/skills`** | 瀏覽與使用 skills |
| **`/agent`**、**`/subagents`** | 切換目前的 agent thread |
| **`/plugins`** | 瀏覽已安裝與可安裝的 plugin |
| **`/hooks`** | 檢視與管理 lifecycle hooks |
| **`/memories`** | 設定記憶的使用與生成 |
| **`/ide`** | 帶入開啟中的檔案與編輯器上下文 |
| **`/import`** | **匯入 Claude Code 或 Cursor 的設定** |
| **`/keymap`** | 重新設定 TUI 快捷鍵 |
| **`/vim`** | 切換輸入框的 Vim 模式 |

> 💡 **`/import`** 對本教材的讀者很有用：先裝了 Claude Code 並設定好之後，
> 用它把設定帶過來，不用重做一次。

### 3.3 鍵盤快捷鍵

| 按鍵 | 作用 |
| :--- | :--- |
| **`@`** | 搜尋工作區檔案並插入路徑 —— **指定資料集路徑時最好用** |
| **`!`** | 用目前權限直接跑一個本機 shell 命令 |
| **`Tab`** | agent 還在工作時，先排隊下一個 prompt |
| **`Esc` 按兩下** | 編輯前一則訊息並分岔對話 |
| **`Ctrl+R`** | 搜尋 prompt 歷史 |
| **`Ctrl+O`** | 複製最新輸出（等同 `/copy`） |
| **`↑` / `↓`** | 瀏覽 prompt 草稿歷史 |
| **`Ctrl+C`** | 關閉 session（等同 `/exit`） |

---

## 4. 學生實戰建議

1. **先把沙箱與核准調對，再開始上課。**
   Codex 跟其他三款最大的差別就在這裡。`-s workspace-write -a on-request` 是分析課的合理起點。
   一直被卡住就回頭看 [`INSTALL.md` 第 3 節](./INSTALL.md#3-兩個上課前該先懂的設定)，
   **不要直接跳到 bypass 旗標**。

2. **用 `@` 指定資料集，不要用手打路徑。**
   本 repo 的路徑含中文（`資料集/Online Retail/...`），手打很容易錯。
   `@` 會搜尋工作區檔案並插入正確路徑。

3. **每個階段開一段新對話。**
   六階段各自有明確的輸入與產出。用 `/clear` 分段，把上一階段的產出當文字貼進去，
   比讓一段對話從階段 00 一路長到階段 05 可靠得多。

4. **`/diff` 是你的安全網。**
   agent 說它「已經把清洗邏輯修好了」的時候，用 `/diff` 看它實際改了什麼。
   這比讀它的自述可靠。

5. **注意 32 KiB 的 `AGENTS.md` 合併上限。**
   本 repo 的 `AGENTS.md` 約 12 KB，離上限還有餘裕。但如果你在子目錄又加了幾份，
   超出的部分會被靜默丟掉 —— 而你不會收到任何警告。

6. **路徑區隔。**
   `codex` 只讀 `AGENTS.md` 與 `~/.codex/`，**不會讀 `CLAUDE.md`（Claude Code）
   或 `.agents/`（Antigravity）**。跨工具共用的東西一律放 `AGENTS.md`。

---

## 下一步

- 安裝與環境驗證 → [`INSTALL.md`](./INSTALL.md)
- 選擇其他 agent、四款對照 → [`../README.md`](../README.md)
- 回到分析主線 → [`上課用prompt/index.html`](../../上課用prompt/index.html)
