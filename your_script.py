import os
import sys
from playwright.sync_api import sync_playwright

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc74hNLDykqQnTUeJk7gY9pGrhqF1-V4IQi8_xnpgs9_40MKg/viewform?usp=publish-editor"

def fill_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto(FORM_URL, wait_until="networkidle")

            page.screenshot(path="step1-loaded.png", full_page=True)

            # Try filling by label text if you know the question text.
            # Replace these labels with the exact form question text.
            page.get_by_label("Your name").fill("Max Liang")
            page.get_by_label("Plan").click()

            page.get_by_role("option", name="Gold", exact=True).click()

            page.wait_for_timeout(2000)

            submit = page.get_by_role("button", name="Submit")
            submit.click()

            page.wait_for_load_state("networkidle")
            page.screenshot(path="step2-submitted.png", full_page=True)

            print("Done")

        except Exception as e:
            os.makedirs("artifacts", exist_ok=True)
            page.screenshot(path="artifacts/failure.png", full_page=True)
            with open("artifacts/error.txt", "w") as f:
                f.write(str(e))
            print(f"FAILED: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    fill_form()
