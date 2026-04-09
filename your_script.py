from playwright.sync_api import sync_playwright

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc74hNLDykqQnTUeJk7gY9pGrhqF1-V4IQi8_xnpgs9_40MKg/viewform?usp=publish-editor"

def fill_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(FORM_URL, wait_until="domcontentloaded")

        page.get_by_role("textbox").first.fill("Max Liang")
        page.get_by_role("listbox").click()
        page.get_by_role("option", name="Gold", exact=True).click()

        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Submit").click()

        page.wait_for_load_state("networkidle")
        browser.close()

if __name__ == "__main__":
    fill_form()
