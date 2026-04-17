import sys
import os
from playwright.sync_api import sync_playwright

url   = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"
label = sys.argv[2] if len(sys.argv) > 2 else "section"

out_dir = os.path.join(os.path.dirname(__file__), "temporary screenshots")
os.makedirs(out_dir, exist_ok=True)

n = 1
while os.path.exists(os.path.join(out_dir, f"screenshot-{n}-{label}.png")):
    n += 1
out_path = os.path.join(out_dir, f"screenshot-{n}-{label}.png")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(url, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(1200)
    # trigger all scroll reveals first
    # Trigger all scroll-reveal observers
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(700)
    # Disable smooth scroll, jump to top instantly
    page.evaluate("document.documentElement.style.scrollBehavior='auto'; window.scrollTo(0,0);")
    page.wait_for_timeout(400)
    page.screenshot(path=out_path, clip={"x":0,"y":0,"width":1440,"height":900})
    browser.close()

print(f"Saved: {out_path}")
