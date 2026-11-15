# Minecraft Cape Notifier (Telegram)

[![Minecraft Cape Notifier](https://github.com/oddstab/mc-cape-notifier/actions/workflows/notify.yml/badge.svg)](https://github.com/oddstab/mc-cape-notifier/actions/workflows/notify.yml)

**English** · [繁體中文](README.md) · [简体中文](README.zh-CN.md)

Get a Telegram message when Minecraft releases a new cape. Runs on GitHub Actions, so no server of your own is needed.

## How it works

1. GitHub Actions runs `main.py` every 30 minutes (the schedule is UTC; GitHub often delays runs by several minutes).
2. `main.py` reads the cape navigation template [`Template:Navbox_capes`](https://minecraft.wiki/w/Template:Navbox_capes) from the Minecraft Wiki and builds the current cape list.
3. It compares that list with the one saved in `state.json`. If something changed, it sends a bilingual Telegram message listing the newly added capes and commits the new list back to the repository. If nothing changed, it does nothing.

Standard library only — no dependencies to install.

## GitHub Secrets

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

## Manual test

- Web: [Actions](https://github.com/oddstab/mc-cape-notifier/actions/workflows/notify.yml) → **Run workflow**, set `send_test` to `true` to receive a test message immediately.
- CLI: `gh workflow run notify.yml -f send_test=true`
- Local self-check (sends nothing): `python main.py --check`

## Limitations

- The data comes from the community-maintained Minecraft Wiki, so notifications arrive as fast as wiki editors update the page and may lag behind official announcements.
- GitHub disables scheduled workflows on public repositories after 60 days without commits and emails you about it. Open the Actions tab and press **Enable workflow** to resume.

## License

[MIT](LICENSE)
