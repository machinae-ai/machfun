# Description: Scrapes a URL and returns the HTML source from dynamic page using pyppeteer
# Add the following in requirements.txt: pyppeteer==1.0.2
import asyncio
from pyppeteer import launch

async def get_page_dynamic(givenUrl):
    """Scrapes a URL of dynamic page using Pyppeteer.
    
    Args:
        url (string): Fully qualified URL of a page.
    
    Returns:
        Title (string) and Description Text (list).
    """
    #Downloads the browser in next line
    browser = await launch(
        headless=True,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        args= ['--no-sandbox']
    )
    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36')
    
    url = givenUrl
      
    await page.goto(url)
    pageTitle = await page.title()

    pTags = await page.querySelectorAll('p, h1, h2, h3, h4, h5, h6, ul, li, a')
    descriptionText = [await page.evaluate('(element) => element.innerText', p) for p in pTags]

    await browser.close()
    return descriptionText