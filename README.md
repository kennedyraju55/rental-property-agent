# 🏠 Rental Property Agent

An automated agent that sends a **monthly email reminder on the 1st of every month** to collect rent, along with the latest **HOA dues** scraped from TownSq.

> **Property:** 121 Groveland Dr, Liberty Hill, TX 78642
> **Rent Amount:** $2,150/month

---

## How It Works

- **GitHub Actions** runs automatically on the 1st of every month at 9:00 AM UTC
- **`hoa_check.py`** logs into [TownSq](https://app.townsq.io) using Playwright (headless Chromium) and scrapes the current HOA balance and last payment date
- **`notify.py`** composes and sends a **Gmail email** containing the rent reminder and HOA dues info

### Sample Email

**Subject:** `🏠 Rent & HOA Due — 121 Groveland Dr, Liberty Hill, TX 78642`

```
Rent of $2,150 is due today! Please collect from your tenant.
HOA Dues — Current Balance: $0.00 | Last Payment: 03/01/2026
```

---

## Setup

### Step 1: Configure GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add the following secrets:

| Secret Name | Description |
|---|---|
| `TOWNSQ_EMAIL` | Email address used to log in to TownSq |
| `TOWNSQ_PASSWORD` | Password for TownSq |
| `GMAIL_APP_PASSWORD` | [Gmail App Password](https://support.google.com/accounts/answer/185833) for sending email |
| `NOTIFY_EMAIL` | Destination email address to receive the reminder |

> **Note:** All four secrets are required. The Gmail App Password is different from your regular Gmail password — generate one in your Google account under **Security → 2-Step Verification → App passwords**.

### Step 2: Test It

Go to **Actions → Monthly Rent Reminder → Run workflow** to trigger it manually and verify you receive the email notification.

A debug screenshot of the TownSq dashboard (`townsq-debug.png`) is uploaded as a workflow artifact after each run (even on failure) to help with troubleshooting.

---

## Project Structure

| File | Description |
|---|---|
| `notify.py` | Sends the monthly rent & HOA reminder email via Gmail SMTP |
| `hoa_check.py` | Logs into TownSq via Playwright and returns HOA balance & last payment date |
| `requirements.txt` | Python dependencies (`requests`, `playwright`) |
| `.github/workflows/rent-reminder.yml` | GitHub Actions workflow (scheduled + manual trigger) |

---

## Schedule

The reminder runs automatically at **9:00 AM UTC on the 1st of every month**.

---

## Future Phases (planned)
- Tenant details tracking
- Expense logging
- Lease renewal reminders
- Monthly income/expense summary
