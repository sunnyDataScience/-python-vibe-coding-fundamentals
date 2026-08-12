# 安裝 SOP：Claude Code（`claude`）

> 本文是學生在乾淨環境下**照著做就能裝完**的操作手冊與環境檢查指南。
>
> - 標「**依官方文件**」的：取自 `code.claude.com/docs` 官方文件。
> - 標「**本機實測**」的：在本教材開發機（Ubuntu 22.04 / x86_64）實際執行過的輸出。
> - 標「**範例輸出**」的：乾淨 Linux / macOS 環境下的標準預期結果。
> - 標「⚠️ 官方文件未載明」的：官方未明確紀錄，操作時需多加注意。
>
> 唯一可信來源：`code.claude.com/docs`。第三方部落格一律不採用。
> 四款 agent 的比較與選擇建議見 [`../README.md`](../README.md)。

---

## 0. 先讀這段

### 0.1 你需要一個付費帳號

**這是最容易卡住的一點，先確認再花時間裝。**

依官方文件：Claude Code 需要 **Pro、Max、Team、Enterprise 或 Console 帳號**。
**免費的 Claude.ai 方案不包含 Claude Code 存取權。**

也可以改走第三方 API 供應商（Amazon Bedrock、Google Cloud Agent Platform、Microsoft Foundry），
但那需要企業雲端帳號，不在本教材範圍。

> 沒有以上任何一種帳號的話，先看 [`../README.md`](../README.md) 第 2 節挑另一款工具，
> 不要先裝完才發現登不進去。

### 0.2 Headless / SSH 環境可以用

Claude Code 是**純終端機工具**，沒有圖形介面需求。
Remote SSH、Headless Linux、WSL 都是官方支援的正常用法 ——
這一點跟 Antigravity IDE 不同，不需要挑環境。

登入時會嘗試開瀏覽器；SSH 環境開不了瀏覽器時的處置見 2.4。

### 0.3 選哪一種安裝方式

依官方文件，共有五種安裝管道。**課堂上請用 Native Install（原生安裝）**：

| 管道 | 自動更新 | 什麼時候選 |
| :--- | :--- | :--- |
| **Native（curl / PowerShell）** | ✅ 背景自動更新 | **預設選這個。** 不需要 Node.js |
| Homebrew | ❌ 需手動 `brew upgrade` | 你已經用 brew 管所有工具 |
| WinGet | ❌ 需手動 `winget upgrade` | Windows 且習慣 WinGet |
| npm | ⚠️ 需 Node.js 22+ | 你已經有 Node 環境且偏好 npm 管理 |
| apt / dnf / apk | ❌ 走系統升級流程 | 需要簽章驗證的企業環境 |

> Native 安裝**不需要 Node.js**。npm 管道裝的是同一個原生執行檔，
> Node 只用在安裝當下，`claude` 執行時不會呼叫 Node。

---

## 1. 前置檢查

**整段貼進終端機執行：**

```bash
# 1. 作業系統與架構
grep PRETTY_NAME /etc/os-release 2>/dev/null || sw_vers 2>/dev/null
uname -m

# 2. 記憶體（官方需求 4GB+）
free -g 2>/dev/null | awk '/^Mem:/{print "RAM: " $2 " GB"}' || echo "RAM: 非 Linux，請自行確認 ≥ 4GB"

# 3. ~/.local/bin 在不在 PATH（決定裝完能不能直接執行 claude）
case ":$PATH:" in *":$HOME/.local/bin:"*) echo "PATH OK: ~/.local/bin 已在 PATH";; *) echo "PATH MISSING";; esac

# 4. 是不是 SSH session（決定登入走哪條路）
echo "SSH_CONNECTION=[${SSH_CONNECTION:-未設定}]"

# 5. 現況
command -v claude || echo "claude: 尚未安裝"
ls -d ~/.claude 2>/dev/null || echo "~/.claude 不存在（全新安裝）"
```

**乾淨環境下的預期範例輸出**

```
PRETTY_NAME="Ubuntu 22.04.5 LTS"
x86_64
RAM: 15 GB
PATH OK: ~/.local/bin 已在 PATH
SSH_CONNECTION=[未設定]
claude: 尚未安裝
~/.claude 不存在（全新安裝）
```

**逐項判讀**

| # | 檢查 | 應該看到 | 不符合怎麼辦 |
|---|---|---|---|
| 1 | 發行版 / 架構 | 依官方文件支援：macOS 13.0+、Windows 10 1809+／Server 2019+、Ubuntu 20.04+、Debian 10+、Alpine 3.19+；`x64` 或 `ARM64` | 低於這些版本官方不支援。Alpine 另有額外步驟，見 3.2 |
| 2 | 記憶體 | `≥ 4 GB` | 低於 4GB 官方未列為支援配置 |
| 3 | PATH | `PATH OK` | 顯示 `PATH MISSING` 時，裝完會 `command not found`。見第 5 節第 1 項 |
| 4 | `SSH_CONNECTION` | 有值 = 在 SSH session 內 | 有值代表登入時瀏覽器不會自動開啟，見 2.4 |
| 5 | `command -v claude` | 有輸出 = 已安裝 | 顯示「尚未安裝」代表可進行乾淨安裝 |

**還需要什麼**

- **網路連線**（官方需求；企業防火牆環境見官方 network-config 文件）
- **所在地區**須在 Anthropic 支援國家清單內
- **shell**：Bash、Zsh、PowerShell 或 CMD
- **ripgrep**：依官方文件「usually included with Claude Code」，通常不用自己裝

---

## 2. 安裝 `claude`

### 2.1 安裝命令（逐字照抄官方）

**macOS / Linux / WSL：**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

其他管道（同樣逐字照抄官方）：

| 平台 / 管道 | 命令 |
|---|---|
| Windows PowerShell | `irm https://claude.ai/install.ps1 \| iex` |
| Windows CMD | `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` |
| Homebrew | `brew install --cask claude-code` |
| WinGet | `winget install Anthropic.ClaudeCode` |
| npm | `npm install -g @anthropic-ai/claude-code` |

> 💡 **分不清自己在 PowerShell 還是 CMD**：提示字元開頭有 `PS` 的是 PowerShell。
> 官方也給了反向判斷：看到 `The token '&&' is not a valid statement separator` 代表你在 PowerShell；
> 看到 `'irm' is not recognized` 代表你在 CMD。

**依官方文件**，macOS / Linux 的原生安裝會把 launcher 放在 **`~/.local/bin/claude`**，
它是一個指向 `~/.local/share/claude/versions/` 的 symlink。

> 🚨 **不要用 `sudo npm install -g`。** 官方明確警告這會造成權限問題與安全風險。

### 2.2 想裝特定版本或穩定頻道

依官方文件，原生安裝器接受版本號或頻道名（`latest` / `stable`）：

```bash
curl -fsSL https://claude.ai/install.sh | bash -s stable      # 穩定頻道（約落後一週）
curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89      # 指定版本
```

安裝當下選的頻道會成為之後自動更新的預設值。
Homebrew 則是用 cask 名稱區分：`claude-code` 走 stable、`claude-code@latest` 走 latest。

### 2.3 驗證安裝

```bash
claude --version
```

**依官方文件應看到**：一組版本號，例如 `2.1.211 (Claude Code)`。

**本機實測**（2026-08，開發機）：

```
2.1.228 (Claude Code)
```

更完整的健檢（不啟動 session，只印診斷）：

```bash
claude doctor
```

依官方文件，`claude doctor` 會印出安裝健康度、設定檔驗證錯誤、以及最近一次更新嘗試的結果。
**裝完之後、上課之前跑一次，比事後除錯省時間。**

### 2.4 登入

依官方文件：安裝完成後執行 `claude`，跟著瀏覽器提示登入即可。

```bash
claude
```

| 情況 | 依官方文件的行為 |
|---|---|
| 一般本機 | 開啟瀏覽器完成登入 |
| 已設 `ANTHROPIC_API_KEY` 環境變數 | **不開瀏覽器**，改為提示你確認是否使用該金鑰（只問一次） |

> ⚠️ **官方 setup 文件未載明 SSH / Headless 環境的專用登入流程。**
> 實務上瀏覽器無法自動開啟時，終端機會印出登入 URL，複製到你自己筆電的瀏覽器完成後，
> 依提示把結果貼回終端機。**本文不編造該流程的逐字畫面** ——
> 若你的版本沒有印出可複製的 URL，見第 5 節第 3 項。

### 2.5 確認它活著

在任一專案目錄執行 `claude` 進入互動介面，輸入：

```
/help
```

**應看到**：可用斜線指令與快捷鍵的清單。

離開：`/exit`，或按 `Ctrl+D`。

---

## 3. 平台特別注意事項

### 3.1 Windows：原生還是 WSL

依官方文件，兩條路的差別在**沙箱**：

| 選項 | 需要 | 沙箱支援 | 什麼時候用 |
|---|---|---|---|
| 原生 Windows | 無（Git for Windows 選配） | ❌ 不支援 | Windows 原生專案與工具 |
| WSL 2 | 啟用 WSL 2 | ✅ 支援 | Linux 工具鏈，或需要沙箱執行指令 |
| WSL 1 | 啟用 WSL 1 | ❌ 不支援 | WSL 2 不可用時 |

原生 Windows 安裝 [Git for Windows](https://git-scm.com/downloads/win) 是**選配但建議** ——
有裝的話 Claude Code 用 Git Bash 執行 Bash 工具，沒裝則改用 PowerShell 工具。

走 WSL 的話：在 WSL 終端機裡跑 Linux 安裝命令，並且在 WSL 裡啟動 `claude`，
**不是**從 PowerShell 或 CMD 啟動。

### 3.2 Alpine / musl 系發行版

依官方文件，Alpine 預設沒有 `bash` 與 `curl`，安裝命令會直接失敗。先補套件：

```bash
apk add bash curl libgcc libstdc++ ripgrep
```

然後在 `settings.json` 設 `USE_BUILTIN_RIPGREP` 為 `0`：

```json
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

> `ripgrep` 在 Alpine 的 community repository。`apk` 說找不到套件時，
> 依你的 Alpine 版本把 community repo 加進 `/etc/apk/repositories`，`apk update` 後重試。

---

## 4. 把本 repo 的 harness 接上

### 4.1 Claude Code 不讀 `AGENTS.md`

**依官方文件（原文）**：「Claude Code reads `CLAUDE.md`, not `AGENTS.md`.」

官方給的接法是寫一個 `CLAUDE.md` 去 import `AGENTS.md`：

```markdown
@AGENTS.md

## Claude Code 專屬補充
（只寫 AGENTS.md 沒有的部分）
```

**本 repo 已經是這個結構，你不需要自己建立。** 根目錄 `CLAUDE.md` 的內容就是
「`@AGENTS.md` ＋ Claude Code 專屬補充」，所以資料集契約與分析鐵律會自動載入。

> 官方也提供 symlink 寫法（`ln -s AGENTS.md CLAUDE.md`），但那樣就沒地方寫工具專屬補充了。
> 本 repo 兩者都需要，所以走 import。Windows 建立 symlink 需要管理員權限或開發者模式，
> 也是走 import 比較省事。

### 4.2 確認契約真的載入了

在 **repo 根目錄**啟動 `claude`，輸入：

```
/context
```

**應看到**：`Memory files` 區塊列出 `CLAUDE.md`。
沒列出來代表沒讀到 —— 先 `pwd` 確認你在 repo 根目錄。

接著跑 [`../README.md`](../README.md#3-裝完之後先做這個驗收) 第 3 節的驗收提問，
它會直接測出契約內容有沒有進到 context。

### 4.3 本 repo 用得到的路徑

| 路徑 | 角色 |
|---|---|
| `CLAUDE.md`（repo 根目錄） | 專案指令。本 repo 用它 import `AGENTS.md` |
| `AGENTS.md`（repo 根目錄） | 跨工具的真正契約來源 |
| `~/.claude/CLAUDE.md` | 你個人的跨專案偏好 |
| `.claude/rules/*.md` | 模組化的專案規範，可用 `paths:` frontmatter 限定只在碰到特定檔案時載入 |
| `.claude/settings.json` | 專案設定（權限、環境變數等） |
| `.mcp.json` | 專案層級 MCP server 設定 |

依官方文件，`CLAUDE.md` 建議**控制在 200 行以內** —— 太長會吃掉 context 也降低遵循度。
內容要分拆時用 `.claude/rules/`，不要一直往 `CLAUDE.md` 塞。

> `@path` import 最多遞迴 **4 層**。想在 `CLAUDE.md` 裡提到一個路徑但不要 import 它，
> 用反引號包起來：寫 `` `@README` `` 是純文字，`@README` 才會被 import。

---

## 5. 卡住就看這裡

| # | 症狀 | 原因 | 處置 |
|---|---|---|---|
| 1 | `claude: command not found`（但裝好了） | 執行檔在 `~/.local/bin/claude`，該路徑不在 shell PATH | 先 `ls -l ~/.local/bin/claude` 確認檔案在。在的話把 `export PATH="$HOME/.local/bin:$PATH"` 加進 `~/.bashrc`（或 `~/.zshrc`）再 `source` |
| 2 | 登入被擋，訊息提到 plan / subscription | 用的是免費 Claude.ai 帳號 | 依官方文件，Claude Code 需要 Pro / Max / Team / Enterprise / Console。免費方案不含。見 0.1 |
| 3 | SSH 進來登入，瀏覽器開不起來 | Headless 環境沒有可開啟的瀏覽器 | 終端機通常會印出可複製的登入 URL，複製到自己筆電完成登入。⚠️ 官方 setup 文件未載明此流程細節；完全沒有 URL 出現時，改在有桌面的機器登入 |
| 4 | 安裝命令報 `syntax error near unexpected token '<'` 或 `403` | curl 抓到的不是腳本（通常是網路中介或代理回傳了 HTML） | 官方有專門的 troubleshoot-install 頁面對照錯誤訊息。先確認網路能直接連到 `claude.ai` |
| 5 | 搜尋功能失效 | `ripgrep` 缺失 | 通常隨附。Alpine / musl 環境見 3.2，需自行 `apk add ripgrep` 並設 `USE_BUILTIN_RIPGREP=0` |
| 6 | npm 安裝後找不到執行檔 | npm 透過 per-platform optional dependency 拉原生 binary，你的套件管理器可能停用了 optional deps | 確認套件管理器允許 optional dependencies。支援平台：`darwin-arm64`、`darwin-x64`、`linux-x64`、`linux-arm64`、`linux-x64-musl`、`linux-arm64-musl`、`win32-x64`、`win32-arm64` |
| 7 | npm 安裝時出現 `EBADENGINE` 警告 | npm 套件自 v2.1.198 起要求 Node.js 22+ | 依官方文件這只是警告不是失敗：安裝會完成，`claude` 也能跑，因為它跑的是原生 binary 不用 Node。想消掉警告就升級 Node |
| 8 | 裝了但 `/context` 看不到 `CLAUDE.md` | 沒有在 repo 根目錄啟動 | `pwd` 確認位置。Claude Code 是從當前目錄往上找 `CLAUDE.md`，在子目錄啟動仍會找到根目錄那份，但在 repo 之外啟動就不會 |
| 9 | 更新沒生效 | 背景更新在下次啟動才套用 | `claude doctor` 會印出最近一次更新嘗試的結果。要立刻更新就跑 `claude update` |
| 10 | 移除後 `claude` 還在 | 有第二份安裝，或舊安裝器留下的 shell alias | 官方 troubleshoot-install 有「Check for conflicting installations」一節。先 `command -v claude` 看它指到哪 |

---

## 6. 更新與解除安裝

### 6.1 更新

原生安裝**會背景自動更新**。要立刻更新：

```bash
claude update
```

Homebrew / WinGet / apt / dnf / apk 安裝**不會自動更新**，需手動：

| 管道 | 命令 |
|---|---|
| Homebrew | `brew upgrade claude-code`（或 `brew upgrade claude-code@latest`） |
| WinGet | `winget upgrade Anthropic.ClaudeCode` |
| npm | `npm install -g @anthropic-ai/claude-code@latest` |

> ⚠️ npm 請勿用 `npm update -g` —— 官方說明它會受原始安裝的 semver range 限制，可能不會更新到最新版。

想關掉自動更新，在 `settings.json` 的 `env` 設 `DISABLE_AUTOUPDATER` 為 `"1"`。

### 6.2 移除執行檔

**原生安裝（macOS / Linux / WSL）：**

```bash
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```

其他管道：

| 管道 | 命令 |
|---|---|
| Homebrew | `brew uninstall --cask claude-code` |
| WinGet | `winget uninstall Anthropic.ClaudeCode` |
| npm | `npm uninstall -g @anthropic-ai/claude-code` |
| apt | `sudo apt remove claude-code` |

### 6.3 移除設定與資料

> 🚨 **先讀完再決定。** 依官方文件，刪掉這些會失去你所有設定、允許的工具清單、
> MCP server 設定與 session 歷史。

```bash
# 使用者層級設定與狀態
rm -rf ~/.claude
rm ~/.claude.json

# 專案層級設定（在專案目錄執行）
rm -rf .claude
rm -f .mcp.json
```

> ⚠️ VS Code 擴充、JetBrains plugin 與桌面版 App **也會寫入 `~/.claude/`**。
> 只要其中任何一個還裝著，這個目錄下次執行時就會被重建。
> 要完全移除，得先把那些也解除安裝。

---

## 下一步

裝完 `claude` 之後：

1. **學指令與 `.claude` 設定** → [`CLI_GUIDE.md`](./CLI_GUIDE.md)
2. **跑一次驗收，確認契約載入** → [`../README.md`](../README.md#3-裝完之後先做這個驗收)
3. **回到分析主線** → [`上課用prompt/index.html`](../../上課用prompt/index.html)
   或 [`上課用prompt/分析師武器庫.md`](../../上課用prompt/分析師武器庫.md)
