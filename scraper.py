import asyncio
import json
from playwright.async_api import async_playwright
from json_tree_viewer import save_structure_to_file

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

from urllib.parse import urlparse, urlunparse

async def find_urls(page):
    """
    Finds all article links on the page and returns a list of unique base URLs.
    Filters out links containing "/all-" and removes fragment identifiers.
    """
    links = await page.query_selector_all("#mainContainer a[href*='/']")
    seen = set()
    unique_hrefs = []

    for link in links:
        href = await link.get_attribute("href")
        if href and "/all-" not in href:
            # Remove fragment
            parsed = urlparse(href)
            base_href = urlunparse(parsed._replace(fragment=""))

            # Preserve order while deduplicating
            if base_href not in seen:
                seen.add(base_href)
                unique_hrefs.append(base_href)

    return unique_hrefs

async def scrape_article(page, url):
    """
        Scrapes the title and content of an article from the given URL.
        Returns a dictionary with 'name', 'link', and 'content'.
    """
    try:
        await page.goto(url, wait_until="domcontentloaded")

        # Extract the title
        title_element = await page.query_selector("h1")
        title = await title_element.inner_text() if title_element else "Untitled"

        # Extract the content
        main_content = await page.query_selector('[data-testid="topic-main-content"]')
        content = await parse_element(main_content, title=title)

        return {
            "name": title.strip(),
            "link": url,
            "content": content
        }
    except Exception as e:
        print(f"⚠️ Failed to scrape {url}: {e}")
        return None

async def extract_introduction(element):
    children = await element.query_selector_all(':scope > *')
    content = ""
    
    for child in children:
        tag = await child.evaluate('(el) => el.tagName')

        if tag == "SECTION":
            return content.strip()  # Stop at the first section

        elif tag == "P":
            if not await child.get_attribute("data-testid") == "topicPara":
                continue
            text = await child.inner_text()
            text = text.strip()
            if text:
                content += text + "\n"

        elif tag == "DIV":
            data_testid = await element.get_attribute("data-testid")
            class_name = await element.get_attribute("class") or ""
            if "Figure" in class_name or data_testid == "baseillustrative":
                continue
            content += await extract_introduction(child)
    return content.strip()

async def get_element_depth(elem, root):
    return await elem.evaluate(
        "(el, root) => { let d = 0; while (el && el !== root) { d++; el = el.parentElement; } return d; }",
        root
    )


async def parse_element(element, title=None):
    content_dict = {}

    # Optional: Store section title
    if not title: 
        first_heading = await element.query_selector('h1, h2, h3, h4, h5, h6')
        title = (await first_heading.inner_text()).strip() if first_heading else "Untitled"
    content_dict["title"] = title

    # Fix: Await this!
    content_dict["content"] = await extract_introduction(element)

    # Parse subsections recursively
    sections = await element.query_selector_all('section')    
    if not sections:
        return content_dict
    reference_depth = await get_element_depth(sections[0], element)

    for section in sections:
        depth = await get_element_depth(section, element)
        if depth != reference_depth:
            continue
        section_content = await parse_element(section)
        section_title = section_content.get("title", "Untitled Section")
        content_dict[section_title] = section_content

    return content_dict



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
    playwright, browser, page = await init_browser(headless=True)
    base_url = "https://www.merckvetmanual.com/dog-owners"
    await page.goto(base_url)
    await page.wait_for_timeout(2000)
    await accept_cookies(page)

    urls = await find_urls(page)
    for i, url in enumerate(urls): 
        print(url + '\n')
        if i > 100: 
            break

    articles = []
    for i, url in enumerate(urls):
        print(f"Scraping article {i + 1}/{len(urls)}: {"https://www.merckvetmanual.com" + url}")
        article = await scrape_article(page, "https://www.merckvetmanual.com" + url)
        if not article:
            print(f"⚠️ Failed to scrape article {i + 1}")
            continue
        articles.append(article)
        

    await save_to_json(articles, filename="merck_articles.json")
    save_structure_to_file("merck_articles.json")

    await browser.close()
    await playwright.stop()

if __name__ == "__main__":
    asyncio.run(main())