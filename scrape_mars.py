# This code is imported by app.py. App.py calls the scrape function here to scrape Mars data from 
# various websites and return in the dictionary.

# Import dependencies.
import pandas as pd
from pprint import pprint
import time
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup
import pymongo

# Initial dictionary to be populated in scrape function
mars_dict = {}

# Scrape function calls other functions below that use browser to 
# collect Mars information from various websites.
def scrape():

    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_p = get_mars_news(browser)

    mars_dict = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image_url": get_featured_image_url(browser), 
        "mars_tweet": get_mars_tweet(browser),
        "mars_facts_html": get_mars_facts(),
        "hemispheres": get_hemispheres(browser),  
    }

    browser.quit()

    return mars_dict


def get_mars_news(browser):

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)

    mars_html = browser.html
    mars_soup = BeautifulSoup(mars_html, 'html.parser')

    try:
        news_title = mars_soup.find('ul', class_="item_list").find('li',class_="slide"). find('div',class_="content_title").text
        print(f"news_title = {news_title}") 
    
        news_p = mars_soup.find('ul',class_="item_list").find('li',class_="slide"). \
        find('div',class_="article_teaser_body").text
        print(f"news_p = {news_p}")
    
    except AttributeError as e:
        print(e)

    return news_title, news_p    

def get_featured_image_url(browser):
 
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)

    # Find and click the Full Image button
    full_image_button = browser.find_by_id('full_image')
    full_image_button.click()
    time.sleep(2)

    # Find and click more info button
    more_info_button = browser.find_link_by_partial_text('more info')
    more_info_button.click()
    time.sleep(2)
    mars_html = browser.html
    mars_images_soup = BeautifulSoup(mars_html, 'html.parser')

    # Get featured_image_url
    try:    
        url = mars_images_soup.find('figure', class_='lede').a['href']
        print(f"url: {url}") 
    
    except AttributeError:
        return None

    featured_image_url = "https://www.jpl.nasa.gov" + url
    print(f"full url: {featured_image_url}") 

    return featured_image_url


def get_mars_tweet(browser):

    url = 'https://twitter.com/marswxreport?lang=en)'
    browser.visit(url)
    mars_weather_html = browser.html
    mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')
    mars_tweet = mars_weather_soup.find('p', class_='TweetTextSize').text
    print(f"tweet: {mars_tweet}") 

    return mars_tweet

def get_mars_facts():

    url = 'https://space-facts.com/mars/'
    earth_mars_facts = pd.read_html(url)
    mars_facts_df = earth_mars_facts[1]
    mars_facts_df.columns = ['Mars Attribute','Value']
    mars_facts_df.set_index('Mars Attribute', inplace=True)
    mars_facts_df
    
    return mars_facts_df.to_html()


def get_hemispheres(browser):

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    usgs_soup = BeautifulSoup(html, 'html.parser')

    # Get list of hemisphere blocks
    hemisphere_blocks = usgs_soup.find('div', class_='collapsible results').find_all('div',class_='item')

    # Initialize list
    hemisphere_images = []

    # Loop through hemisphere results and append to list
    for hemisphere in hemisphere_blocks:
    
        # Get title and cut off 'enhanced' from end
        title = hemisphere.find('div', class_='description').find('a', class_='itemLink product-item').h3.text
        if title.endswith(' Enhanced'):
            title = title[:-9]  
        # Construct each hemisphere image URL
        url = 'https://astrogeology.usgs.gov'
        full_url = url + hemisphere.find('a',class_='itemLink product-item')['href']    
        browser.visit(full_url)
        time.sleep(3)
    
        usgs_html = browser.html
        image_soup = BeautifulSoup(usgs_html,'html.parser')
        image_url = image_soup.find('div',class_='downloads').a['href']
    
        hemisphere_dict = {"title": title,"image_url": image_url}

        # Construct list of hemisphere dictionaries  
        hemisphere_images.append(hemisphere_dict)

        pprint(hemisphere_images)
    
        # take browser back
        browser.back()

    return hemisphere_images