import os
import sys
from playwright.sync_api import sync_playwright

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc74hNLDykqQnTUeJk7gY9pGrhqF1-V4IQi8_xnpgs9_40MKg/viewform?usp=publish-editor"

def write_marker():
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/started.txt", "w", encoding="utf-8") as f:
        f.write("script started\n")

def main():
    write_marker()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()

        try:
            page.goto(FORM_URL, wait_until="networkidle")
            page.screenshot(path="artifacts/loaded.png", full_page=True)

            page.get_by_role("textbox").first.fill("Max Liang")

            dropdown = page.get_by_role("listbox").first
            dropdown.click()
            page.wait_for_timeout(500)

            option = page.get_by_role("option", name="Gold", exact=True)
            option.wait_for(state="visible")
            option.click(force=True)

            page.wait_for_timeout(1000)
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
