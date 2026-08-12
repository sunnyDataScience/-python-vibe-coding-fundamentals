# 安裝 SOP：Codex CLI（`codex`）

> 本文是學生在乾淨環境下**照著做就能裝完**的操作手冊與環境檢查指南。
>
> - 標「**依官方文件**」的：取自 `developers.openai.com/codex`（會轉址到 `learn.chatgpt.com/docs`）
>   與 `github.com/openai/codex` 官方倉庫。
> - 標「**本機實測**」的：在本教材開發機（Ubuntu 22.04 / x86_64、`codex-cli 0.146.0`）實際執行過的輸出。
> - 標「**範例輸出**」的：乾淨 Linux / macOS 環境下的標準預期結果。
> - 標「⚠️ 官方文件未載明」的：官方未明確紀錄，操作時需多加注意。
>
> 唯一可信來源：OpenAI 官方站台與 `openai/codex` 倉庫。第三方部落格一律不採用。
> 四款 agent 的比較與選擇建議見 [`../README.md`](../README.md)。

---

## 0. 先讀這段

### 0.1 你需要什麼帳號

依官方文件，Codex CLI 的主要登入方式是 **Sign in with ChatGPT** ——
用你既有的 ChatGPT 訂閱，不必另外辦 API 帳號。

也可以改用 **OpenAI API key**（見 2.4），走用量計費。

> 💡 **已經有 ChatGPT Plus / Pro 的人，這是四款裡最快上手的一款** ——
> 不用開通新服務、不用綁信用卡、`codex` 一跑就進登入流程。

### 0.2 Headless / SSH 環境可以用

Codex CLI 是純終端機工具，沒有圖形介面需求。Remote SSH、Headless Linux 都是正常用法。

### 0.3 這份文件裡的「本機實測」是什麼版本

**本機實測**（2026-08）：

```
codex-cli 0.146.0
```

Codex 更新頻繁，你裝到的版本會比較新。**若官方文件或 `codex --help` 與本文衝突，以它們為準。**

---

## 1. 前置檢查

**整段貼進終端機執行：**

```bash
# 1. 作業系統與架構
grep PRETTY_NAME /etc/os-release 2>/dev/null || sw_vers 2>/dev/null
uname -m

# 2. ~/.local/bin 在不在 PATH（決定裝完能不能直接執行 codex）
case ":$PATH:" in *":$HOME/.local/bin:"*) echo "PATH OK: ~/.local/bin 已在 PATH";; *) echo "PATH MISSING";; esac

# 3. 是不是 SSH session
echo "SSH_CONNECTION=[${SSH_CONNECTION:-未設定}]"

# 4. 現況
command -v codex || echo "codex: 尚未安裝"
ls -d ~/.codex 2>/dev/null || echo "~/.codex 不存在（全新安裝）"
```

**乾淨環境下的預期範例輸出**

```
PRETTY_NAME="Ubuntu 22.04.5 LTS"
x86_64
PATH OK: ~/.local/bin 已在 PATH
SSH_CONNECTION=[未設定]
codex: 尚未安裝
~/.codex 不存在（全新安裝）
```

**逐項判讀**

| # | 檢查 | 應該看到 | 不符合怎麼辦 |
|---|---|---|---|
| 1 | 發行版 / 架構 | 依官方倉庫，支援 macOS（Apple Silicon `arm64` 與 `x86_64`）、Linux（`x86_64` 與 `arm64`）、Windows | ⚠️ **官方未載明最低 OS 版本與最低記憶體**，本文不編造。架構不在上表之列就沒有官方 binary |
| 2 | PATH | `PATH OK` | 顯示 `PATH MISSING` 時，用 curl 裝完會 `command not found`。見第 5 節第 1 項 |
| 3 | `SSH_CONNECTION` | 有值 = 在 SSH session 內 | 有值代表登入時瀏覽器不會自動開啟，見 2.4 |
| 4 | `command -v codex` | 有輸出 = 已安裝 | 顯示「尚未安裝」代表可進行乾淨安裝 |

> **沒有 Node.js 檢查。** curl 與 brew 管道不需要 Node；只有走 npm 管道才需要。

---

## 2. 安裝 `codex`

### 2.1 安裝命令（逐字照抄官方）

**macOS / Linux：**

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

其他管道（同樣逐字照抄官方）：

| 平台 / 管道 | 命令 |
|---|---|
| Windows PowerShell | `powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 \| iex"` |
| npm | `npm install -g @openai/codex` |
| Homebrew | `brew install --cask codex` |

> 🚨 **不要用 `sudo npm install -g`。** 全域安裝加 sudo 會造成權限與安全問題，
> 這對所有 npm 全域套件都成立。遇到權限錯誤時改用 curl 管道，不要加 sudo 硬上。

**本機實測**：curl 管道裝完後執行檔在 `~/.local/bin/codex`。
⚠️ 官方文件未逐字載明安裝路徑，上面是本機實測結果，你的系統可能不同 ——
用第 2.2 節的 `command -v codex` 確認實際位置。

### 2.2 驗證安裝

```bash
command -v codex
codex --version
```

**本機實測**：

```
/home/<你的帳號>/.local/bin/codex
codex-cli 0.146.0
```

更完整的健檢：

```bash
codex doctor
```

依 `codex --help`，`doctor` 會「Diagnose local Codex installation, config, auth, and runtime health」。
**裝完之後、上課之前跑一次。**

### 2.3 登入

最簡單的方式是直接跑 `codex`，依官方文件在首次啟動時選 **Sign in with ChatGPT**：

```bash
codex
```

也可以走 CLI 子命令：

| 動作 | 命令 |
|---|---|
| 登入 | `codex login` |
| **查目前登入狀態** | `codex login status` |
| 登出（清除憑證） | `codex logout` |

**本機實測** `codex login status` 的輸出：

```
Logged in using ChatGPT
```

### 2.4 改用 API key

依 `codex login --help`，API key 從 **stdin** 讀入，不是當參數傳：

```bash
printenv OPENAI_API_KEY | codex login --with-api-key
```

> 💡 **為什麼要用 stdin**：把 key 寫在命令列會被記進 shell history，
> 也會出現在 `ps` 的 process 列表裡。這個設計是刻意的，照著用。

還有一個 `--with-access-token`，同樣從 stdin 讀：

```bash
printenv CODEX_ACCESS_TOKEN | codex login --with-access-token
```

### 2.5 SSH / Headless 環境的登入

⚠️ **官方文件未載明 Headless 專用的登入流程。**

**本機實測**：在 SSH session 中登入是可行的（本開發機即為 SSH 環境且已登入）。
若你的環境開不了瀏覽器，最穩的做法是走 2.4 的 API key 流程 —— 它完全不需要瀏覽器。

### 2.6 確認它活著

在專案目錄執行 `codex` 進入互動介面，然後：

- 輸入 `/` 會列出可用的斜線指令
- 輸入 `/init` 會產生 `AGENTS.md` 骨架（**本 repo 已經有了，不要在本 repo 跑這個**）
- 按 `Ctrl+C` 或輸入 `/exit` 離開

---

## 3. 兩個上課前該先懂的設定

Codex 跟其他三款最大的差別是**它預設就有沙箱與核准機制**。搞不清楚這兩個，
你會覺得它一直卡住不動手。

### 3.1 沙箱（`-s` / `--sandbox`）

依 `codex --help`，可選值有三個：

| 值 | 意思 |
|---|---|
| `read-only` | 只能讀，不能寫檔案 |
| `workspace-write` | 可以寫工作目錄 |
| `danger-full-access` | 完全不設限 |

跑本教材的分析流程需要**寫得了 `reports/`、`scripts/`、`charts/`**，所以至少要 `workspace-write`：

```bash
codex -s workspace-write
```

### 3.2 核准政策（`-a` / `--ask-for-approval`）

依 `codex --help`，可選值有三個（以下為官方原文轉述）：

| 值 | 意思 |
|---|---|
| `untrusted` | 只有「可信」命令（如 `ls`、`cat`、`sed`）不問就跑；模型提出不在可信集合裡的命令時，會升級給你核准 |
| `on-request` | 由模型決定何時要問你 |
| `never` | 永不詢問。執行失敗直接回報給模型 |

> 🚨 **另有一個 `--dangerously-bypass-approvals-and-sandbox`。**
> `--help` 的原文是「EXTREMELY DANGEROUS. Intended solely for running in environments that are
> externally sandboxed」—— **課堂上不要用。**
> 你的筆電不是「externally sandboxed 環境」。

也可以在互動介面裡用 `/permissions` 調整（「Set what Codex can do without asking first」）。

---

## 4. 把本 repo 的 harness 接上

### 4.1 Codex 原生讀 `AGENTS.md`

**這是好消息：本 repo 不需要任何額外設定。**

依官方 `agents-md` 指南，Codex 的讀取順序是：

**全域範圍**（Codex home，預設 `~/.codex`，可用 `CODEX_HOME` 改）
1. `AGENTS.override.md`（存在就讀它）
2. 否則讀 `AGENTS.md`

**專案範圍**（從 project root，通常是 git root，往下走到你的 cwd）
沿路每個目錄依序檢查：
1. `AGENTS.override.md`
2. `AGENTS.md`
3. `project_doc_fallback_filenames` 裡設定的備援檔名

**合併方式（官方原文轉述）**：由 root 往下串接，用空行相連。
**越靠近你當前目錄的檔案越晚出現在合併後的 prompt 裡，所以會覆蓋前面的指引。**

| 限制 | 值 |
|---|---|
| 空檔案 | 跳過 |
| 合併總大小上限 | `project_doc_max_bytes`，**預設 32 KiB**，達到上限就停止加入後續檔案 |

> ⚠️ **本 repo 的 `AGENTS.md` 約 12 KB**（本機實測 12,354 bytes），離 32 KiB 上限還有餘裕。
> 但如果你自己在子目錄又加了幾份 `AGENTS.md`，要留意這個上限 ——
> **超過的部分是被靜默丟掉的，不會有警告。**

### 4.2 確認契約真的載入了

在 **repo 根目錄**啟動 `codex`，跑
[`../README.md`](../README.md#3-裝完之後先做這個驗收) 第 3 節的驗收提問。

答得出 `20.5%` 與 `24.9%` 就代表契約有進到 context。

### 4.3 `~/.codex/` 裡有什麼

**本機實測**，這些是跟本教材有關的項目：

| 路徑 | 角色 |
|---|---|
| `~/.codex/config.toml` | 主設定檔（模型、沙箱預設值、fallback 檔名等） |
| `~/.codex/auth.json` | 🚨 **登入憑證。不要 commit、不要貼給任何人** |
| `~/.codex/AGENTS.md` | 你個人的跨專案偏好（依官方文件；**預設不存在，要自己建**） |
| `~/.codex/skills/` | 全域 skills |
| `~/.codex/rules/` | 全域規範 |
| `~/.codex/plugins/` | 已安裝的 plugin |
| `~/.codex/sessions/` | 對話歷史 |

想覆蓋單一設定而不改檔案，用 `-c`：

```bash
codex -c model="gpt-5.1-codex" -c shell_environment_policy.inherit=all
```

依 `--help`，`value` 會先當成 TOML 解析，解析失敗才當字串。

---

## 5. 卡住就看這裡

| # | 症狀 | 原因 | 處置 |
|---|---|---|---|
| 1 | `codex: command not found`（但裝好了） | 執行檔所在目錄不在 shell PATH | 先找出檔案位置。curl 管道**本機實測**落在 `~/.local/bin/codex`；把 `export PATH="$HOME/.local/bin:$PATH"` 加進 `~/.bashrc` 再 `source`。npm 管道則檢查 `npm bin -g` 的輸出在不在 PATH |
| 2 | agent 一直說沒權限寫檔，或分析腳本存不進 `scripts/` | 沙箱是 `read-only` | 用 `codex -s workspace-write` 啟動，或在互動介面用 `/permissions` 調整。見 3.1 |
| 3 | 每一個指令都要你按核准，跑不動 | 核准政策是 `untrusted` | 改 `-a on-request`。**不要**直接跳到 `--dangerously-bypass-approvals-and-sandbox`。見 3.2 |
| 4 | 分不清現在到底登入了沒 | — | `codex login status`。**本機實測**已登入時會印 `Logged in using ChatGPT` |
| 5 | SSH 環境登入卡住、瀏覽器開不起來 | Headless 沒有可開啟的瀏覽器 | ⚠️ 官方未載明 headless 流程。最穩的替代路徑是 2.4 的 `printenv OPENAI_API_KEY \| codex login --with-api-key`，完全不需要瀏覽器 |
| 6 | agent 不知道資料集欄位，開始猜 `Price` / `Customer ID` | 沒在 repo 根目錄啟動，或 `AGENTS.md` 沒被讀到 | `pwd` 確認位置。Codex 從 git root 往下讀，在 repo 之外啟動就讀不到。跑 4.2 的驗收確認 |
| 7 | 子目錄的 `AGENTS.md` 好像沒生效 | 合併總量超過 `project_doc_max_bytes`（預設 32 KiB） | 超出的部分會被**靜默丟掉**。精簡各層的 `AGENTS.md`，或在 `~/.codex/config.toml` 調高 `project_doc_max_bytes` |
| 8 | 想暫時換掉全域設定但不想刪檔 | — | 依官方文件建立 `~/.codex/AGENTS.override.md`，它會蓋過 `~/.codex/AGENTS.md`。用完刪掉即可還原 |
| 9 | 版本太舊 | — | `codex update`（依 `--help`：「Update Codex to the latest version」） |
| 10 | 說不上來哪裡怪 | — | `codex doctor`，它會一次檢查安裝、設定、認證與 runtime 健康度 |

---

## 6. 更新與解除安裝

### 6.1 更新

```bash
codex update
```

npm 與 Homebrew 管道另有各自的更新方式（`npm install -g @openai/codex@latest`、`brew upgrade --cask codex`）。

### 6.2 解除安裝

⚠️ **官方文件未載明解除安裝程序** —— 沒有 uninstall 子命令
（`codex --help` 的命令清單裡沒有）。以下是依實測安裝路徑整理的最小移除方式：

**步驟 1：先登出**（在移除執行檔前做）

```bash
codex logout
```

**步驟 2：移除執行檔**

```bash
rm -f "$(command -v codex)"
```

> npm 管道請改用 `npm uninstall -g @openai/codex`；
> Homebrew 管道請用 `brew uninstall --cask codex`。

**步驟 3：設定與資料目錄 `~/.codex/`**

> 🚨 **先讀完再決定。** `rm -rf ~/.codex` 會一次刪光：

| 路徑 | 刪掉會失去 |
|---|---|
| `config.toml` | 全部設定 |
| `auth.json` | 登入憑證（登出後本來就該清掉） |
| `AGENTS.md` | 你的全域偏好 |
| `skills/`、`rules/`、`plugins/` | 全域 skills、規範與已安裝 plugin |
| `sessions/`、`history.jsonl` | 全部對話歷史 |

只是想**重設而不是移除**的話，先只刪 `config.toml`，保留其他。

---

## 下一步

裝完 `codex` 之後：

1. **學指令與 `AGENTS.md` 設定** → [`CLI_GUIDE.md`](./CLI_GUIDE.md)
2. **跑一次驗收，確認契約載入** → [`../README.md`](../README.md#3-裝完之後先做這個驗收)
3. **回到分析主線** → [`上課用prompt/index.html`](../../上課用prompt/index.html)
   或 [`上課用prompt/分析師武器庫.md`](../../上課用prompt/分析師武器庫.md)
