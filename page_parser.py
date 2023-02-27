# Description: Scrapes a URL and returns the HTML source from static page
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re

def get_page(url):
    """Scrapes a URL of static page using Beautiful Soup.
    
    Args:
        url (string): Fully qualified URL of a page.
    
    Returns:
         Title (string) and Description Text (list).
    """
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, 
                         'html.parser', 
                         from_encoding=response.info().get_param('charset'))
    
    title = soup.title.string
    try:
        position = soup.find(attrs={"data-automation": "job-detail-title"}).text
        company = soup.find(attrs={"data-automation": "advertiser-name"}).text
        details = soup.find(attrs={"data-automation": "jobAdDetails"}).get_text(separator='\n')
        salary = soup.find(string=re.compile(r'per (annum|year|month)'))
        text = [position, company, salary, details]
    except:
        desc = soup.find("meta", property="og:description")['content'] or '' 
        tags = soup.select("p, h1, h2, h3, h4, h5, h6, ul")
        text = [item.text+'\n' for item in list(tags)]
    
    print('extracted using bs4')
    return title, text