# 安裝 SOP：opencode

> 本文是學生在乾淨環境下**照著做就能裝完**的操作手冊與環境檢查指南。
>
> - 標「**依官方文件**」的：取自 `opencode.ai/docs` 官方文件。
> - 標「**範例輸出**」的：乾淨 Linux / macOS 環境下的標準預期結果。
> - 標「⚠️ 官方文件未載明」的：官方未明確紀錄，操作時需多加注意。
>
> 🚨 **本文沒有「本機實測」標註。**
> 另外三份手冊裡有些數字來自教材開發機的實際執行，
> 但 opencode **未安裝在該機器上**，所以本文全部內容都來自官方文件。
> 你實際跑出來的畫面若與本文不同，以你的畫面與官方文件為準。
>
> 唯一可信來源：`opencode.ai/docs`。第三方部落格一律不採用。
> 四款 agent 的比較與選擇建議見 [`../README.md`](../README.md)。

---

## 0. 先讀這段

### 0.1 opencode 跟另外三款不一樣的地方

**它不綁定單一模型供應商。** Antigravity 綁 Google、Claude Code 綁 Anthropic、Codex 綁 OpenAI，
而 opencode 讓你自己接 provider。

這帶來一個代價與一個好處：

- **代價**：你得自己準備 API key 或帳號，安裝完不是馬上就能用。
- **好處**：同一個介面裡切換模型。要做
  [`04報告呈現/報告數字驗算.md`](../../上課用prompt/04報告呈現/報告數字驗算.md)
  說的「換一家模型來當稽核員」時，這是最省事的做法。

### 0.2 終端機有要求

**依官方文件**：需要一個「modern terminal emulator」，官方點名的例子是
**WezTerm、Alacritty、Ghostty、Kitty**。

> ⚠️ **官方未列出「不支援」的終端機清單**，本文不編造。
> 但這是四款裡唯一對終端機提出要求的 —— 如果你在很舊的終端機上出現畫面破圖或按鍵失效，
> 先換一個終端機再排查其他問題。

**Windows 使用者**：依官方文件建議走 **WSL** 以獲得最佳效能。

### 0.3 你需要什麼帳號

依官方文件，兩條路：

| 路線 | 做法 |
| :--- | :--- |
| **opencode 帳號** | 在介面裡跑 `/connect` → 選 opencode → 到 `opencode.ai/auth` 登入、填帳務資料、取得 API key，貼回終端機 |
| **自帶 provider** | `/connect` 時選其他 provider，用你自己的 API key |

> ⚠️ **官方未載明免費額度的細節**，本文不編造。開始之前先確認你有可用的 key 或額度。

---

## 1. 前置檢查

**整段貼進終端機執行：**

```bash
# 1. 作業系統與架構
grep PRETTY_NAME /etc/os-release 2>/dev/null || sw_vers 2>/dev/null
uname -m

# 2. 你在什麼終端機裡（官方要求 modern terminal emulator）
echo "TERM=[${TERM:-未設定}] TERM_PROGRAM=[${TERM_PROGRAM:-未設定}]"

# 3. 是不是 WSL（Windows 使用者官方建議走 WSL）
echo "WSL=[${WSL_DISTRO_NAME:-否}]"

# 4. ~/.local/bin 在不在 PATH
case ":$PATH:" in *":$HOME/.local/bin:"*) echo "PATH OK: ~/.local/bin 已在 PATH";; *) echo "PATH MISSING";; esac

# 5. 現況
command -v opencode || echo "opencode: 尚未安裝"
ls -d ~/.config/opencode 2>/dev/null || echo "~/.config/opencode 不存在（全新安裝）"
```

**乾淨環境下的預期範例輸出**

```
PRETTY_NAME="Ubuntu 22.04.5 LTS"
x86_64
TERM=[xterm-256color] TERM_PROGRAM=[未設定]
WSL=[否]
PATH OK: ~/.local/bin 已在 PATH
opencode: 尚未安裝
~/.config/opencode 不存在（全新安裝）
```

**逐項判讀**

| # | 檢查 | 應該看到 | 不符合怎麼辦 |
|---|---|---|---|
| 1 | 發行版 / 架構 | ⚠️ **官方未載明最低 OS 版本、架構清單與記憶體需求**，本文不編造 | 裝完跑不起來時，先確認第 2 項的終端機 |
| 2 | 終端機 | 官方點名 WezTerm / Alacritty / Ghostty / Kitty | 出現畫面破圖或按鍵失效時，**先換終端機**再排查別的 |
| 3 | WSL | Windows 使用者建議有值 | 原生 Windows 也能裝（choco / scoop），但官方建議 WSL |
| 4 | PATH | `PATH OK` | ⚠️ 官方未載明 install script 的安裝路徑；顯示 `PATH MISSING` 且裝完找不到指令時，見第 5 節第 1 項 |
| 5 | `command -v opencode` | 有輸出 = 已安裝 | 顯示「尚未安裝」代表可進行乾淨安裝 |

---

## 2. 安裝 opencode

### 2.1 安裝命令（逐字照抄官方）

**通用安裝腳本（官方建議的最快路徑）：**

```bash
curl -fsSL https://opencode.ai/install | bash
```

其他管道（同樣逐字照抄官方）：

| 管道 | 命令 |
|---|---|
| npm | `npm install -g opencode-ai` |
| Bun | `bun install -g opencode-ai` |
| pnpm | `pnpm install -g opencode-ai` |
| Yarn | `yarn global add opencode-ai` |
| Homebrew | `brew install anomalyco/tap/opencode` |
| Arch Linux | `sudo pacman -S opencode`（或 `paru -S opencode-bin`） |
| Chocolatey（Windows） | `choco install opencode` |
| Scoop（Windows） | `scoop install opencode` |
| Mise | `mise use -g github:anomalyco/opencode` |
| Docker | `docker run -it --rm ghcr.io/anomalyco/opencode` |

> 🚨 **不要用 `sudo npm install -g`。** 全域安裝加 sudo 會造成權限與安全問題。
> 遇到權限錯誤時改用 install script，不要加 sudo 硬上。

### 2.2 驗證安裝

```bash
command -v opencode
opencode --version
```

**應看到**：執行檔路徑與一組版本號。

> ⚠️ **官方文件未載明 install script 的安裝路徑與版本號格式**，本文不編造。
> 用 `command -v opencode` 確認實際位置。

### 2.3 登入與選 provider

啟動：

```bash
opencode
```

在介面裡輸入：

```
/connect
```

依官方文件，這會列出可選的 provider。選 **opencode** 的話，接著到 `opencode.ai/auth`
登入、填帳務資料、複製 API key，再貼回終端機的提示處。
也可以選其他 provider，用你自己的 key。

也可以走 CLI 子命令：

| 動作 | 命令 |
| :--- | :--- |
| 設定 API key | `opencode auth login` |
| 列出已認證的 provider | `opencode auth list`（別名 `ls`） |
| 清除某 provider 的憑證 | `opencode auth logout` |

### 2.4 確認可用模型

```bash
opencode models
```

依官方文件，這會「List all available models from configured providers」。
**列得出東西，代表 provider 接好了。**

### 2.5 確認它活著

在專案目錄執行 `opencode`，然後：

- 輸入 `/help` 開說明對話框
- 按 `Ctrl+P` 開命令面板
- 輸入 `/exit`（別名 `/quit`、`/q`）離開

---

## 3. 兩個要先知道的操作習慣

opencode 的 TUI 操作邏輯跟另外三款不太一樣，先知道這兩個會省很多困惑。

### 3.1 Leader key 是 `Ctrl+X`

依官方文件，`Ctrl+X` 是預設的 leader key，快捷鍵都是「先按 `Ctrl+X`，再按第二個鍵」：

| 快捷鍵 | 作用 |
| :--- | :--- |
| `Ctrl+X` `n` | 開新 session |
| `Ctrl+X` `l` | 列出／切換 session |
| `Ctrl+X` `c` | 壓縮 session |
| `Ctrl+X` `m` | 列出模型 |
| `Ctrl+X` `u` / `r` | 復原 / 重做 |
| `Ctrl+X` `e` | 開外部編輯器 |
| `Ctrl+X` `x` | 匯出對話 |
| `Ctrl+X` `q` | 離開 |
| `Ctrl+P` | 命令面板（不用 leader key） |

### 3.2 `Tab` 切換 agent

依官方文件，opencode 內建兩個 primary agent：

| Agent | 行為 |
| :--- | :--- |
| **Build** | **預設**，所有工具都開啟 |
| **Plan** | 受限模式，編輯與 bash 指令預設為 `ask`（要你核准） |

按 **`Tab`** 在 session 中循環切換。另有三個 subagent（`general`、`explore`、`scout`），
用 `@` 提及來呼叫，或由 primary agent 自動委派。

> 💡 **分析課的建議**：階段 00~03（定義問題、選策略、挑圖表）用 **Plan** 就夠了，
> 它不會亂改你的檔案。到階段 02+ 要真的跑數字、寫腳本時再 `Tab` 切到 **Build**。

---

## 4. 把本 repo 的 harness 接上

### 4.1 opencode 原生讀 `AGENTS.md`

**這是好消息：本 repo 不需要任何額外設定。**

依官方 rules 文件，opencode 找指令檔的順序是：

```text
1.【專案】從當前目錄往上找，第一個命中的 AGENTS.md（找不到才退而找 CLAUDE.md）
2.【全域】~/.config/opencode/AGENTS.md
3.【相容】~/.claude/CLAUDE.md（除非你關掉）
```

> 每一類裡「第一個命中的檔案」勝出。官方舉的例子：
> 本地同時有 `AGENTS.md` 與 `CLAUDE.md` 時，**只載入 `AGENTS.md`**。
> 對本 repo 來說這正好 —— 我們的 `CLAUDE.md` 只是給 Claude Code 用的轉接層。

### 4.2 確認契約真的載入了

在 **repo 根目錄**啟動 `opencode`，跑
[`../README.md`](../README.md#3-裝完之後先做這個驗收) 第 3 節的驗收提問。

> 🚨 **不要在本 repo 跑 `/init`。** 那個指令會分析專案並產生一份新的 `AGENTS.md`，
> 本 repo 已經有一份寫好的了，跑了可能會覆蓋掉。

### 4.3 設定檔位置

依官方文件：

| 層級 | 路徑 |
| :--- | :--- |
| **專案** | `opencode.json` 或 `opencode.jsonc`（專案根目錄） |
| **全域** | `~/.config/opencode/opencode.json` |
| TUI 專用 | `tui.json`（專案）／`~/.config/opencode/tui.json` |
| 自訂路徑 | 環境變數 `OPENCODE_CONFIG`、`OPENCODE_CONFIG_DIR` |

設定檔要加 `$schema` 才有編輯器自動補完：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-5"
}
```

### 4.4 想額外載入本 repo 的其他文件

依官方文件，`instructions` 選項可以把別的檔案一起併進來：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["上課用prompt/分析師武器庫.md"]
}
```

官方說明這些檔案「are combined with your `AGENTS.md` files」。

> ⚠️ 遠端 URL 也支援，但有 **5 秒逾時**限制。課堂上用本機路徑就好。

---

## 5. 卡住就看這裡

| # | 症狀 | 原因 | 處置 |
|---|---|---|---|
| 1 | `opencode: command not found`（但裝好了） | 安裝路徑不在 shell PATH | ⚠️ 官方未載明 install script 的安裝路徑。先用 `ls ~/.local/bin \| grep opencode` 與 `npm root -g` 找找看；找到後把該目錄加進 PATH。或改用 Homebrew / pacman 等有標準路徑的管道 |
| 2 | 畫面破圖、按鍵沒反應、顏色怪異 | 終端機太舊或不相容 | **先換終端機。** 官方點名 WezTerm / Alacritty / Ghostty / Kitty。這是 opencode 特有的坑，另外三款沒有 |
| 3 | 裝好了但問什麼都沒反應 | provider 沒接上 | 跑 `opencode models`。列不出東西就代表沒接好，回到 2.3 跑 `/connect` 或 `opencode auth login` |
| 4 | agent 一直要你核准編輯與 bash | 目前在 **Plan** agent | 按 `Tab` 切到 **Build**。見 3.2 |
| 5 | agent 不知道資料集欄位，開始猜 `Price` / `Customer ID` | 沒在 repo 根目錄啟動 | `pwd` 確認位置。opencode 從當前目錄往上找 `AGENTS.md`，在 repo 之外啟動就讀不到。跑 4.2 的驗收確認 |
| 6 | 不小心跑了 `/init`，`AGENTS.md` 被改了 | `/init` 會產生或更新 `AGENTS.md` | `git diff AGENTS.md` 看它改了什麼，`git checkout AGENTS.md` 還原。**這也是為什麼契約要進版控** |
| 7 | 想用 Claude Code 的既有設定 | — | 依官方文件，opencode 會 fallback 到 `~/.claude/CLAUDE.md`。你的個人偏好如果寫在那裡，opencode 讀得到 |
| 8 | 想知道花了多少錢 | — | `opencode stats`（依官方文件：「Show token usage and cost statistics」） |
| 9 | 版本太舊 | — | `opencode upgrade` |
| 10 | 想把對話交出去當佐證 | — | `/export` 匯出成 Markdown 並用預設編輯器開啟；或 `opencode export` 匯出成 JSON |

---

## 6. 更新與解除安裝

### 6.1 更新

```bash
opencode upgrade
```

依官方文件：「Updates opencode to the latest version」。

### 6.2 解除安裝

**opencode 是四款裡唯一有官方 uninstall 子命令的：**

```bash
opencode uninstall
```

依官方文件：「Uninstall OpenCode and remove all related files」。

> ⚠️ **官方未逐字載明它究竟刪了哪些檔案。**
> 想確認設定有沒有清乾淨，跑完之後自己看一眼：
>
> ```bash
> ls -d ~/.config/opencode 2>/dev/null || echo "設定已清除"
> command -v opencode || echo "執行檔已移除"
> ```
>
> 用套件管理器裝的（brew / pacman / choco / scoop / npm），
> 建議改用該管理器自己的移除命令，避免兩套機制打架。

---

## 下一步

裝完 opencode 之後：

1. **學指令與 `opencode.json` 設定** → [`CLI_GUIDE.md`](./CLI_GUIDE.md)
2. **跑一次驗收，確認契約載入** → [`../README.md`](../README.md#3-裝完之後先做這個驗收)
3. **回到分析主線** → [`上課用prompt/index.html`](../../上課用prompt/index.html)
   或 [`上課用prompt/分析師武器庫.md`](../../上課用prompt/分析師武器庫.md)
