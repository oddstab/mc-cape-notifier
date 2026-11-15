# Minecraft Cape Notifier (Telegram)

每 30 分鐘透過 GitHub Actions 檢查 Minecraft Wiki 披風導覽模板（`Template:Navbox_capes`），當有新披風加入或模板更新時，自動透過 Telegram Bot 發送通知。

## GitHub Secrets 設定

| Secret 名稱 | 說明 |
| :--- | :--- |
| `TG_BOT_TOKEN` | Telegram BotFather 核發的 Bot Token（必填） |
| `TG_CHAT_ID` | 接收通知的 Chat ID（選填；若未填寫，會自動從你傳給 Bot 的最新訊息取得） |

## 手動測試與本機檢查

- 在 GitHub Actions 頁面點選 **Minecraft Cape Notifier** → **Run workflow**（`send_test` 選 `true`）即可立刻發送測試訊息。
- 本機自我檢查：`python main.py --check`
