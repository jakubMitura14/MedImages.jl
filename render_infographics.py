import os
from playwright.sync_api import sync_playwright

def render_html_to_png(html_file, png_file):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 800, "height": 450})

        # Get absolute path
        abs_path = "file://" + os.path.abspath(html_file)
        page.goto(abs_path)

        # Wait a moment for rendering
        page.wait_for_timeout(1000)

        # Screenshot the container element
        container = page.locator('.container')
        container.screenshot(path=png_file)

        print(f"Rendered {html_file} -> {png_file}")
        browser.close()

if __name__ == "__main__":
    files = [
        ('elsarticle/figures_new/challenge_1.html', 'elsarticle/figures_new/challenge_1.png'),
        ('elsarticle/figures_new/challenge_2.html', 'elsarticle/figures_new/challenge_2.png'),
        ('elsarticle/figures_new/challenge_3.html', 'elsarticle/figures_new/challenge_3.png'),
        ('elsarticle/figures_new/challenge_4.html', 'elsarticle/figures_new/challenge_4.png')
    ]

    for html, png in files:
        render_html_to_png(html, png)
