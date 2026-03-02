import os
import urllib.request
import urllib.error
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from hoa_check import get_hoa_dues

NTFY_TOPIC = os.environ["NTFY_TOPIC"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
NOTIFY_EMAIL = os.environ["NOTIFY_EMAIL"]
GMAIL_FROM = "rajug058@gmail.com"
RENT_AMOUNT = 2150

# Build message
lines = [f"Rent of ${RENT_AMOUNT:,} is due today! Please collect from your tenant."]

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

# Send Gmail
msg = MIMEMultipart()
msg["From"] = GMAIL_FROM
msg["To"] = NOTIFY_EMAIL
msg["Subject"] = "🏠 Rent & HOA Due Reminder"
msg.attach(MIMEText(message, "plain"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(GMAIL_FROM, GMAIL_APP_PASSWORD)
    server.sendmail(GMAIL_FROM, NOTIFY_EMAIL, msg.as_string())
    print(f"✅ Email sent to {NOTIFY_EMAIL}")
    print(f"Message:\n{message}")

# Also send ntfy push notification
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
    print(f"✅ Push notification sent! Status: {response.status}")
