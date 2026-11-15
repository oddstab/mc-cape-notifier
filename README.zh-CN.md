# Minecraft Cape Notifier (Telegram)

[![Minecraft Cape Notifier](https://github.com/oddstab/mc-cape-notifier/actions/workflows/notify.yml/badge.svg)](https://github.com/oddstab/mc-cape-notifier/actions/workflows/notify.yml)

[English](README.en.md) · [繁體中文](README.md) · **简体中文**

Minecraft 出新披风（Cape）时，通过 Telegram Bot 通知你。由 GitHub Actions 定时执行，不需要自己的服务器。

## 运行方式

1. GitHub Actions 每 30 分钟执行一次 `main.py`（排程按 UTC 计算，GitHub 常会延迟几分钟到十几分钟）。
2. `main.py` 读取 Minecraft Wiki 的披风导航模板 [`Template:Navbox_capes`](https://minecraft.wiki/w/Template:Navbox_capes)，整理出披风清单。
3. 与上次保存在 `state.json` 的清单比对；有变动就发送双语 Telegram 通知并列出新增的披风，再把新清单 commit 回仓库。没有变动则不做任何事。

只用 Python 标准库，无需安装任何依赖。

## GitHub Secrets

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

## 手动测试

- 网页：[Actions](https://github.com/oddstab/mc-cape-notifier/actions/workflows/notify.yml) → **Run workflow**，`send_test` 选 `true`，会立即发送一条测试通知。
- 命令：`gh workflow run notify.yml -f send_test=true`
- 本地自检（不发送通知）：`python main.py --check`

## 限制

- 数据来源是社区维护的 Minecraft Wiki，通知速度取决于 Wiki 编辑者的更新速度，可能晚于官方公告。
- 公开仓库连续 60 天没有 commit，GitHub 会自动停用排程并发送邮件通知。到 Actions 页面点击 **Enable workflow** 即可恢复。

## 许可

[MIT](LICENSE)
