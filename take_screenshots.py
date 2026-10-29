"""Take screenshots of the main views with Playwright. Usage: python take_screenshots.py [url]"""
import sys
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8599"
OUT = "screenshots"
errors = []


def settle(page, t=1500):
    page.wait_for_timeout(t)
    page.wait_for_selector('[data-testid="stStatusWidget"]', state="detached", timeout=60000) if page.query_selector('[data-testid="stStatusWidget"]') else None
    page.wait_for_timeout(800)


with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    page = b.new_page(viewport={"width": 1500, "height": 1100})
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(URL)
    page.wait_for_selector("text=One split vs K-fold", timeout=90000)
    settle(page, 4000)
    page.screenshot(path=f"{OUT}/01-full-page.png", full_page=True)
    page.screenshot(path=f"{OUT}/02-top-single-vs-kfold.png")
    page.locator('[data-testid="stMain"]').first.evaluate("e=>e.scrollTo(0,420)")
    page.wait_for_timeout(800)
    page.screenshot(path=f"{OUT}/02b-single-vs-kfold-charts.png")
    page.get_by_role("button", name="Reshuffle").click()
    settle(page, 3000)
    page.screenshot(path=f"{OUT}/03-after-reshuffle.png")
    # leakage section
    page.get_by_text("Before the split (leaks)").click()
    settle(page, 3000)
    page.get_by_text("Leakage: when the test data").scroll_into_view_if_needed()
    page.wait_for_timeout(800)
    page.screenshot(path=f"{OUT}/04-leakage-switch-on.png")
    page.get_by_text("See a leak that really hurts").click()
    page.wait_for_timeout(1200)
    page.screenshot(path=f"{OUT}/05-leakage-noise-demo.png")
    # advisor
    page.get_by_text("Small data or large data?").first.scroll_into_view_if_needed()
    page.wait_for_timeout(800)
    page.screenshot(path=f"{OUT}/06-advisor.png")
    # stratified imbalanced dataset
    page.locator('[data-testid="stMain"]').first.evaluate("e=>e.scrollTo(0,0)")
    page.locator('[role=combobox][aria-label="Dataset"]').click()
    page.get_by_role("option", name="Synthetic imbalanced (1,000 rows, 5% positive)").click()
    settle(page, 5000)
    page.evaluate("window.scrollTo(0,0)"); page.locator('section.main, [data-testid="stMain"]').first.evaluate("e=>e.scrollTo(0,0)")
    page.wait_for_timeout(800)
    page.screenshot(path=f"{OUT}/07-imbalanced-dataset.png")
    page.get_by_text("Small data or large data?").first.scroll_into_view_if_needed()
    page.wait_for_timeout(800)
    page.screenshot(path=f"{OUT}/08-advisor-imbalanced.png")
    # CSV upload
    page.locator('[data-testid="stMain"]').first.evaluate("e=>e.scrollTo(0,0)")
    page.locator('[data-testid="stSidebar"]').get_by_text("Upload my CSV").click()
    settle(page, 1500)
    page.set_input_files('input[type="file"]', "sample_data/customer_churn_sample.csv")
    settle(page, 5000)
    page.locator('[data-testid="stMain"]').first.evaluate("e=>e.scrollTo(0,0)")
    page.wait_for_timeout(800)
    page.screenshot(path=f"{OUT}/09-csv-upload.png")
    b.close()
print("page errors:", errors)
