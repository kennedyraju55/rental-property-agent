import os
import urllib.request
import urllib.error

NTFY_TOPIC = os.environ["NTFY_TOPIC"]
RENT_AMOUNT = 2150

url = f"https://ntfy.sh/{NTFY_TOPIC}"

req = urllib.request.Request(
    url,
    data=f"Rent of ${RENT_AMOUNT:,} is due today! Please collect from your tenant.".encode(),
    headers={
        "Title": "Rent Due Reminder",
        "Priority": "high",
        "Tags": "house,moneybag",
    },
    method="POST"
)

with urllib.request.urlopen(req) as response:
    print(f"✅ Notification sent! Status: {response.status}")
