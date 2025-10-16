import requests
from datetime import date, datetime, timezone, timedelta
import json
from weighting.func_ranking import message

WEBHOOK_URL_REGIME = "https://defaultfaae79b27e8f423993e3c7b5cb5b2e.4b.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/4fd6c1601f964b629b661216b6e77d77/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=iMCAtWfMIRWmYuLWWUtLZUuT4-JpXmHjw6v0IdWXAxE"
WEBHOOK_URL_AA = "https://defaultfaae79b27e8f423993e3c7b5cb5b2e.4b.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/3975339ef26c47829f1d26865d746a7c/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=SK1Fzr1fRsbfp9zxnHNmqaJXO65JR9pIanZLZ8G8qck"
WEBHOOK_URL_WEIGHT = "https://defaultfaae79b27e8f423993e3c7b5cb5b2e.4b.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/2f00424cbc1c4f5b980a178cfc8c2191/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=TFxCCUyEZd5IH2ELFAgK0Rvd19GgayKk1KIlN-p3f-8"

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

def send_teams_message(webhook_url, message):
    headers = {"Content-Type": "application/json"}
    payload = {
        "message": message
    }
    resp = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
    return resp

if __name__ == "__main__":
    # ts = get_bangkok_timestamp(compact=True)
    # print("Sending timestamp:", ts)

    today = date.today().strftime("%Y_%m_%d")

    try:
        # Send regime
        regime = send_timestamp(WEBHOOK_URL_REGIME, today)
        print("Status:", regime.status_code)
        print("Response:", regime.text)

        # Send AA
        asset_allocation = send_timestamp(WEBHOOK_URL_AA, today)
        print("Status:", asset_allocation.status_code)
        print("Response:", asset_allocation.text)

        # Send Weight
        weight = send_teams_message(WEBHOOK_URL_WEIGHT, message)
        print("Status:", weight.status_code)
        print("Response:", weight.text)
    except requests.RequestException as e:
        print("Request failed:", e)
