import os
import sys
from playwright.sync_api import sync_playwright

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc74hNLDykqQnTUeJk7gY9pGrhqF1-V4IQi8_xnpgs9_40MKg/viewform?usp=publish-editor"

def ensure_artifacts():
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/started.txt", "w", encoding="utf-8") as f:
        f.write("started\n")

def save_error(page, label, err):
    with open(f"artifacts/{label}-error.txt", "w", encoding="utf-8") as f:
        f.write(repr(err) + "\n")
        f.write("URL: " + page.url + "\n")
    try:
        page.screenshot(path=f"artifacts/{label}-failure.png", full_page=True)
    except Exception:
        pass

def do_step(page, label, fn):
    try:
        fn()
        with open(f"artifacts/{label}-ok.txt", "w", encoding="utf-8") as f:
            f.write("ok\n")
    except Exception as e:
        save_error(page, label, e)
        raise

def main():
    ensure_artifacts()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            context = browser.new_context(storage_state="state.json")
            page = context.new_page()

            do_step(page, "goto", lambda: page.goto(FORM_URL, wait_until="networkidle"))
            do_step(page, "name", lambda: page.get_by_role("textbox").first.fill("Max Liang"))

            def choose_gold():
                dropdown = page.get_by_role("listbox").first
                dropdown.click()
                page.wait_for_timeout(700)
                option = page.get_by_role("option", name="Gold", exact=True)
                option.wait_for(state="visible")
                option.click(force=True)

            do_step(page, "dropdown", choose_gold)
            do_step(page, "submit", lambda: page.get_by_role("button", name="Submit").click())

            page.wait_for_load_state("networkidle")
            page.screenshot(path="artifacts/submitted.png", full_page=True)

        finally:
            browser.close()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(1)
