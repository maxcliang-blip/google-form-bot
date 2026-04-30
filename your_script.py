import os
import sys
from playwright.sync_api import sync_playwright

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc74hNLDykqQnTUeJk7gY9pGrhqF1-V4IQi8_xnpgs9_40MKg/viewform?usp=publish-editor"

def ensure_artifacts():
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/started.txt", "w", encoding="utf-8") as f:
        f.write("started\n")

def write_fail(label, err, page=None):
    with open(f"artifacts/{label}-error.txt", "w", encoding="utf-8") as f:
        f.write(repr(err) + "\n")
        if page is not None:
            f.write("URL: " + page.url + "\n")
    if page is not None:
        try:
            page.screenshot(path=f"artifacts/{label}-failure.png", full_page=True)
        except Exception:
            pass

def main():
    ensure_artifacts()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = None
        page = None

        try:
            try:
                context = browser.new_context(storage_state="state.json")
                with open("artifacts/context-ok.txt", "w", encoding="utf-8") as f:
                    f.write("context created\n")
            except Exception as e:
                write_fail("context", e)
                raise

            try:
                page = context.new_page()
                with open("artifacts/page-ok.txt", "w", encoding="utf-8") as f:
                    f.write("page created\n")
            except Exception as e:
                write_fail("page", e, page)
                raise

            try:
                page.goto(FORM_URL, wait_until="networkidle")
                page.screenshot(path="artifacts/loaded.png", full_page=True)
                with open("artifacts/goto-ok.txt", "w", encoding="utf-8") as f:
                    f.write("goto ok\n")
            except Exception as e:
                write_fail("goto", e, page)
                raise

            try:
                page.get_by_role("textbox").first.fill("Max Liang")
                with open("artifacts/name-ok.txt", "w", encoding="utf-8") as f:
                    f.write("name ok\n")
            except Exception as e:
                write_fail("name", e, page)
                raise

            try:
                dropdown = page.get_by_role("listbox").first
                dropdown.click()
                page.wait_for_timeout(700)
                option = page.get_by_role("option", name="Gold", exact=True)
                option.wait_for(state="visible")
                option.click(force=True)
                with open("artifacts/dropdown-ok.txt", "w", encoding="utf-8") as f:
                    f.write("dropdown ok\n")
            except Exception as e:
                write_fail("dropdown", e, page)
                raise

            try:
                page.get_by_role("button", name="Submit").click()
                page.wait_for_load_state("networkidle")
                page.screenshot(path="artifacts/submitted.png", full_page=True)
                with open("artifacts/submit-ok.txt", "w", encoding="utf-8") as f:
                    f.write("submit ok\n")
            except Exception as e:
                write_fail("submit", e, page)
                raise

        finally:
            browser.close()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(1)
