# 安裝 SOP：Antigravity CLI（`agy`）

> 本文是學生在乾淨環境下**照著做就能裝完**的操作手冊與環境檢查指南。
>
> - 標「**依官方文件**」的：取自 `antigravity.google` 官方規格。
> - 標「**範例輸出**」的：乾淨 Linux / macOS 環境下執行命令的標準預期結果。
> - 標「⚠️ 官方文件未載明」的：官方站台未明確紀錄，操作時需多加注意。
>
> 唯一可信來源：`antigravity.google`。第三方部落格一律不採用。

---

## 0. 先讀這段

### 0.1 你的系統環境評估

| 目標 | 可否執行 | 判定依據 |
|---|---|---|
| **Antigravity CLI（`agy`）** | ✅ 可以 | macOS / Linux（Ubuntu 20.04+ / x86_64 或 aarch64）、glibc **≥ 2.28**、GLIBCXX **≥ 3.4.25** |
| **Antigravity IDE** | ⚠️ 需圖形介面 | 若 `DISPLAY` 與 `WAYLAND_DISPLAY` 都未設定且非 WSL —— 表示這是一台**沒有圖形介面**的 Linux 主機（SSH / Headless）。IDE 是 GUI 應用程式 |

若在 Headless / SSH 環境中跑 IDE 不是「設定沒調好」，而是沒有圖形介面可供顯示。

**兩條路線，依環境選擇：**

- **路線 A（本 repo 預設）**：在 Remote SSH / Headless Linux 環境下**只裝 `agy` CLI**，全程走終端機。
  本 repo 的 harness 以 CLI 為主，走這條不會少任何功能。
- **路線 B**：IDE 裝在有桌面環境的電腦（Apple Silicon Mac / Windows / 有 GUI 的 Linux），
  Headless 主機維持僅安裝 CLI。第 3 節是寫給有桌面環境看的。

### 0.2 為什麼是 `agy`，不是 `gemini`

本 repo 的 Antigravity 軌**不涵蓋 Gemini CLI**：自 **2026-06-18** 起對個人帳號
（free tier / Google AI Pro / Google AI Ultra）停止服務，官方指定改用 Antigravity CLI（`agy`）；
只有持有 **Gemini Code Assist Standard / Enterprise** 授權的組織不受影響 —— 那不是本教材的讀者。

所以本文從頭到尾只有一個工具：**`agy`**。

### 0.3 上課環境與全新安裝說明

如果你是第一次安裝，環境會是乾淨狀態：
- `~/.local/bin/agy` 未安裝
- `~/.gemini/` 不存在（全新安裝，無需遷移舊 Gemini CLI 設定）

若先前已安裝過 `agy`：
- `~/.local/bin/agy` 執行檔已存在
- `~/.gemini/` 為 Antigravity CLI 自己建立的設定與資料目錄（`~/.gemini` 目錄名稱為歷史包袱，Antigravity CLI 沿用它）。

請先執行 **第 1 節 前置檢查** 確認系統環境，再依步驟進行安裝與驗證。

---

## 1. 前置檢查

**整段貼進終端機執行，檢查系統環境：**

```bash
# 1. 作業系統與架構
grep PRETTY_NAME /etc/os-release
uname -m

# 2. glibc / libstdc++
ldd --version | head -1
strings /usr/lib/x86_64-linux-gnu/libstdc++.so.6 | grep -o 'GLIBCXX_3\.4\.[0-9]*' | sort -V | tail -1

# 3. 有沒有圖形介面（決定 IDE 能不能跑在此環境）
echo "DISPLAY=[${DISPLAY:-未設定}] WAYLAND_DISPLAY=[${WAYLAND_DISPLAY:-未設定}] WSL=[${WSL_DISTRO_NAME:-否}]"

# 4. ~/.local/bin 在不在 PATH（決定裝完能不能直接執行 agy）
case ":$PATH:" in *":$HOME/.local/bin:"*) echo "PATH OK: ~/.local/bin 已在 PATH";; *) echo "PATH MISSING";; esac

# 5. 是不是 SSH session（決定認證走哪條路）
echo "SSH_CONNECTION=[${SSH_CONNECTION:-未設定}]"

# 6. 現況
command -v agy || echo "agy: 尚未安裝"
ls -d ~/.gemini 2>/dev/null || echo "~/.gemini 不存在（全新安裝）"
```

**乾淨環境下的預期範例輸出**

```
PRETTY_NAME="Ubuntu 22.04.5 LTS"
x86_64
ldd (Ubuntu GLIBC 2.35-0ubuntu3.14) 2.35
GLIBCXX_3.4.30
DISPLAY=[未設定] WAYLAND_DISPLAY=[未設定] WSL=[否]
PATH OK: ~/.local/bin 已在 PATH
SSH_CONNECTION=[未設定]
agy: 尚未安裝
~/.gemini 不存在（全新安裝）
```

**逐項判讀**

| # | 檢查 | 應該看到 | 不符合怎麼辦 |
|---|---|---|---|
| 1 | 發行版 / 架構 | Ubuntu 20 以上、`x86_64` 或 `aarch64` | 舊於 Ubuntu 20（或等價的 Debian 10 / Fedora 36 / RHEL 8）就先看第 2、3 項的實際數字，版本號只是代理指標 |
| 2 | glibc | `≥ 2.28` | 低於 2.28 不能裝。升級發行版或更換主機。⚠️ 這是官方為 **IDE** 列的需求；**CLI 自己的系統需求官方未載明**，本文借用它當保守下限 |
| 2 | GLIBCXX | `≥ 3.4.25` | 同上。輸出空白代表 `libstdc++.so.6` 不在該路徑，用 `ldconfig -p \| grep libstdc++` 找出實際位置再測 |
| 3 | `DISPLAY` / `WAYLAND_DISPLAY` | 有值 = 有桌面 | **兩者皆「未設定」= 沒有 GUI**。跳過第 3 節，走路線 A |
| 4 | PATH | `PATH OK` | 顯示 `PATH MISSING` 時，`agy` 裝完會 `command not found`。見第 5 節第 1 項 |
| 5 | `SSH_CONNECTION` | 有值 = 在 SSH session 內 | 有值代表認證需走 **2.4 的手動 URL 流程**，不會自動開啟瀏覽器 |
| 6 | `command -v agy` | 有輸出 = 已安裝 | 顯示「尚未安裝」代表此環境可進行乾淨安裝（第 2 節） |

**沒有 Node.js 檢查。** `agy` 不需要 Node —— 那是舊 Gemini CLI 的需求，本文不涵蓋。

---

## 2. 安裝 `agy`

### 2.1 安裝命令（逐字照抄官方）

macOS / Linux：

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

其他平台（給有桌面的 Windows 環境參考，同樣逐字照抄官方）：

| 平台 | 命令 |
|---|---|
| Windows PowerShell | `irm https://antigravity.google/cli/install.ps1 \| iex` |
| Windows CMD | `curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd` |

**依官方文件**，macOS / Linux 的執行檔會放在 **`~/.local/bin/agy`**
（Windows 是 `C:\Users\<Username>\AppData\Local\agy\bin`）。

**依官方文件應看到**：安裝腳本印出下載與安裝進度後正常結束。
⚠️ 官方文件未載明安裝腳本的逐字輸出，本文不編造。
**說明**：`~/.local/bin/agy` 執行檔大小約為 200 MB 上下。

### 2.2 兩個可選旗標

| 旗標 | 官方說明（轉述） | 什麼時候用 |
|---|---|---|
| `--skip-aliases` | 跳過 shell profile 的 alias 清理 —— 不讓安裝腳本 purge 或更新既有的 `agy` / `antigravity` legacy alias | 你自己在 `.bashrc` / `.zshrc` 定義過同名 alias，不想被動到 |
| `--skip-path` | 跳過 shell profile 的 `PATH` 附加 —— 不修改你的 shell profile | 你自己管理 PATH |

帶旗標的寫法：

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash -s -- --skip-path
```

> ⚠️ 官方文件未載明 `bash -s --` 這種傳參寫法，上面是 shell 的標準用法。
> 若安裝器回報不認得旗標，改用不帶旗標的版本。

**什麼時候適合使用 `--skip-path`**：
若你的 `~/.local/bin` 在安裝前**就已經在 PATH 中**，但安裝器預設仍會在 Shell Profile（如 `~/.bashrc` 或 `~/.profile`）追加路徑設定：

```bash
# Added by Antigravity CLI installer
export PATH="$HOME/.local/bin:$PATH"
```

如果偏好保持 Shell Profile 簡潔、避免重複追加 PATH 條目，可在安裝時帶上 `--skip-path`。

### 2.3 驗證安裝

```bash
command -v agy
```

**你應看到**：`/home/<你的帳號>/.local/bin/agy` （或對應系統的 PATH 路徑）

> ⚠️ **官方文件未載明 `agy --version` / `agy --help` 是否存在**，也未載明手動更新命令。
> 所以本文只用 `command -v` 這種與工具無關的方式驗證，不虛構版本旗標。
> 你的版本若剛好支援 `agy --version`，那是額外收穫，不是本文的通過條件。

### 2.4 認證：Remote SSH / Headless 環境走手動 URL 流程

**依官方文件**，`agy` 會先嘗試靜默讀取 OS keyring；沒有有效 token 時：

| 環境 | 官方描述的行為 |
|---|---|
| 有桌面的本機 | 「automatically launches your local default web browser」做 OAuth |
| **Remote SSH / Headless** | 走官方稱為 **manual URL loop** 的流程，**不會**開瀏覽器 |

**manual URL loop 五步（依官方文件）**：

1. 在遠端 terminal 執行 `agy`
2. CLI 印出一組 unique, secure authorization URL
3. 把該 URL 複製到**你自己筆電的**瀏覽器並登入 Google 帳號
4. 瀏覽器顯示一組 **alphanumeric authorization code**
5. 回到 SSH terminal，在提示處貼上該 code

**依官方文件應看到**：終端機印出一個授權 URL 與一個等待貼上 code 的提示。
在 Headless 環境下**不會**自動彈出瀏覽器，需手動複製 URL 登入。

> 貼不進去（SSH 剪貼簿）→ 第 5 節第 6 項。
> 完全沒出現 URL、畫面就卡住 → 第 5 節第 2 項。

**依官方文件**，Linux 的憑證存放在 Secret Service / dbus keyring（GNOME Keyring 或 KWallet）。
**說明**：若在無 GUI / Headless 環境且未執行 keyring daemon，憑證通常會落在 `~/.gemini/antigravity-cli/antigravity-oauth-token`（權限 `600`）。

登出（保留安裝）：在 `agy` 互動介面輸入 `/logout`
—— 官方說明是「disconnect your account and purge saved authentication profiles from your
operating system's keyring」。

### 2.5 確認 CLI 活著

**依官方文件**，首次在專案目錄啟動 `agy` 會依序問三件事：

1. **Color Scheme**（Solarized / Dark / Solarized Light / Terminal defaults）
2. **Rendering Mode**（Alt-Screen 全螢幕，或 Inline 併入 terminal 歷史）
3. **Workspace Trust**（確認信任這個 repo 目錄，agent 隨後索引檔案）

答完之後，在 prompt 輸入：

```
/help
```

官方說明：「開說明面板（指令與快捷鍵）」。
**依官方文件應看到**：終端機內開啟一個列出 slash command 與快捷鍵的面板。
按 `Esc` 關閉，`/exit` 或 `Ctrl+D` 離開 session。

> 想看額度用量是 `/usage`（alias `/quota`），不是 `/help`。
> 官方 `/docs/cli/features` 頁把兩者寫反了；本文採 `/docs/cli/reference` 的說法
> （與 `/docs/cli/commands/usage` 一致）。

---

## 3. Antigravity IDE（在有桌面環境的機器上）

**無 GUI / Headless 環境請跳過本節。**（見 0.1）

下載頁：**<https://antigravity.google/download>**

系統需求（官方原文，`antigravity.google` getting-started）：

| 平台 | 需求 | 注意 |
|---|---|---|
| **macOS** | 最低 12（Monterey）；「macOS versions with Apple security update support. This is typically the current and two previous versions.」 | 🚨 **「X86 is not supported」—— 僅 Apple Silicon。Intel Mac 不能裝** |
| **Windows** | 「Windows 10 (64 bit)」 | — |
| **Linux** | 「glibc >= 2.28, glibcxx >= 3.4.25 (e.g. Ubuntu 20, Debian 10, Fedora 36, RHEL 8)」 | 需具備圖形桌面環境（X11 或 Wayland） |

安裝時若跳出「Keep Both」/「Replace」提示，官方指示選 **「Replace」**。
安裝後建立專案：點資料夾圖示 → **New Project** → 加入資料夾 → **Create**。

⚠️ 官方文件未載明 IDE 的解除安裝程序，見第 6 節。

---

## 4. 把本 repo 的 harness 接上

裝完之後，在 **repo 根目錄**確認跨工具 harness 有被讀到。

> 下列檔案屬於本 repo 的 Antigravity 軌。**你不需要自己建立它們** ——
> 若你的 clone 裡還沒有，代表該軌尚未合併進你的分支，那是預期內的，不是安裝失敗。

### 4.1 檔案存在性（純 shell，可立刻跑）

```bash
cd <你的 repo 根目錄>
ls -d AGENTS.md .agents/skills .agents/rules 2>&1
ls .agents/skills/*/SKILL.md 2>&1
```

**你應看到**：三個路徑都列得出來，且 `.agents/skills/` 底下每個資料夾各有一個 `SKILL.md`。

為什麼是這些路徑（依官方文件）：

| 路徑 | 角色 |
|---|---|
| `AGENTS.md`（workspace root） | 官方 best-practices 指定的 codebase rule file（`GEMINI.md` 亦可） |
| `.agents/skills/<name>/SKILL.md` | workspace 層級 Agent Skills |
| `.agents/agents/<name>/agent.md` | workspace 層級 subagent 定義 |
| `.agents/mcp_config.json` | workspace 層級 MCP 設定 |

> ⚠️ **官方 CLI 文件未確認 `.agents/rules/` 會被 CLI 讀取**
> —— CLI best-practices 只寫 workspace root 的 `AGENTS.md` / `GEMINI.md`。
> `.agents/rules/` 出現在 plugin 結構與 Antigravity 主文件裡。
> 所以本 repo 的長期紀律以 `AGENTS.md` 為主要落點，`.agents/rules/` 視為補充。

### 4.2 `agy` 有沒有讀到 skills

在 **repo 根目錄**啟動 `agy`，輸入：

```
/skills
```

官方說明：「瀏覽已載入的 local 與 global Agent Skills」。

**依官方文件應看到**：`.agents/skills/` 底下每個 skill 的 `name` 與 `description` 出現在清單裡。
沒出現時最常見的原因是 `SKILL.md` frontmatter 缺 `description` —— 那是必填欄位。

> `agy` **不讀 `.claude/skills/`**。本 repo 的 Claude Code skills 要能在 Antigravity 用，
> 必須落在 `.agents/skills/`。
> ⚠️ 移植差異的 `PORTING.md` 尚未納入本 repo（與 `.agents/` 軌一併待補）。

### 4.3 其他可選的活體檢查

| 想確認 | 在 `agy` 裡輸入 | 依官方文件應看到 |
|---|---|---|
| MCP server 連線狀態 | `/mcp` | MCP Manager 面板，含狀態燈與連線 log |
| 目前生效的 hooks | `/hooks` | 目前生效的 pre-flight / post-format script hooks 清單 |
| 目前的權限規則 | `/permissions` | allowlist / denylist / asklist 三個分頁 |
| subagent 有沒有被認出 | `/agents` | Agent Manager Panel，列出 Identifier / Role / State |

> ⚠️ 官方 CLI 文件**未載明 CLI hooks 的設定檔路徑與 schema**（`/hooks` 只能「瀏覽」）。
> 本 repo 的 Antigravity hook adapter 屬於實驗性接法，`/hooks` 列不出來時**不算安裝失敗**。

---

## 5. 卡住就看這裡

| # | 症狀 | 原因 | 處置 |
|---|---|---|---|
| 1 | `agy: command not found`（但檔案裝好了） | 執行檔在 `~/.local/bin/agy`，該路徑不在 shell PATH（或你用了 `--skip-path` 而 PATH 本來就沒有） | 先 `ls -l ~/.local/bin/agy` 確認檔案在。在的話，把 `export PATH="$HOME/.local/bin:$PATH"` 加進 `~/.bashrc`（或 `~/.zshrc`），再 `source ~/.bashrc`。若第 1 節前置檢查確認 PATH 已包含該路徑，正常不會遇到 |
| 2 | SSH 進來跑 `agy`，畫面卡住、**沒有出現授權 URL** | CLI 沒把環境判定為 remote SSH，正在等 OS keyring 或瀏覽器回應 —— Headless 環境下無 GUI 可自動彈出瀏覽器 | `Ctrl+C` 中止。用 `echo $SSH_CONNECTION` 確認你確實在 SSH session 裡。仍不出現時：⚠️ **官方文件未載明強制走 manual URL loop 的旗標** —— 改走路線 B，在有桌面的機器完成登入 |
| 3 | 認證時被擋，訊息提到 region / country / not available | Google 帳號所在地區尚未開放，或組織政策封鎖 | ⚠️ **官方文件未列出可用地區清單。** 用組織帳號者找 workspace 管理員確認。**不要用 VPN 繞過服務條款** |
| 4 | 安裝或啟動時報 `GLIBC_2.xx not found` / `GLIBCXX_3.4.xx not found` | 系統的 glibc 或 libstdc++ 舊於需求 | 跑第 1 節第 2 項看實際數字。低於 `glibc 2.28` / `GLIBCXX 3.4.25` **沒有安全的繞法**（不要手動塞 `.so` 進系統目錄）—— 升級發行版，或更換主機 |
| 5 | 認證報 `failed to retrieve token: secret keyring is locked` | Linux 的 Secret Service（GNOME Keyring / KWallet）沒解鎖；headless / SSH session 通常根本沒有 D-Bus | 官方給 Linux 的處置：確認 keyring 已解鎖；headless / SSH session 需啟動 D-Bus —— `export $(dbus-launch)` 後重跑 `agy`。Headless / SSH 環境最常遇到此情況 |
| 6 | 授權 code 貼不進 terminal，或報 `local pasteboard is empty or unreachable over SSH connection` | 標準 SSH 不轉發圖形剪貼簿 | 官方處置：改用支援進階 clip channel 的終端機（iTerm2 / Ghostty）；iTerm2 走 Preferences → General → Selection → 開啟「Applications in terminal may access clipboard」；用 tmux 的話在設定檔加 `set -s set-clipboard on`。**最省事的作法：手動打那串 code** |
| 7 | 在 Headless Linux 主機啟動 Antigravity **IDE**，出現 `cannot open display` 或無回應 | IDE 是 GUI 應用程式；Headless 主機沒有 `DISPLAY` 也沒有 Wayland | **不要嘗試修。** 這不是設定問題。走 0.1 的路線 B：IDE 裝在有桌面的機器，Headless 主機僅保留 `agy` CLI |
| 8 | 更新卡住，或報 `another background updater process is already active (update.lock)` | 內建 self-updater 的 advisory lock 沒釋放，或安裝路徑唯讀 | 官方處置：`rm -f ~/.gemini/antigravity-cli/updater/update.lock`；要整個關掉自動更新就在 shell profile 設 `AGY_CLI_DISABLE_AUTO_UPDATE=true`；並確認 `~/.local/bin/` 為你自己所有且可寫 |
| 9 | `/skills` 列不到 `.agents/skills/` 底下的 skill | 沒有在 **repo 根目錄**啟動 `agy`，或 `SKILL.md` frontmatter 缺必填的 `description` | `pwd` 確認位置；`head -5 .agents/skills/<name>/SKILL.md` 確認 frontmatter 有 `name` 與 `description`。另外確認 skill **不是**只放在 `.claude/skills/` —— `agy` 不讀那裡 |
| 10 | 非互動模式（`agy -p "..."`）報 authentication required | Headless 模式只用**快取憑證**，不會自己發起登入 | 官方原文：「Headless mode uses your cached credentials. Authenticate once with an interactive `agy` session first.」先跑一次互動式 `agy` 完成 2.4 的認證 |

---

## 6. 解除安裝

### 6.1 `agy` CLI

⚠️ **官方文件未載明解除安裝程序** —— 沒有 uninstall 腳本、沒有 uninstall 命令、沒有 uninstall 章節。
以下是依官方載明的安裝路徑與 Shell Profile 修改紀錄整理的最小移除方式：

**步驟 1：先登出**（在移除執行檔前做，否則就沒有工具可以清憑證了）

在 `agy` 互動介面輸入 `/logout`
—— 官方：「purge saved authentication profiles from your operating system's keyring」。

**步驟 2：移除執行檔**

```bash
rm -f ~/.local/bin/agy
```

**步驟 3：清掉安裝器加進 shell profile 的片段**

**說明**：安裝器若在 Shell Profile（如 `~/.bashrc` 或 `~/.profile`）中加了設定，標記固定是同一行註解。
先看，再決定要不要刪：

```bash
grep -n -A1 "Added by Antigravity CLI installer" ~/.bashrc ~/.profile ~/.zshrc 2>/dev/null
```

**你應看到**：`# Added by Antigravity CLI installer` 加上它下一行的 `export PATH=...`。
確認過內容之後手動編輯檔案刪掉那兩行。

> 🚨 **不要用 `sed -i` 一鍵刪。** Shell Profile 是你登入 shell 的命脈，
> 改壞了下次開啟 session 會一起壞。用編輯器開啟、看清楚、只刪那兩行。
> 另外：若 `~/.local/bin` 原本就已在你的 `PATH` 中，請勿誤刪原本的 `PATH` 設定。

### 6.2 設定與資料目錄 `~/.gemini/`

**先讀完再決定。** 這個目錄名稱是歷史包袱，實際上是 **Antigravity 全家桶共用的家目錄命名空間**：

| 路徑 | 屬於 | 刪掉會失去 |
|---|---|---|
| `~/.gemini/antigravity-cli/settings.json` | CLI | 主題、editor mode、權限 preset 等全部 CLI 設定 |
| `~/.gemini/antigravity-cli/keybindings.json` | CLI | 自訂快捷鍵（**刪除即還原官方預設**，這是官方載明的重設方式） |
| `~/.gemini/antigravity-cli/skills/` | CLI | global Agent Skills |
| `~/.gemini/antigravity-cli/plugins/` | CLI | 所有已安裝 plugin |
| `~/.gemini/antigravity-cli/cache/`、`conversations/` | CLI | 對話歷史與 session 快取 |
| `~/.gemini/config/agents/<name>/agent.md` | **跨產品 global** | global subagent 定義 |
| `~/.gemini/config/mcp_config.json` | **跨產品 global** | global MCP server 設定 |
| `~/.gemini/GEMINI.md` | **跨產品 global** | global rules |

> 🚨 **`rm -rf ~/.gemini` 會一次刪光上表全部** ——
> 包含你可能還要在 IDE 那台繼續用的 global subagent、MCP 與 rules。
> 只是想重設 CLI 的話，刪 `~/.gemini/antigravity-cli/` 就好；
> 只是想重設快捷鍵的話，刪 `keybindings.json` 這一個檔案就好。

只想「重來一次首次啟動」而不是真的解除安裝：刪 `~/.gemini/antigravity-cli/settings.json`。
⚠️ 官方文件未載明「刪掉 settings.json 之後首次啟動精靈會不會重跑」，這只是最小破壞的嘗試順序。

### 6.3 Antigravity IDE

⚠️ 官方文件未載明解除安裝程序。依各平台慣例移除應用程式即可
（macOS 丟進「應用程式」的垃圾桶、Windows 走「應用程式與功能」、Linux 依你當初的安裝方式）。
**設定殘留一樣落在 `~/.gemini/`**，處置與風險同 6.2。

---

## 下一步

裝完 `agy` 之後：

1. **學指令與 `.agents` 設定** → [`CLI_GUIDE.md`](./CLI_GUIDE.md)
   （含元件責任對照表、`SKILL.md` 撰寫方式、常用 slash commands）
2. **回到本 repo 的分析主線** → 根目錄 [`README.md`](../../README.md)
   ，或直接進 [`上課用prompt/分析師武器庫.md`](../../上課用prompt/分析師武器庫.md) 走六階段流程
3. **讓 agent 認識資料集** → 根目錄 [`AGENTS.md`](../../AGENTS.md)
   已寫好資料集契約與分析鐵律，`agy` 會自動讀取，不需要你額外設定

> ⚠️ 完整 Antigravity 文件集裡另有 `COMPONENTS.md`（元件選用時機）與
> `PORTING.md`（`.claude/` → `.agents/` 的移植陷阱），**尚未納入本 repo**，
> 與 `.agents/` 軌一併待補。元件責任的部分，`CLI_GUIDE.md` 第 2.1 節已有對照表可先用。
