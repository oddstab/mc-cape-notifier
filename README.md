# Minecraft Cape Notifier (Telegram)

[![Minecraft Cape Notifier](https://github.com/oddstab/mc-cape-notifier/actions/workflows/notify.yml/badge.svg)](https://github.com/oddstab/mc-cape-notifier/actions/workflows/notify.yml)

Minecraft 出新披風（Cape）時，透過 Telegram Bot 通知你。用 GitHub Actions 定時執行，不需要自己的伺服器。

**語言 / Languages / 语言：** [繁體中文](#繁體中文) · [English](#english) · [简体中文](#简体中文)

---

## 繁體中文

### 運作方式

1. GitHub Actions 每 30 分鐘執行一次 `main.py`（排程以 UTC 計算，GitHub 常會延遲幾分鐘到十幾分鐘）。
2. `main.py` 讀取 Minecraft Wiki 的披風導覽模板 [`Template:Navbox_capes`](https://minecraft.wiki/w/Template:Navbox_capes)，整理出披風清單。
3. 和上次存在 `state.json` 的清單比對；有變動就發 Telegram 通知並列出新增的披風，再把新清單 commit 回儲存庫。沒變動就什麼都不做。

只用 Python 標準庫，不需要安裝任何套件。

### GitHub Secrets

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

### 手動測試

- 網頁：[Actions](https://github.com/oddstab/mc-cape-notifier/actions/workflows/notify.yml) → **Run workflow**，`send_test` 選 `true`，會立刻發一則測試通知。
- 指令：`gh workflow run notify.yml -f send_test=true`
- 本機自我檢查（不發通知）：`python main.py --check`

### 限制

- 資料來源是社群維護的 Minecraft Wiki，通知時間取決於 Wiki 編輯者多快更新，可能比官方公告晚。
- 公開儲存庫連續 60 天沒有 commit，GitHub 會自動停用排程，並寄信通知。到 Actions 頁面按 **Enable workflow** 即可恢復。

---

## English

Get a Telegram message when Minecraft releases a new cape. Runs on GitHub Actions, so no server of your own is needed.

### How it works

1. GitHub Actions runs `main.py` every 30 minutes (schedule is UTC; GitHub often delays runs by several minutes).
2. `main.py` reads the cape navigation template [`Template:Navbox_capes`](https://minecraft.wiki/w/Template:Navbox_capes) from the Minecraft Wiki and builds the current cape list.
3. It compares that list with the one saved in `state.json`. If something changed, it sends a Telegram message listing the newly added capes and commits the new list back to the repository. If nothing changed, it does nothing.

Standard library only — no dependencies to install.

### GitHub Secrets

Set them under [Settings → Secrets and variables → Actions](https://github.com/oddstab/mc-cape-notifier/settings/secrets/actions). Secret values cannot be read back once saved; you can only overwrite them.

| Secret | Description |
| :--- | :--- |
| `TG_BOT_TOKEN` | Bot token issued by `@BotFather` (required) |
| `TG_CHAT_ID` | Chat ID that receives notifications (optional; when empty, it is taken from the most recent message the bot received) |

Update with `gh`:

```bash
gh secret set TG_BOT_TOKEN   # interactive prompt, value stays out of shell history
gh secret set TG_CHAT_ID
gh secret list               # shows names and update times only
```

### Manual test

- Web: [Actions](https://github.com/oddstab/mc-cape-notifier/actions/workflows/notify.yml) → **Run workflow**, set `send_test` to `true` to receive a test message immediately.
- CLI: `gh workflow run notify.yml -f send_test=true`
- Local self-check (sends nothing): `python main.py --check`

### Limitations

- The data comes from the community-maintained Minecraft Wiki, so notifications arrive as fast as wiki editors update the page and may lag behind official announcements.
- GitHub disables scheduled workflows on public repositories after 60 days without commits and emails you about it. Open the Actions tab and press **Enable workflow** to resume.

---

## 简体中文

Minecraft 出新披风（Cape）时，通过 Telegram Bot 通知你。由 GitHub Actions 定时执行，不需要自己的服务器。

### 运行方式

1. GitHub Actions 每 30 分钟执行一次 `main.py`（排程按 UTC 计算，GitHub 常会延迟几分钟到十几分钟）。
2. `main.py` 读取 Minecraft Wiki 的披风导航模板 [`Template:Navbox_capes`](https://minecraft.wiki/w/Template:Navbox_capes)，整理出披风清单。
3. 与上次保存在 `state.json` 的清单比对；有变动就发送 Telegram 通知并列出新增的披风，再把新清单 commit 回仓库。没有变动则不做任何事。

只用 Python 标准库，无需安装任何依赖。

### GitHub Secrets

在 [Settings → Secrets and variables → Actions](https://github.com/oddstab/mc-cape-notifier/settings/secrets/actions) 设置。Secret 的值保存后无法查看，只能覆盖。

| Secret 名称 | 说明 |
| :--- | :--- |
| `TG_BOT_TOKEN` | `@BotFather` 签发的 Bot Token（必填） |
| `TG_CHAT_ID` | 接收通知的 Chat ID（可选；未设置时会从 Bot 最近收到的消息自动获取） |

用 `gh` 更新：

```bash
gh secret set TG_BOT_TOKEN   # 交互输入，值不会留在终端记录
gh secret set TG_CHAT_ID
gh secret list               # 只列出名称与更新时间
```

### 手动测试

- 网页：[Actions](https://github.com/oddstab/mc-cape-notifier/actions/workflows/notify.yml) → **Run workflow**，`send_test` 选 `true`，会立即发送一条测试通知。
- 命令：`gh workflow run notify.yml -f send_test=true`
- 本地自检（不发送通知）：`python main.py --check`

### 限制

- 数据来源是社区维护的 Minecraft Wiki，通知速度取决于 Wiki 编辑者的更新速度，可能晚于官方公告。
- 公开仓库连续 60 天没有 commit，GitHub 会自动停用排程并发送邮件通知。到 Actions 页面点击 **Enable workflow** 即可恢复。

---

## 授權 / License

[MIT](LICENSE)
