import os
from playwright.sync_api import sync_playwright

url = "http://localhost:3000"
out_dir = os.path.join(os.path.dirname(__file__), "temporary screenshots")
os.makedirs(out_dir, exist_ok=True)

def save(page, name):
    n = 1
    while os.path.exists(os.path.join(out_dir, f"ss-{name}-{n}.png")):
        n += 1
    path = os.path.join(out_dir, f"ss-{name}-{n}.png")
    page.screenshot(path=path, clip={"x":0,"y":0,"width":1440,"height":900})
    print(f"  {name}: {path}")
    return path

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(url, wait_until="networkidle", timeout=30000)

    # --- HERO: capture before any scroll, after CSS anims settle ---
    page.wait_for_timeout(1800)
    save(page, "hero")

    # Force-show all scroll-reveal elements
    page.evaluate("""
        document.querySelectorAll('.rv').forEach((el, i) => {
            el.style.transitionDelay = (i % 4) * 0.04 + 's';
            el.classList.add('on');
        });
    """)
    page.wait_for_timeout(400)

    # Screenshot each section at its scroll position
    sections = [
        ("about",      840),
        ("statement",  1940),
        ("benefits",   2460),
        ("community",  3560),
        ("cta",        4680),
        ("footer",     5380),
    ]
    for name, y in sections:
        page.evaluate(f"document.documentElement.style.scrollBehavior='auto'; window.scrollTo(0,{y});")
        page.wait_for_timeout(250)
        save(page, name)

    browser.close()
print("Done.")
