#!/usr/bin/env python3
import sys
import json
import requests

# 1) CAMBIA ESTO por tu chat_id (privado o grupo)
CHAT_ID = "PEGA_AQUI_TU_CHAT_ID"

def main():
    # Wazuh pasa: 1) alert file, 2) api_key (no lo usamos), 3) hook_url
    alert_path = sys.argv[1]
    hook_url = sys.argv[3]

    with open(alert_path, "r", encoding="utf-8") as f:
        alert_json = json.load(f)

    rule = alert_json.get("rule", {})
    agent = alert_json.get("agent", {})

    level = rule.get("level", "N/A")
    desc  = rule.get("description", "N/A")
    rid   = rule.get("id", "N/A")
    aname = agent.get("name", "manager")
    aip   = agent.get("ip", "-")
    ts    = alert_json.get("timestamp", "-")
    loc   = alert_json.get("location", "-")

    text = (
        f"🚨 Wazuh alert\n"
        f"Level: {level}\n"
        f"Rule: {rid} - {desc}\n"
        f"Agent: {aname} ({aip})\n"
        f"Time: {ts}\n"
        f"Location: {loc}\n"
    )

    payload = {"chat_id": CHAT_ID, "text": text}
    r = requests.post(hook_url, json=payload, timeout=10)
    r.raise_for_status()

if __name__ == "__main__":
    main()
