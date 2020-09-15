# DEPENDENCIES
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

# SCRAPE FUNCTION
def scrape_mars():
    
    scrape_result = {}
    
    # Initialize browser object
    browser = init_browser()
    
    # -----------
    # Scrape news
    # -----------
    
    # Visit site
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    
    # Instantiate BS object
    html = browser.html
    soup = bs(html, "html.parser")
    
    # Find news slide
    news_slide = soup.find('li', class_='slide')

    # Scrape slide title
    news_title = news_slide.find('div', class_='content_title').get_text()

    # Scrape slide text
    news_preview  = news_slide.find('div', class_='article_teaser_body').get_text()

    # Store data in a dictionary
    news_data = {

        "title": news_title,
        "content": news_preview
    }
    
    scrape_result['news'] = news_data
    
    # -----------
    # Scrape JPL
    # -----------
    
    # Visit site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    # Instantiate BS object
    html = browser.html
    soup = bs(html, "html.parser")

    # Find featured image link
    img_url = soup('article', class_='carousel_item')[0]['style'][23:-3]
    jpl_url = "https://www.jpl.nasa.gov" + img_url
    
    scrape_result['jpl'] = jpl_url
    
    # ------------------------
    # Scrape Space Facts Table
    # ------------------------
    
    # Use Pandas html function to scrape Space Facts table
    df = pd.read_html(url)[0]

    # Convert dataframe back into html
    page_table = df.to_html()
    
    scrape_result['fact_table'] = page_table
    
    # --------------------------
    # Scrape Astrogeology Images
    # --------------------------
    
    # Visit astrogeology site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(1)

    # Instantiate BS object
    html = browser.html
    soup = bs(html, "html.parser")

    # Find page link containers
    link_list_raw = soup.find_all('a', class_='itemLink product-item')

    # Extract page urls and concatenate with base url for Splinter
    link_list = []
    base_url = "https://astrogeology.usgs.gov"
    for item in link_list_raw:
        if item['href'] not in link_list:
            link_list.append(item['href'])

    searches = [base_url + item for item in link_list]
    
    # Create list of dictionaries
    dictionary_list = []
    for link in searches:
        dictionary = {}
        browser.visit(link)
        html = browser.html
        soup = bs(html, "html.parser")
        img_url = soup.find('img', class_='wide-image')['src']
        raw_title = soup.find('h2', class_='title').text.split()
        title = " ".join(raw_title[:-1])
        dictionary['title'] = title
        dictionary['img_url'] = base_url + img_url
        dictionary_list.append(dictionary)
        browser.back()
        
    scrape_result['astrogeo'] = dictionary_list
        
    # Close browser
    browser.quit()
    
    # Return results
    return scrape_result