from selenium import webdriver
import time
import re
import csv
import math

driver = webdriver.Chrome()
driver.get("https://runrepeat.com/ranking/rankings-of-running-shoes?page=1")


# creating list of product pages

num_products = driver.find_element_by_xpath('//*[@id="rankings-header"]/h1').text
num_products = int(re.findall('\d+', num_products)[0])
total_pages = math.ceil(num_products / 30)
url_list = [f'https://runrepeat.com/ranking/rankings-of-running-shoes?page={i + 1}' for i in range(total_pages)]


product_links = driver.find_elements_by_xpath('//div[@class="product-name hidden-sm hidden-xs"]/a')
product_links = [x.get_attribute('href') for x in product_links]





#begin cycle through each url
for url in url_list:

    # create list of product links to click for current page
    driver.get(url)
    product_links = driver.find_elements_by_xpath('//div[@class="product-name hidden-sm hidden-xs"]/a')
    product_links = [x.get_attribute('href') for x in product_links]

    #cycle through each product_page and scrape fields
    for i in range(len(product_links)):
        driver.get(product_links[i])

        driver.execute_script("window.scrollTo(0, 1900);")
        time.sleep(1)
        #clicking to expand table
        try:
            more_facts_button = driver.find_element_by_xpath('//div[@class="btn-more-container"]')
            more_facts_button.click()
        except:
            pass

        time.sleep(3)
        #scraping table from page and converting to a dictionary


        table = driver.find_elements_by_xpath('//table[@class="table table-striped"]/tbody/tr')
        table = [x.text for x in table]
        spec_dict = {}
        #print(table)
        for row in table:
            try:
                feature, spec = row.split(':', 1)
            except:
                pass
            spec_dict[feature] = spec



        spec_dict["product"] = driver.find_element_by_xpath('//*[@id="product-title"]/h1/span').text
        spec_dict["core score"] = int(driver.find_element_by_xpath('//*[@id="corescore"]/span').text)
        spec_dict["reviews"] = int(re.findall('\d+', driver.find_element_by_xpath('//*[@id="rr-top-section"]/div[2]/div[1]/div[2]/div/span[2]/button').text)[0])
        spec_dict["expert_score"] = int(driver.find_element_by_xpath('//*[@id="experts_reviews_section"]/div/p').text[0:2])
        spec_dict["summary"] = driver.find_element_by_xpath('//*[@id="bottom_line_section"]/div[2]').text

        print('*'*50)
        print(spec_dict)
        print('*'*50)

        # Unpack spec_dict into item fields
        #item['terrain'] = spec_dict.get('Terrain')
        #item['updated_prod'] = spec_dict.get('Update', 'No product')

        time.sleep(1)


#    #page_num = 1

#while True:
    #print(f'Scraping page {page_num}')
    #products = driver.find_elements_by_xpath('.//div[@class="product-name hidden-sm hidden-xs"]/a/@href')
