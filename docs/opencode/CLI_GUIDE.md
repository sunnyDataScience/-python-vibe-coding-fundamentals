# opencode 入門與 `opencode.json` 設定手冊

> 本手冊專為初學者設計，說明 **opencode** 的核心操作、課堂上真正會用到的斜線指令，
> 以及如何用 `AGENTS.md` 與 `opencode.json` 配置 agent 環境。
>
> 安裝與環境驗證見 [`INSTALL.md`](./INSTALL.md)。
>
> 🚨 **本文全部內容取自 `opencode.ai/docs` 官方文件**，沒有本機實測。
> 你的畫面與本文不同時，以你的畫面與官方文件為準。

---

## 1. 快速上手

### 1.1 啟動與離開

| 動作 | 做法 |
| :--- | :--- |
| **啟動** | 在專案根目錄執行 `opencode` |
| **開說明** | `/help` |
| **命令面板** | `Ctrl+P` |
| **離開** | `/exit`（別名 `/quit`、`/q`），或 `Ctrl+X` `q` |
| **接 provider** | `/connect` |

### 1.2 兩個 opencode 特有的操作

| 操作 | 按鍵 | 說明 |
| :--- | :--- | :--- |
| **切換 agent** | `Tab` | 在 **Build**（全工具）與 **Plan**（編輯與 bash 要核准）之間循環 |
| **快捷鍵 leader** | `Ctrl+X` | 所有快捷鍵都是「先 `Ctrl+X`，再按第二個鍵」 |

> 💡 **分析課的建議動線**：階段 00~03 用 **Plan**（它不會亂改檔案），
> 到階段 02+ 要真的跑數字、寫腳本時按 `Tab` 切到 **Build**。

### 1.3 非互動模式（跑批次用）

```bash
opencode run "讀 AGENTS.md 第 3 節，產出 online_retail_09_10.csv 的數據卡到 reports/"
```

依官方文件，`run` 是「Run opencode in non-interactive mode by passing a prompt directly」。

---

## 2. 設定與元件責任

### 2.1 檔案位置一覽

```text
your-project/
├── AGENTS.md                  # 專案契約 —— opencode 原生讀這份
├── opencode.json              # 專案設定（模型、MCP、權限、instructions）
└── .opencode/
    └── agents/                # 專案層級的自訂 agent
        └── <agent-name>.md

~/.config/opencode/
├── AGENTS.md                  # 你個人的跨專案偏好
├── opencode.json              # 全域設定
├── tui.json                   # TUI 設定
└── agents/                    # 全域自訂 agent
```

### 2.2 元件責任對照表

| 元件 / 檔案 | 路徑 | 責任與使用時機 |
| :--- | :--- | :--- |
| **專案契約** | `AGENTS.md`（專案根目錄） | 長期 context 與專案規範。**本 repo 已經有了** |
| **個人偏好** | `~/.config/opencode/AGENTS.md` | 跨所有專案的個人習慣，不進版控 |
| **專案設定** | `opencode.json` / `opencode.jsonc` | 模型、provider、MCP、權限、額外要載入的指令檔 |
| **自訂 agent** | `.opencode/agents/<name>.md` | 專屬角色（例如「稽核員」），檔名就是 agent 名稱 |
| **MCP** | `opencode.json` 的 `mcp` 區塊 | 外部工具與資料連線 |

> ⚠️ **官方文件對自訂 agent 目錄的寫法**是 `.opencode/agents/` 與 `~/.config/opencode/agents/`。
> 你的版本若不吃這個路徑，用 `opencode agent list` 確認它實際認得哪些，
> 或直接用 `opencode agent create` 讓它自己建到正確位置。

### 2.3 opencode 怎麼找專案契約

依官方 rules 文件：

```text
1.【專案】從當前目錄往上找，第一個命中的 AGENTS.md
          （找不到 AGENTS.md 才退而找 CLAUDE.md）
2.【全域】~/.config/opencode/AGENTS.md
3.【相容】~/.claude/CLAUDE.md（除非你關掉）
```

每一類裡「第一個命中的檔案」勝出。官方舉的例子：本地同時有 `AGENTS.md` 與 `CLAUDE.md` 時，
**只載入 `AGENTS.md`**。

**對本 repo 來說這正好** —— 我們的 `CLAUDE.md` 只是給 Claude Code 用的轉接層，
opencode 直接讀真正的 `AGENTS.md`，不會讀到轉接層。

> 🚨 **不要在本 repo 跑 `/init`。** 那會產生或更新 `AGENTS.md`，
> 而本 repo 已經有一份寫好的了。

### 2.4 `opencode.json` 常用選項

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-5",
  "small_model": "anthropic/claude-haiku-4-5",
  "instructions": ["上課用prompt/分析師武器庫.md"]
}
```

| 選項 | 用途 |
| :--- | :--- |
| `model` | 主要模型 |
| `small_model` | 輕量任務用的另一顆模型 |
| `provider` | Provider 設定與認證 |
| `agent` | 定義專用 agent |
| `default_agent` | 沒指定時用哪個 agent |
| `tools` | 開關個別工具（如 `write`、`bash`） |
| `permission` | 哪些操作需要核准 |
| `instructions` | 額外要一起載入的指令檔（路徑或 glob） |
| `mcp` | MCP server 設定 |

> `$schema` 那一行不是裝飾 —— 加了之後編輯器才有自動補完與欄位驗證。

### 2.5 自訂一個 agent

依官方文件，agent 是 markdown 檔，**檔名就是 agent 名稱**
（`review.md` → `review` agent）：

```markdown
---
description: 稽核報告中的每一個量化陳述，逐項用另一種算法重算。交付分析報告前使用。
mode: subagent
temperature: 0
---

你是資料稽核員。你的工作不是幫報告講得更好聽，而是找出站不住腳的數字。
每個數字都先假設它是錯的，直到你親手用**另一種算法**把它算出來為止。
判定只用四級：✅ 通過 / ⚠️ 有出入 / ❌ 無法驗證 / 🚨 杜撰。不要打分數。
```

| Frontmatter 欄位 | 必填 | 說明 |
| :--- | :--- | :--- |
| `description` | ✅ | 決定它何時被叫用 |
| `mode` | ❌ | `subagent`、`primary` 或 `all` |
| `model` | ❌ | 這個 agent 專用的模型 |
| `temperature` / `top_p` | ❌ | 取樣參數 |
| `permission` | ❌ | 這個 agent 的權限 |
| `steps` | ❌ | 步數上限 |
| `color` / `hidden` | ❌ | 顯示相關 |

> 也可以用 `opencode agent create` 互動式建立，省得記路徑。

### 2.6 MCP server

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-local-server": {
      "type": "local",
      "command": ["npx", "-y", "my-mcp-command"],
      "enabled": true,
      "environment": { "MY_ENV_VAR": "value" }
    },
    "my-remote-server": {
      "type": "remote",
      "url": "https://my-mcp-server.com",
      "enabled": true,
      "headers": { "Authorization": "Bearer MY_API_KEY" }
    }
  }
}
```

> 🚨 **不要把真的 API key 寫死在 `opencode.json` 裡再 commit。**
> 這個檔案通常會進版控。用環境變數，或把含密鑰的設定放在
> `~/.config/opencode/opencode.json`（全域、不進版控）。

管理指令：`opencode mcp list` / `auth <server>` / `logout <server>` / `debug <server>`。

---

## 3. 課堂上真正會用到的指令

### 3.1 TUI 斜線指令

| 指令 | 說明（官方原文轉述） | 什麼時候用 |
| :--- | :--- | :--- |
| **`/new`**（別名 `/clear`） | 開新 session | **換階段時用。** 階段 01 做完要開始階段 02+ |
| **`/compact`**（別名 `/summarize`） | 壓縮目前 session | 對話很長但還想接著同一條線做 |
| **`/sessions`**（別名 `/resume`、`/continue`） | 列出與切換 session | 昨天做到一半 |
| **`/undo`** / **`/redo`** | 復原上一則訊息並**還原檔案變更** / 重做 | agent 改壞了東西 |
| **`/models`** | 列出可用模型 | 想換一顆模型當稽核員 |
| **`/connect`** | 加入 provider | 第一次設定，或要多接一家 |
| **`/export`** | 匯出對話成 Markdown 並用預設編輯器開啟 | 要把分析過程交出去當佐證 |
| **`/details`** | 切換工具執行細節的顯示 | 想看它到底跑了什麼指令 |
| **`/thinking`** | 切換思考／推理區塊的顯示 | 想理解它為什麼這樣分析 |
| **`/editor`** | 開外部編輯器撰寫訊息 | 要貼一大段前一階段的產出時 |
| **`/share`** / **`/unshare`** | 分享／取消分享目前 session | 🚨 分享等於公開，**不要分享含公司資料的對話** |
| **`/init`** | 引導式建立或更新 `AGENTS.md` | 🚨 **本 repo 已經有了，不要在這裡跑** |
| **`/themes`** | 列出佈景主題 | — |
| **`/help`** | 開說明對話框 | — |
| **`/exit`**（別名 `/quit`、`/q`） | 離開 | — |

### 3.2 快捷鍵（leader key 是 `Ctrl+X`）

| 按鍵 | 作用 |
| :--- | :--- |
| `Tab` | **切換 agent（Build ↔ Plan）** |
| `Ctrl+P` | 命令面板 |
| `Ctrl+X` `n` | 開新 session |
| `Ctrl+X` `l` | 列出／切換 session |
| `Ctrl+X` `c` | 壓縮 session |
| `Ctrl+X` `m` | 列出模型 |
| `Ctrl+X` `u` / `r` | 復原 / 重做 |
| `Ctrl+X` `e` | 開外部編輯器 |
| `Ctrl+X` `x` | 匯出對話 |
| `Ctrl+X` `t` | 列出佈景主題 |
| `Ctrl+X` `q` | 離開 |

### 3.3 CLI 子命令

| 命令 | 說明（官方原文轉述） |
| :--- | :--- |
| `opencode run` | 非互動模式，直接傳一個 prompt |
| `opencode models` | 列出所有已設定 provider 的可用模型 |
| `opencode auth login` / `list` / `logout` | 管理 provider 憑證 |
| `opencode agent create` / `list` | 建立／列出自訂 agent |
| `opencode session list` / `delete` | 管理 session |
| `opencode mcp list` / `auth` / `logout` / `debug` | 管理 MCP server |
| `opencode stats` | 顯示 token 用量與費用統計 |
| `opencode export` / `import` | 匯出／匯入 session 資料 |
| `opencode serve` / `web` / `attach` | 起 headless server / 帶網頁介面 / 接上已在跑的後端 |
| `opencode upgrade` | 更新到最新版 |
| `opencode uninstall` | 解除安裝並移除所有相關檔案 |

---

## 4. 學生實戰建議

1. **先跑 `opencode models` 確認 provider 接好了。**
   opencode 不綁模型，所以「裝完」不等於「能用」。列得出模型才算真的裝好。

2. **用 `Tab` 管住 agent 的手。**
   階段 00~03 是思考與規劃，用 **Plan** 就好，它不會動你的檔案。
   到階段 02+ 才切 **Build**。這比事後用 `/undo` 救可靠。

3. **每個階段開一段新 session。**
   六階段各自有明確的輸入與產出。用 `/new` 分段，把上一階段的產出當文字貼進去
   （長內容用 `/editor` 或 `Ctrl+X` `e` 貼比較舒服）。

4. **`/undo` 會還原檔案，不只是還原對話。**
   這是 opencode 一個很實用的差異。agent 改壞了東西時，這比手動 `git checkout` 快。

5. **不要在本 repo 跑 `/init`。**
   `AGENTS.md` 已經寫好了，跑 `/init` 可能會覆蓋掉。
   萬一跑了：`git diff AGENTS.md` 看變更，`git checkout AGENTS.md` 還原。

6. **分享功能要小心。**
   `/share` 會把 session 變成可分享的連結。課程練習資料沒關係，
   但**不要分享任何含公司實際資料的對話**。

7. **路徑區隔。**
   opencode 讀 `AGENTS.md`、`opencode.json` 與 `.opencode/`，
   **不會讀 `.agents/`（Antigravity）或 `~/.codex/`（Codex）**。
   不過它會 fallback 到 `~/.claude/CLAUDE.md` —— 這是唯一的跨工具例外。

---

## 下一步

- 安裝與環境驗證 → [`INSTALL.md`](./INSTALL.md)
- 選擇其他 agent、四款對照 → [`../README.md`](../README.md)
- 回到分析主線 → [`上課用prompt/index.html`](../../上課用prompt/index.html)
