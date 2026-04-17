import sys
import os
from playwright.sync_api import sync_playwright

url   = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"
label = f"-{sys.argv[2]}" if len(sys.argv) > 2 else ""

out_dir = os.path.join(os.path.dirname(__file__), "temporary screenshots")
os.makedirs(out_dir, exist_ok=True)

n = 1
while os.path.exists(os.path.join(out_dir, f"screenshot-{n}{label}.png")):
    n += 1
out_path = os.path.join(out_dir, f"screenshot-{n}{label}.png")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(url, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(1000)
    # Trigger all scroll-reveal observers by scrolling through the page
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(800)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(600)
    page.screenshot(path=out_path, full_page=True)
    browser.close()

print(f"Saved: {out_path}")
