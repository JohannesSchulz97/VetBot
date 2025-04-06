import asyncio
import json
from playwright.async_api import async_playwright

"""
    Initializes the browser using Playwright with headless or non-headless mode.
    Returns the browser context and page object.
"""
async def init_browser(headless=True):
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=headless)
    context = await browser.new_context(viewport={"width": 1200, "height": 800})
    page = await context.new_page()
    return playwright, browser, page

"""
    Tries to accept the cookie banner if it exists on the page.
    Prevents interference with future button clicks.
"""
async def accept_cookies(page):
    try:
        await page.click("#onetrust-accept-btn-handler", timeout=5000)
        print("Accepted cookies.")
        await page.wait_for_timeout(1000)
    except Exception as e:
        print("No cookie banner found or could not click it:", e)

"""
    Finds all collapsed sections and expands them by clicking.
    Only clicks buttons with class names containing 'SectionDataComponent' or 'AccordionSectionComponent'.
"""
async def expand_all_sections(page, max_rounds=10, headless=False):
    expanded_count = 0

    for round_num in range(max_rounds):
        print(f"\n🔁 Expansion round {round_num + 1}")
        buttons = await page.query_selector_all('button[aria-expanded="false"]')
        clicked_this_round = 0
        for i, button in enumerate(buttons):
    
            try:
                class_name = await button.get_attribute("class") or ""
                if "SectionDataComponent" not in class_name and "AccordionSectionComponent" not in class_name:
                    continue

                # Scroll into view and click
                await button.scroll_into_view_if_needed()
                if headless: 
                    await button.click()
                else:
                    await page.wait_for_timeout(100)
                    await button.click()
                    await page.wait_for_timeout(100)

                expanded_count += 1
                clicked_this_round += 1

            except Exception as e:
                print(f"⚠️ Could not click button #{i}: {e}")
                continue
            if expanded_count > 10:
                await page.wait_for_timeout(1000)
                return

        if clicked_this_round == 0:
            print("✅ No more buttons to expand.")
            break

    print(f"\n✅ Finished. Expanded {expanded_count} sections total.")

async def find_urls(page):
    """
        Finds all article links on the page and returns a list of unique URLs.
        Filters out links containing "/all-".
    """
    links = await page.query_selector_all("#mainContainer a[href*='/']")
    hrefs = set([await link.get_attribute("href") for link in links if "/all-" not in await link.get_attribute("href")])
    return list(hrefs)

async def scrape_article(page, url):
    """
        Scrapes the title and content of an article from the given URL.
        Returns a dictionary with 'name', 'link', and 'content'.
    """
    try:
        await page.goto(url)
        await page.wait_for_timeout(1500)  # Wait for the page to load

        # Extract the title
        title_element = await page.query_selector("h1")
        title = await title_element.inner_text() if title_element else "Untitled"

        # Extract the content
        content_element = await page.query_selector(".content-section")
        content = await content_element.inner_text() if content_element else "No content available"

        return {
            "name": title.strip(),
            "link": url,
            "content": content.strip()
        }
    except Exception as e:
        print(f"⚠️ Failed to scrape {url}: {e}")
        return None

async def save_to_json(data, filename="articles.json"):
    """
        Saves a list of articles to a JSON file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(data)} articles to {filename}")

"""
    Main function to launch browser, navigate to site, and run actions.
"""
async def main():
    playwright, browser, page = await init_browser(headless=False)
    await page.goto("https://www.merckvetmanual.com/dog-owners")
    await page.wait_for_timeout(2000)

    await accept_cookies(page)
    await expand_all_sections(page, headless=False)
    urls = await find_urls(page)
    print(f"Found {len(urls)} articles")

    articles = []
    for i, url in enumerate(urls):
        print(f"Scraping article {i + 1}/{len(urls)}: {url}")
        article = await scrape_article(page, url)
        if article and len(article["content"]) > 100:  # Ignore very short articles
            articles.append(article)

    await save_to_json(articles, filename="merck_articles.json")

    input("\nPress Enter to close the browser...")
    await browser.close()
    await playwright.stop()

if __name__ == "__main__":
    asyncio.run(main())