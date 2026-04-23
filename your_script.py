import os
import sys
from playwright.sync_api import sync_playwright

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc74hNLDykqQnTUeJk7gY9pGrhqF1-V4IQi8_xnpgs9_40MKg/viewform?usp=publish-editor"

def main():
    os.makedirs("artifacts", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(FORM_URL, wait_until="networkidle")
            page.screenshot(path="artifacts/loaded.png", full_page=True)

            page.get_by_label("Your name").fill("Max Liang")
            page.get_by_label("Plan").click()
            page.get_by_role("option", name="Gold", exact=True).click()

            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Submit").click()

            page.wait_for_load_state("networkidle")
            page.screenshot(path="artifacts/submitted.png", full_page=True)

        except Exception as e:
            with open("artifacts/error.txt", "w", encoding="utf-8") as f:
                f.write(repr(e) + "\n")
                f.write("Current URL: " + page.url + "\n")
            page.screenshot(path="artifacts/failure.png", full_page=True)
            raise
        finally:
            browser.close()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(1)
