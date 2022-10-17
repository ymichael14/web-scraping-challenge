
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import ssl
import requests

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    title, paragraph = news(browser)

    data = {
        'title': title,
        'paragraph': paragraph,
        'image': image(browser),
        'facts': facts(),
        'hemispheres': hemisphere(browser)
    }
    return data

def news(browser):
    browser.visit('https://redplanetscience.com/')

    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')
    results=soup.find_all('section', class_='image_and_description_container')#the large section of stories 
    headline_div=results[0].find_all('div', class_='content_title')#the div that contains the headline text
    news_parag_teaser=results[0].find_all('div', class_='article_teaser_body')
    return headline_div[0].text, news_parag_teaser[0].text

def image(browser):
    browser.visit('https://spaceimages-mars.com/')
    html_image=browser.html
    soup=BeautifulSoup(html_image, 'html.parser')
    src=soup.select('.headerimage.fade-in')[0]['src']
    return 'https://spaceimages-mars.com/'+src


def facts(): 
    url='https://galaxyfacts-mars.com/'
    mars_facts=pd.read_html(url)[1]
    mars_facts.columns=['Metric', 'Value']
    return mars_facts.to_html('mars_facts_from_web.html', index=False)
     
def hemisphere(browser):
    browser.visit('https://marshemispheres.com/')
    hemisphere_page=browser.html
    soup= BeautifulSoup(hemisphere_page, 'html.parser') 

    img_results=soup.find_all('h3')
    img_results=img_results[:4]
    hemispheres_mars=[]
    for item in img_results: 
        hemispheres_mars.append(item.text)

    browser.visit('https://marshemispheres.com/')
    complete_url_list=[]
    for x in range(4):
        browser.links.find_by_partial_text(hemispheres_mars[x]).click()
        hemisphere_image=browser.html
        soup = BeautifulSoup(hemisphere_image, 'html.parser') 
        image_url_end=soup.find_all('img', class_='wide-image')[0]['src']
        complete_url='https://marshemispheres.com/'+image_url_end
        complete_url_list.append(complete_url)
        browser.links.find_by_partial_text('Back').click()

    hemisphere_mars_url_img=[{'title':hemispheres_mars[0], 'img_url':complete_url_list[0]},
                            {'title':hemispheres_mars[1], 'img_url':complete_url_list[1]},
                            {'title':hemispheres_mars[2], 'img_url':complete_url_list[2]},
                            {'title':hemispheres_mars[3], 'img_url':complete_url_list[3]}
                            ]
    return hemisphere_mars_url_img




