# CLAUDE.md

本專案的作業規範寫在 **[AGENTS.md](AGENTS.md)**（Antigravity / Claude Code / Codex 共用同一份）。

@AGENTS.md

---

## Claude Code 專屬補充

以下只寫 `AGENTS.md` 沒有、且與 Claude Code 環境相關的部分。
**其餘一律以 `AGENTS.md` 為準，不要在本檔重複它的內容。**

### 對全局規範的專案級調整

全局 `~/.claude/CLAUDE.md` 要求 TDD 與 80% 測試覆蓋率。**本專案不適用該門檻**，原因：

- `pandas數據分析工具教學/` 與 `上課用prompt/` 是教學素材，正確性由講義與參考解答保證
- `scripts/` 底下的分析腳本，驗證方式是**能重跑並得到相同數字**，不是單元測試覆蓋率

取而代之的驗收標準：分析腳本必須可從乾淨環境重跑，且報告中的每個數字都能追溯到腳本的某一段
（見 `AGENTS.md` 第 4 節）。若日後新增可重用的工具函式庫，該部分仍套用全局的 TDD 規範。

### 分支

全局鐵律照舊：`main` 不直接改，先開分支。
本專案的分析／教材改動用 `docs/` 或 `feat/` 前綴，例如 `feat/data-analysis-ai-workflow`。

### 常用起手式

```
讀 AGENTS.md 第 3 節的資料集契約，然後 <你的分析需求>
```

跑完整分析流程時，直接指名階段：

```
用 上課用prompt/02數據分析/分析執行_AI_Coding.md 的模式 B，
針對 資料集/Online Retail/online_retail_09_10.csv 做 RFM 分群
```
