# 選一個 coding agent

本 repo 的分析工作流**不綁定任何一款 coding agent**。
你可以用 Antigravity、Claude Code、Codex 或 opencode 走完全部六個階段，產出應該長得一樣。

> 這份文件回答三個問題：**我該選哪一款？** **怎麼裝？** **怎麼確認它真的讀到專案契約？**

---

## 1. 為什麼可以不綁

因為紀律寫在 **`AGENTS.md`**（專案根目錄），不是寫在某一款工具的設定檔裡。

`AGENTS.md` 是跨工具的社群慣例，本 repo 的資料集契約（欄位語意、編碼地雷、清洗標準）
與分析鐵律（數字不得杜撰、結論要可重跑）全部寫在那裡。四款工具讀取它的方式如下：

| 工具 | 讀 `AGENTS.md` 嗎 | 依據 |
| :--- | :--- | :--- |
| **Antigravity (`agy`)** | ✅ 原生 | 官方 best-practices 指定 workspace root 的 `AGENTS.md`（或 `GEMINI.md`）為 codebase rule file |
| **Codex (`codex`)** | ✅ 原生 | 官方 `agents-md` 指南：從 project root 往下走到 cwd，逐層讀 `AGENTS.md` |
| **opencode** | ✅ 原生 | 官方 rules 文件：由當前目錄往上找 `AGENTS.md`（找不到才退而找 `CLAUDE.md`） |
| **Claude Code (`claude`)** | ⚠️ 間接 | **官方明講「Claude Code reads `CLAUDE.md`, not `AGENTS.md`」**，官方建議的接法是寫一個 `CLAUDE.md` 去 import `AGENTS.md` |

**本 repo 已經接好了。** 根目錄的 `CLAUDE.md` 第一行就是 `@AGENTS.md`，
正是官方文件示範的那個寫法。所以四款工具在本 repo 都讀得到同一份契約，你不用自己設定。

---

## 2. 該選哪一款

四款都能走完流程。差別在**帳號**、**模型綁定**與**你已經有什麼**：

| | Antigravity `agy` | Claude Code `claude` | Codex `codex` | opencode |
| :--- | :--- | :--- | :--- | :--- |
| **背後模型** | Google | Anthropic | OpenAI | **多家可選**（自帶 API key） |
| **需要的帳號** | Google 帳號 | Claude Pro / Max / Team / Enterprise / Console<br>（免費版**不含** Claude Code） | ChatGPT 帳號，或 OpenAI API key | 各家 provider 的 API key，或 opencode 帳號 |
| **安裝** | 一行 curl | 一行 curl／brew／winget／npm／apt/dnf/apk | 一行 curl／npm／brew | 一行 curl／npm／brew／pacman／choco |
| **專案契約** | `AGENTS.md` | `CLAUDE.md`（本 repo 已轉接） | `AGENTS.md` | `AGENTS.md` |
| **安裝手冊** | [antigravity/](antigravity/INSTALL.md) | [claude-code/](claude-code/INSTALL.md) | [codex/](codex/INSTALL.md) | [opencode/](opencode/INSTALL.md) |

**選擇建議**

- **已經有 ChatGPT Plus/Pro 訂閱** → Codex（登入即用，不用另外辦帳號）
- **已經有 Claude Pro/Max 訂閱** → Claude Code
- **想用 Google 生態，或想順便玩 IDE** → Antigravity
- **手上有各家 API key，或想在同一個介面切換模型** → opencode
- **完全沒有付費訂閱** → 先看 opencode（自帶 key 最有彈性）；
  ⚠️ 四款都需要付費帳號或 API 額度，本教材無法提供

> 💡 **可以裝不只一款。** 四款的設定各自獨立（`~/.gemini/`、`~/.claude/`、`~/.codex/`、`~/.config/opencode/`），
> 互不干擾。課堂上想比較同一個 Prompt 在不同模型的產出時，這是最直接的做法 ——
> 也正好呼應 [`04報告呈現/報告數字驗算.md`](../上課用prompt/04報告呈現/報告數字驗算.md) 說的
> 「換一家模型來當稽核員，用別家的偏誤抵銷自家的偏誤」。

---

## 3. 裝完之後，先做這個驗收

不管你裝了哪一款，**在 repo 根目錄**啟動它，然後問這一句：

```
這個專案的 Online Retail 資料集，CustomerID 的缺失率是多少？
不要算，直接從專案契約回答。
```

**正確答案**（`AGENTS.md` 第 3.1 節寫死的）：

```
online_retail_09_10.csv → 20.5%
online_retail_10_11.csv → 24.9%
```

| 它的回答 | 代表什麼 | 怎麼辦 |
| :--- | :--- | :--- |
| 兩個數字都對 | ✅ 契約有被讀到，可以開始上課 | — |
| 說「我需要先讀檔才能回答」 | ⚠️ 契約沒載入，但它至少誠實 | 看各工具手冊的「把本 repo 的 harness 接上」那一節 |
| 給了一個看起來很合理的數字（例如「約 25%」「大約四分之一」） | 🚨 **契約沒載入，而且它在編** | 同上。順帶一提：這正是本課程要教你抓的東西 |

> 這個測試之所以有效，是因為那兩個數字**不可能猜對** ——
> 它們是實際跑過這兩個檔案才知道的。答得出來就代表它真的讀到了 `AGENTS.md`。

---

## 4. 各工具文件

| 工具 | 安裝與環境驗證 | 指令與設定 |
| :--- | :--- | :--- |
| Antigravity（`agy`） | [`antigravity/INSTALL.md`](antigravity/INSTALL.md) | [`antigravity/CLI_GUIDE.md`](antigravity/CLI_GUIDE.md) |
| Claude Code（`claude`） | [`claude-code/INSTALL.md`](claude-code/INSTALL.md) | [`claude-code/CLI_GUIDE.md`](claude-code/CLI_GUIDE.md) |
| Codex（`codex`） | [`codex/INSTALL.md`](codex/INSTALL.md) | [`codex/CLI_GUIDE.md`](codex/CLI_GUIDE.md) |
| opencode | [`opencode/INSTALL.md`](opencode/INSTALL.md) | [`opencode/CLI_GUIDE.md`](opencode/CLI_GUIDE.md) |

其他文件：

| 文件 | 內容 |
| :--- | :--- |
| [`course/M0-M9_懶人包.md`](course/M0-M9_懶人包.md) | 延伸閱讀：LLM 工程通則（評估驅動開發、別讓球員兼裁判等） |

---

## 5. 下一步

裝完並通過第 3 節的驗收之後，回到分析主線：

1. [`上課用prompt/index.html`](../上課用prompt/index.html) —— 六階段工作流的教學導覽頁（含流程圖）
2. [`上課用prompt/分析師武器庫.md`](../上課用prompt/分析師武器庫.md) —— Prompt 模板總索引
3. [`AGENTS.md`](../AGENTS.md) —— 資料集契約與分析鐵律（agent 會自動讀，你也該讀一次第 3 節）

---

## 附錄：這些文件的可信度標註

四份 `INSTALL.md` 沿用同一套標註，讀的時候請注意：

| 標註 | 意思 |
| :--- | :--- |
| **依官方文件** | 取自該工具的官方站台，非第三方部落格 |
| **本機實測** | 在本教材的開發機（Ubuntu 22.04 / x86_64）實際執行過的輸出 |
| **範例輸出** | 乾淨環境下的標準預期結果，你的畫面可能略有出入 |
| ⚠️ **官方文件未載明** | 官方沒寫，本文不編造 —— 遇到這種標註請自己多確認一次 |

> 版本會變。本文標註的版本號是撰寫當下（2026-08）在開發機上實測到的，
> 你裝到的版本更新是正常的。**若官方文件與本文衝突，以官方為準。**
