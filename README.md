# 🏠 Rental Property Agent

A lightweight agent that sends a **WhatsApp notification on the 1st of every month** reminding you to collect rent.

> **Rent Amount:** $2,150/month

---

## Setup

### Step 1: Register with Callmebot (one-time)

1. Save **+34 644 77 68 09** as a contact in WhatsApp (name it "CallMeBot")
2. Send this exact message to that number:
   ```
   I allow callmebot to send me messages
   ```
3. You'll receive a reply with your **API key** — save it!

### Step 2: Create GitHub Repository

1. Create a new repo at [github.com/new](https://github.com/new) named `rental-property-agent`
2. Push this code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/rental-property-agent.git
   git branch -M main
   git add .
   git commit -m "Initial commit: monthly rent reminder"
   git push -u origin main
   ```

### Step 3: Add GitHub Secrets

Go to your repo → **Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Value |
|---|---|
| `CALLMEBOT_PHONE` | Your WhatsApp number with country code (e.g. `+12025551234`) |
| `CALLMEBOT_APIKEY` | The API key you received from Callmebot |

### Step 4: Test It

Go to **Actions → Monthly Rent Reminder → Run workflow** to trigger it manually and verify you receive the WhatsApp message.

---

## Schedule

The reminder runs automatically at **9:00 AM UTC on the 1st of every month**.

---

## Future Phases (planned)
- Tenant details tracking
- Expense logging
- Lease renewal reminders
- Monthly income/expense summary
