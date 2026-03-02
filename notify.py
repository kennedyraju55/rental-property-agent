import os
import urllib.request
import urllib.error
from hoa_check import get_hoa_dues

NTFY_TOPIC = os.environ["NTFY_TOPIC"]
RENT_AMOUNT = 2150

# Build rent message
lines = [f"Rent of ${RENT_AMOUNT:,} is due today! Please collect from your tenant."]

# Append HOA dues info
hoa = get_hoa_dues()
if hoa["success"] and (hoa["balance"] or hoa["due_date"]):
    hoa_parts = []
    if hoa["balance"]:
        hoa_parts.append(f"Current Balance: {hoa['balance']}")
    if hoa["due_date"]:
        hoa_parts.append(f"Last Payment: {hoa['due_date']}")
    lines.append(f"HOA Dues — {' | '.join(hoa_parts)}")
else:
    lines.append("HOA Dues — could not retrieve (check TownSq manually)")

message = "\n".join(lines)

url = f"https://ntfy.sh/{NTFY_TOPIC}"

req = urllib.request.Request(
    url,
    data=message.encode(),
    headers={
        "Title": "Rent & HOA Due Reminder",
        "Priority": "high",
        "Tags": "house,moneybag",
    },
    method="POST"
)

with urllib.request.urlopen(req) as response:
    print(f"✅ Notification sent! Status: {response.status}")
    print(f"Message:\n{message}")
