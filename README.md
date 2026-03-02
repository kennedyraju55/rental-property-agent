# 🏠 Rental Property Agent

A lightweight agent that sends a **push notification on the 1st of every month** reminding you to collect rent.

> **Rent Amount:** $2,150/month

---

## How It Works

- **GitHub Actions** runs a Python script automatically on the 1st of every month at 9:00 AM UTC
- The script sends a push notification via **[ntfy.sh](https://ntfy.sh)** (free, no account needed)
- You receive the notification on your phone via the **Ntfy app**

---

## Setup

### Step 1: Install the Ntfy App on Your Phone

| Platform | Link |
|---|---|
| Android | [Google Play](https://play.google.com/store/apps/details?id=io.heckel.ntfy) |
| iPhone | [App Store](https://apps.apple.com/app/ntfy/id1625396347) |

Open the app → tap **Subscribe to topic** → enter:
```
rental-reminder-rajug058
```

### Step 2: GitHub Secret (already configured)

The following secret is already set in this repository:

| Secret Name | Value |
|---|---|
| `NTFY_TOPIC` | `rental-reminder-rajug058` |

> If you fork this repo, go to **Settings → Secrets and variables → Actions** and add `NTFY_TOPIC` with your own unique topic name.

### Step 3: Test It

Go to **Actions → Monthly Rent Reminder → Run workflow** to trigger it manually and verify you receive the push notification.

---

## Schedule

The reminder runs automatically at **9:00 AM UTC on the 1st of every month**.

---

## Future Phases (planned)
- Tenant details tracking
- Expense logging
- Lease renewal reminders
- Monthly income/expense summary
