# Minecraft Cape Notifier (Telegram)

[![Minecraft Cape Notifier](https://github.com/oddstab/mc-cape-notifier/actions/workflows/notify.yml/badge.svg)](https://github.com/oddstab/mc-cape-notifier/actions/workflows/notify.yml)

[English](README.md) · **繁體中文** · [简体中文](README.zh-CN.md)

Minecraft 出新披風（Cape）時，透過 Telegram Bot 通知你。用 GitHub Actions 定時執行，不需要自己的伺服器。

## 運作方式

1. GitHub Actions 每 30 分鐘執行一次 `main.py`（排程以 UTC 計算，GitHub 常會延遲幾分鐘到十幾分鐘）。
2. `main.py` 讀取 Minecraft Wiki 的披風導覽模板 [`Template:Navbox_capes`](https://minecraft.wiki/w/Template:Navbox_capes)，整理出披風清單。
3. 和上次存在 `state.json` 的清單比對；有變動就發雙語 Telegram 通知並列出新增的披風，再把新清單 commit 回儲存庫。沒變動就什麼都不做。

只用 Python 標準庫，不需要安裝任何套件。

## GitHub Secrets

在 [Settings → Secrets and variables → Actions](https://github.com/oddstab/mc-cape-notifier/settings/secrets/actions) 設定。Secret 的值存進去後就看不到了，只能覆寫。

| Secret 名稱 | 說明 |
| :--- | :--- |
| `TG_BOT_TOKEN` | `@BotFather` 核發的 Bot Token（必填） |
| `TG_CHAT_ID` | 接收通知的 Chat ID（選填；未設定時會從 Bot 最近收到的訊息自動取得） |

用 `gh` 更新：

```bash
gh secret set TG_BOT_TOKEN   # 互動輸入，值不會留在終端機紀錄
gh secret set TG_CHAT_ID
gh secret list               # 只列名稱與更新時間
```

## 手動測試

- 網頁：[Actions](https://github.com/oddstab/mc-cape-notifier/actions/workflows/notify.yml) → **Run workflow**，`send_test` 選 `true`，會立刻發一則測試通知。
- 指令：`gh workflow run notify.yml -f send_test=true`
- 本機自我檢查（不發通知）：`python main.py --check`

## 限制

- 資料來源是社群維護的 Minecraft Wiki，通知時間取決於 Wiki 編輯者多快更新，可能比官方公告晚。
- 公開儲存庫連續 60 天沒有 commit，GitHub 會自動停用排程，並寄信通知。到 Actions 頁面按 **Enable workflow** 即可恢復。

## 授權

[MIT](LICENSE)
