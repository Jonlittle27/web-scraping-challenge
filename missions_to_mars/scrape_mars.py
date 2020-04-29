#dependencies
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)



def scrape():
    #initialize browser and mars data dictionary
    browser = init_browser()
    mars = {}
    #url of page to be scraped
    url = "https://mars.nasa.gov/news/"

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # results are returned as an iterable list
    results = soup.find('div', class_="slide")

    # Identify and return title of article
    news_title = results.find('div', class_="content_title").text
    # capturing the teaser text
    news_p = results.find('div', class_="rollover_description_inner").text

    mars["news_title"] = results.find('div', class_="content_title").text
    mars["news_p"] = results.find('div', class_="rollover_description_inner").text


    #----------------------------------

    #Setting up splinter
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #visting the first vist and obtaining the soup
    browser.visit(url2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #clicking the full image button to direct to the images page
    browser.click_link_by_partial_text('FULL IMAGE')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #clicking more info to direct to the article page
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #clicking the image to direct to the full size image page
    browser.click_link_by_partial_href('/spaceimages/images/largesize/')

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_img_url = soup.find('img')
    featured_img_url = featured_img_url.get('src')

    mars["featured_img_url"]= featured_img_url

    #---------------------------------------

    #pandas scraping
    url3 = 'https://space-facts.com/mars/'

    tables = pd.read_html(url3)

    df = tables[0]

    table_html = df.to_html()

    mars["table_html"] = table_html

    #-------------------------------------

    #scraping hemisphere links and titles
    url3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #visting the intial site and obtaining the soup
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(url3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #navigating to the cerberus site and scraping the data

    results = soup.find_all('div','description')

    hemisphere_img_urls= []

    return mars

    # for result in results:
    
    #     try:
    #          # Identify and return title of hemisphre
    #         title = result.find('h3').text
    #         # Identify and return link to hemisphere picture
        
    #         browser.visit(url4)
        
    #         browser.click_link_by_partial_text(title)
        
    #         html = browser.html
    #         soup = BeautifulSoup(html, 'html.parser')
        
    #         img_url = soup.find('li')
    #         img_url = img_url.a['href']
        
    #         title_dict = {'title': title}
    #         img_dict = {'img_url': img_url}
        
    #         #printing the results for accuracy and appending to the list

    #         if (title and img_url):
                
    #             hemisphere_img_urls.append(title_dict)
    #             hemisphere_img_urls.append(img_dict)
    #     # except AttributeError as e:
    #     #     print(e)

    # # mars = {"news_title":news_title,
    # #     "news_p":news_p,
    # #     "featured_img_url":featured_img_url,
    # #     "table_html":table_html
    # #     # "hemisphere_img_urls":hemisphere_img_urls    
    # # }
