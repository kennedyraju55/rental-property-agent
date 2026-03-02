import os
import urllib.parse
import urllib.request

PHONE = os.environ["CALLMEBOT_PHONE"]
API_KEY = os.environ["CALLMEBOT_APIKEY"]
RENT_AMOUNT = 2150

message = (
    f"🏠 Rent Reminder: It's the 1st of the month! "
    f"Rent of ${RENT_AMOUNT:,} is due. "
    f"Please collect from your tenant."
)

encoded_message = urllib.parse.quote(message)
url = f"https://api.callmebot.com/whatsapp.php?phone={PHONE}&text={encoded_message}&apikey={API_KEY}"

with urllib.request.urlopen(url) as response:
    body = response.read().decode()
    print(f"Status: {response.status}")
    print(f"Response: {body}")
