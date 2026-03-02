import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

HOA_URL = "https://app.townsq.io/w/5d4e0aab529cdf10f9343504/homepage"
LOGIN_URL = "https://app.townsq.io/login"


def get_hoa_dues() -> dict:
    """Login to TownSq and return HOA balance and due date."""
    email = os.environ["TOWNSQ_EMAIL"]
    password = os.environ["TOWNSQ_PASSWORD"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            # Navigate to homepage — will redirect to login if not authenticated
            page.goto(HOA_URL, timeout=30000)

            # Wait for Angular to render, then click "Log in" to reveal the form
            page.wait_for_selector('button:has-text("Log in"), a:has-text("Log in")', timeout=30000)
            page.click('button:has-text("Log in"), a:has-text("Log in")')

            # Now wait for email/password fields to appear
            email_input = page.wait_for_selector(
                'input[type="email"], input[name="email"], input[formcontrolname="email"]',
                timeout=15000
            )
            email_input.fill(email)

            # Two-step login: click Next to reveal password field
            page.click('button:has-text("Next")')

            page.fill('input[type="password"], input[name="password"], input[formcontrolname="password"]', password)
            page.click('button[type="submit"], button:has-text("Sign in"), button:has-text("Log in"), button:has-text("Continue")')

            # Wait for redirect back to homepage after login
            page.wait_for_url("**/homepage**", timeout=20000)

            # Save screenshot of dashboard for debugging
            page.screenshot(path="townsq-debug.png")

            # Data is on the homepage — extract directly
            balance = _extract_balance(page)
            due_date = _extract_due_date(page)

            return {"balance": balance, "due_date": due_date, "success": True}

        except PlaywrightTimeout as e:
            print(f"⚠️ TownSq timeout: {e}")
            try:
                page.screenshot(path="townsq-debug.png")
                print("📸 Screenshot saved: townsq-debug.png")
            except Exception:
                pass
            return {"balance": None, "due_date": None, "success": False, "error": str(e)}
        except Exception as e:
            print(f"⚠️ TownSq error: {e}")
            # Save screenshot for debugging
            try:
                page.screenshot(path="townsq-debug.png")
                print("Screenshot saved to townsq-debug.png")
            except Exception:
                pass
            return {"balance": None, "due_date": None, "success": False, "error": str(e)}
        finally:
            browser.close()


def _extract_balance(page) -> str | None:
    """Extract Current Balance from the Account Information section."""
    import re
    try:
        # Wait for the account info widget to load
        page.wait_for_selector('text=Current Balance', timeout=10000)
        text = page.inner_text("body")
        # "Current Balance:\n$0.00" or "Current Balance: $0.00"
        m = re.search(r'Current Balance[:\s]*\n?\s*(\$[\d,]+\.\d{2})', text)
        if m:
            return m.group(1).strip()
        # Fallback: any dollar amount on page
        matches = re.findall(r'\$[\d,]+\.\d{2}', text)
        if matches:
            return matches[0]
    except Exception:
        pass
    return None


def _extract_due_date(page) -> str | None:
    """Extract Last Payment date from the Account Information section."""
    import re
    try:
        text = page.inner_text("body")
        # "Last payment:\n03/02/2026" or similar
        m = re.search(r'Last payment[:\s]*\n?\s*(\d{2}/\d{2}/\d{4})', text)
        if m:
            return m.group(1).strip()
        # Try other date patterns near "due"
        patterns = [
            r'[Dd]ue\s+[Bb]y\s+([\w\s,]+?\d{4})',
            r'[Dd]ue\s+[Dd]ate[:\s]+([\w\s,/]+)',
            r'\b(\d{1,2}/\d{1,2}/\d{4})\b',
        ]
        for pattern in patterns:
            m = re.search(pattern, text)
            if m:
                return m.group(1).strip()
    except Exception:
        pass
    return None


if __name__ == "__main__":
    result = get_hoa_dues()
    print(result)
