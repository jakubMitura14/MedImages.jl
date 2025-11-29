import os
import sys
from playwright.sync_api import sync_playwright

def render_html_to_png(html_path, output_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Load the HTML file
        abs_path = os.path.abspath(html_path)
        page.goto(f"file://{abs_path}")
        # Take a screenshot of the container element
        element = page.locator(".container")
        element.screenshot(path=output_path)
        browser.close()
        print(f"Successfully created {output_path}")

if __name__ == "__main__":
    html_file = "figures/architecture.html"
    png_file = "figures/architecture.png"

    if not os.path.exists(html_file):
        print(f"Error: {html_file} not found.")
        sys.exit(1)

    try:
        render_html_to_png(html_file, png_file)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
