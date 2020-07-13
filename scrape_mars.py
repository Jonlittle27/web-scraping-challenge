import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #url of news page to be scraped
    news_url = "https://mars.nasa.gov/news/"

    browser.visit(news_url)
    html = browser.html

    # Parse HTML with Beautiful Soup  
    soup = BeautifulSoup(html, "html.parser")

    # Get article title and paragraph text
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text

    #Url for JPL Image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #clicking the full image button to direct to the images page
    browser.click_link_by_partial_text('FULL IMAGE')
    html = browser.html

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

    #Mars weather
    # Visit Twitter url for latest Mars Weather
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tweet_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Extract latest tweet
    tweet_container = soup.find_all('div', class_="js-tweet-text-container")

    mars_weather =[]

    # Loop through latest tweets and find the tweet that has weather information
    for tweet in tweet_container: 
        mars_weather = tweet.find('p').text
        if 'sol' and 'pressure' in mars_weather:
            mars_weather.append(mars_weather)
            break
        else: 
            pass

    #Mars Facts with Pandas

    facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(facts_url)

    df = tables[0]

    table_html = df.to_html()

    #Mars Hemispheres

    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(hemi_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #navigating to the cerberus site and scraping the data

    results = soup.find_all('div','description')

    hemisphere_img_urls= []

    for result in results:
    
        try:
             # Identify and return title of hemisphre
            title = result.find('h3').text
            # Identify and return link to hemisphere picture
        
            browser.visit(hemi_url)
        
            browser.click_link_by_partial_text(title)
        
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
        
            img_url = soup.find('li')
            img_url = img_url.a['href']
        
            title_dict = {'title': title}
            img_dict = {'img_url': img_url}
        
        

            if (title and img_url):
                print('-------------')
                print(title)
                print(img_url)
                hemisphere_img_urls.append(title_dict)
                hemisphere_img_urls.append(img_dict)
        except AttributeError as e:
            print(e) 

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_img_url": featured_img_url,
        "mars_weather": mars_weather,
        "mars_facts": table_html,
        "hemisphere_image_urls": hemisphere_img_urls
    }

    #Close Browser and return results

    browser.quit()

    return mars_data

if __name__ == '__main__':
    scrape()




