import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

WIKI_URL = (
    "https://minecraft.wiki/api.php?action=query&prop=revisions"
    "&titles=Template:Navbox_capes&rvslots=main&rvprop=content"
    "&formatversion=2&format=json"
)
STATE_FILE = Path(__file__).with_name("state.json")


def extract_capes(content: str) -> list[str]:
    # 擷取 Wiki 導覽模板中的所有披風名稱
    return sorted(set(re.findall(r"\{\{PersonaLink\|([^|}]+)", content)))


def fetch_wiki_state() -> dict:
    req = urllib.request.Request(
        WIKI_URL, headers={"User-Agent": "MinecraftCapeNotifier/1.0 (https://github.com/oddstab)"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    content = data["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]
    return {
        "hash": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "capes": extract_capes(content),
    }


def tg_api(token: str, method: str, params: dict | None = None) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = urllib.parse.urlencode(params).encode("utf-8") if params else None
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except TimeoutError as exc:
        raise RuntimeError(
            "連線至 Telegram Bot API 逾時：請確認已先在 Telegram 對你的 Bot 按下 Start / 傳送任意訊息，且 Token 的 Bot ID 正確（未誤改數字）。"
        ) from exc


def resolve_chat_id(token: str, env_chat_id: str) -> str:
    if env_chat_id:
        return env_chat_id
    # ponytail: 若未設定 TG_CHAT_ID，從最近一次與機器人的對話自動抓取
    updates = tg_api(token, "getUpdates")
    for item in reversed(updates.get("result", [])):
        for key in ("message", "edited_message", "channel_post", "my_chat_member"):
            chat_id = item.get(key, {}).get("chat", {}).get("id")
            if chat_id:
                return str(chat_id)
    raise RuntimeError("找不到 Chat ID：請先在 Telegram 對你的機器人傳送任意訊息（例如 /start），或設定 TG_CHAT_ID。")


def send_telegram(token: str, chat_id: str, text: str) -> None:
    res = tg_api(token, "sendMessage", {"chat_id": chat_id, "text": text})
    if not res.get("ok"):
        raise RuntimeError(f"Telegram 發送失敗: {res}")


def self_check() -> None:
    sample = "* {{PersonaLink|Pan Cape|Pan}}\n* {{PersonaLink|Copper Cape|Copper}}"
    assert extract_capes(sample) == ["Copper Cape", "Pan Cape"]
    state = fetch_wiki_state()
    assert len(state["hash"]) == 64 and len(state["capes"]) >= 50
    print(f"Self-check OK: {len(state['capes'])} capes, hash={state['hash'][:12]}...")


def main() -> None:
    if "--check" in sys.argv:
        self_check()
        return

    token = os.getenv("TG_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("未設定 TG_BOT_TOKEN 環境變數")

    force_test = "--test" in sys.argv or os.getenv("FORCE_TEST", "").lower() == "true"
    cur = fetch_wiki_state()
    prev = json.loads(STATE_FILE.read_text(encoding="utf-8")) if STATE_FILE.exists() else None

    if force_test:
        chat_id = resolve_chat_id(token, os.getenv("TG_CHAT_ID", "").strip())
        send_telegram(
            token,
            chat_id,
            f"✅ Minecraft 披風通知測試成功！\n目前共追蹤 {len(cur['capes'])} 款披風。\nhttps://minecraft.wiki/w/Cape",
        )
        print(f"已發送測試通知至 chat_id={chat_id}")

    if prev and prev.get("hash") != cur["hash"]:
        chat_id = resolve_chat_id(token, os.getenv("TG_CHAT_ID", "").strip())
        added = [c for c in cur["capes"] if c not in set(prev.get("capes", []))]
        detail = f"新增披風：{', '.join(added)}\n" if added else "Wiki 披風導覽模板內容已變更。\n"
        send_telegram(
            token,
            chat_id,
            f"🚨 Minecraft 新披風通知！\n{detail}https://minecraft.wiki/w/Cape",
        )
        print("偵測到變更，已發送 Telegram 通知。")

    if not prev or prev.get("hash") != cur["hash"]:
        STATE_FILE.write_text(json.dumps(cur, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("已更新 state.json。")
    else:
        print("披風列表無變更。")


if __name__ == "__main__":
    main()
