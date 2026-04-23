import os
import sys
import time
import random
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc74hNLDykqQnTUeJk7gY9pGrhqF1-V4IQi8_xnpgs9_40MKg/viewform?usp=publish-editor"

def jitter(a=0.5, b=1.5):
    time.sleep(random.uniform(a, b))

def fill_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto(FORM_URL, wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle")

            page.screenshot(path="before.png", full_page=True)

            textboxes = page.get_by_role("textbox")
            count = textboxes.count()
            if count == 0:
                raise Exception("No textbox found")

            textboxes.nth(0).click()
            jitter()
            textboxes.nth(0).fill("Max Liang")

            jitter()
            listboxes = page.get_by_role("listbox")
            if listboxes.count() == 0:
                raise Exception("No listbox found")

            listboxes.nth(0).click()
            jitter()
            page.get_by_role("option", name="Gold", exact=True).click()

            jitter(1, 2)
            submit = page.get_by_role("button", name="Submit")
            if submit.count() == 0:
                raise Exception("Submit button not found")

            submit.click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path="after.png", full_page=True)

            print("Done")
        except Exception as e:
            os.makedirs("artifacts", exist_ok=True)
            page.screenshot(path="artifacts/failure.png", full_page=True)
            with open("artifacts/error.txt", "w") as f:
                f.write(str(e) + "\n")
                f.write("URL: " + page.url + "\n")
            print(f"FAILED: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    fill_form()
