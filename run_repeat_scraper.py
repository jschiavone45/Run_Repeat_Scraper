from selenium import webdriver
import time
import re
import csv
import math

driver = webdriver.Chrome()
driver.get("https://runrepeat.com/ranking/rankings-of-running-shoes?order_by=score&page=1")


# creating list of product pages

num_products = driver.find_element_by_xpath('//*[@id="rankings-header"]/h1').text
num_products = int(re.findall('\d+', num_products)[0])
total_pages = math.ceil(num_products / 30)
url_list = [f'https://runrepeat.com/ranking/rankings-of-running-shoes?order_by=score&page={i + 1}' for i in range(total_pages)]


product_links = driver.find_elements_by_xpath('//div[@class="product-name hidden-sm hidden-xs"]/a')
product_links = [x.get_attribute('href') for x in product_links]





#begin cycle through each url
for url in url_list:
    # create list of product links to click for current page
    driver.get(url)
    product_links = driver.find_elements_by_xpath('//div[@class="product-name hidden-sm hidden-xs"]/a')
    product_links = [x.get_attribute('href') for x in product_links]
    #cycle through each product_page
    for i in range(len(product_links)):
        driver.get(product_links[i])
        time.sleep(1)


#    #page_num = 1

#while True:
    #print(f'Scraping page {page_num}')
    #products = driver.find_elements_by_xpath('.//div[@class="product-name hidden-sm hidden-xs"]/a/@href')
