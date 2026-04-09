import os
import sys
from playwright.sync_api import sync_playwright, TimeoutError

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc74hNLDykqQnTUeJk7gY9pGrhqF1-V4IQi8_xnpgs9_40MKg/viewform?usp=publish-editor"

def save_failure(page, error_msg):
    """Save screenshot and logs when something fails"""
    os.makedirs("artifacts", exist_ok=True)
    
    # Screenshot
    screenshot_path = "artifacts/failure-screenshot.png"
    page.screenshot(path=screenshot_path)
    
    # Page logs
    logs_path = "artifacts/page-logs.txt"
    with open(logs_path, "w") as f:
        f.write(f"Error: {error_msg}\n")
        f.write(f"URL: {page.url}\n")
        f.write("Console logs:\n")
        f.write("\n".join(page.context.console_message_texts()))
    
    print(f"Saved artifacts to {screenshot_path} and {logs_path}")

def fill_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            
            page.goto(FORM_URL, wait_until="domcontentloaded")
            
            page.get_by_role("textbox").first.fill("Max Liang")
            page.get_by_role("listbox").click()
            page.get_by_role("option", name="Gold", exact=True).click()
            
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Submit").click()
            
            page.wait_for_load_state("networkidle")
            print("SUCCESS: Form submitted")
            
        except Exception as e:
            print(f"FAILED: {e}")
            save_failure(page, str(e))
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    fill_form()
