from playwright.sync_api import sync_playwright
import os

def render_html_to_png(html_path, output_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Load the HTML file. Need absolute path for file:// protocol or simple local path
        abs_path = os.path.abspath(html_path)
        page.goto(f"file://{abs_path}")

        # Take a screenshot of the container element
        element = page.locator(".container")
        element.screenshot(path=output_path)

        browser.close()

if __name__ == "__main__":
    render_html_to_png("figures/architecture.html", "figures/architecture.png")
