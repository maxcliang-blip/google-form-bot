import os
import sys
from playwright.sync_api import sync_playwright

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc74hNLDykqQnTUeJk7gY9pGrhqF1-V4IQi8_xnpgs9_40MKg/viewform?usp=publish-editor"

def ensure_artifacts():
    os.makedirs("artifacts", exist_ok=True)

def snap(page, name):
    page.screenshot(path=f"artifacts/{name}.png", full_page=True)

def step(page, label, fn):
    try:
        fn()
    except Exception as e:
        with open(f"artifacts/{label}-error.txt", "w", encoding="utf-8") as f:
            f.write(repr(e) + "\n")
            f.write("URL: " + page.url + "\n")
        try:
            snap(page, f"{label}-failure")
        except Exception:
            pass
        raise

def main():
    ensure_artifacts()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()

        try:
            step(page, "goto", lambda: page.goto(FORM_URL, wait_until="networkidle"))
            snap(page, "loaded")

            step(page, "fill-name", lambda: page.get_by_role("textbox").first.fill("Max Liang"))
            snap(page, "after-name")

            def choose_gold():
                dropdown = page.get_by_role("listbox").first
                dropdown.click()
                page.wait_for_timeout(700)
                option = page.get_by_role("option", name="Gold", exact=True)
                option.wait_for(state="visible")
                option.click(force=True)

            step(page, "choose-gold", choose_gold)
            snap(page, "after-gold")

            step(page, "submit", lambda: page.get_by_role("button", name="Submit").click())
            page.wait_for_load_state("networkidle")
            snap(page, "submitted")

        finally:
            browser.close()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(1)
