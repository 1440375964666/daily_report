import requests
from datetime import datetime, timezone, timedelta
import json

WEBHOOK_URL_REGIME = "https://defaultfaae79b27e8f423993e3c7b5cb5b2e.4b.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/4fd6c1601f964b629b661216b6e77d77/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=iMCAtWfMIRWmYuLWWUtLZUuT4-JpXmHjw6v0IdWXAxE"
WEBHOOK_URL_AA = "https://defaultfaae79b27e8f423993e3c7b5cb5b2e.4b.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/3975339ef26c47829f1d26865d746a7c/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=SK1Fzr1fRsbfp9zxnHNmqaJXO65JR9pIanZLZ8G8qck"

def get_bangkok_timestamp(compact=True):
    # Asia/Bangkok is UTC+7
    tz = timezone(timedelta(hours=7))
    now = datetime.now(tz)
    if compact:
        # compact format: 20251006T153600 (good for ?v=...)
        return now.strftime("%Y%m%dT%H%M%S")
    else:
        # ISO-like with offset: 2025-10-06T15:36:00+07:00
        return now.isoformat()

def send_timestamp(webhook_url, timestamp):
    headers = {"Content-Type": "application/json"}
    payload = {"message": timestamp}   # your adaptive card uses @{triggerBody()?['message']}
    resp = requests.post(webhook_url, json=payload, headers=headers, timeout=15)
    return resp

if __name__ == "__main__":
    ts = get_bangkok_timestamp(compact=True)
    print("Sending timestamp:", ts)
    try:
        # Send regime
        r = send_timestamp(WEBHOOK_URL_REGIME, ts)
        print("Status:", r.status_code)
        print("Response:", r.text)

        # Send AA
        r2 = send_timestamp(WEBHOOK_URL_AA, ts)
        print("Status:", r2.status_code)
        print("Response:", r2.text)
    except requests.RequestException as e:
        print("Request failed:", e)
