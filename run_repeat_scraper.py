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

        #driver.execute_script("window.scrollTo(0, 1700);")

        #clicking to expand table
        #more_facts_button = driver.find_element_by_class_name("div.btn btn-expand btn-default")
        #more_facts_button.click()

        #scraping table from page and converting to a dictionary
        table = driver.find_elements_by_xpath('//table[@class="table table-striped"]/tbody/tr')
        table = [x.text for x in table]
        print(table)
        spec_dict = {}
        #print(table)
        for row in table:
            try:
                feature, spec = row.split(':', 1)
            except:
                pass
            spec_dict[feature] = spec
        print('*'*50)
        print(spec_dict)
        print('*'*50)


        #product = driver.find_element_by_xpath('//*[@id="product-title"]/h1/span').text
        #brand = driver.find_element_by_xpath('//*[@id="rr_facts"]/div/div[1]/div[1]/table/tbody/tr[14]/td').text
        #price = driver.find_element_by_xpath('//*[@id="rr_facts"]/div/div[1]/div[1]/table/tbody/tr[16]/td/span/span/span').text
        #sale_price = driver.find_element_by_xpath('//*[@id="rr_facts"]/div/div[1]/div[1]/table/tbody/tr[16]/td/span/span/button').text
        #core_score = driver.find_element_by_xpath('//*[@id="corescore"]/span').text
        #reviews = driver.find_element_by_xpath('//*[@id="rr-top-section"]/div[2]/div[1]/div[2]/div/span[2]/button').text
        #expert_score = driver.find_element_by_xpath('//*[@id="experts_reviews_section"]/div/p').text
        #summary = driver.find_element_by_xpath('//*[@id="bottom_line_section"]/div[2]').text
        #terrain = driver.find_element_by_xpath('//*[@id="rr_facts"]/div/div[1]/div[1]/table/tbody/tr[1]/td').text
        #arch_support = driver.find_element_by_xpath('//*[@id="rr_facts"]/div/div[1]/div[1]/table/tbody/tr[2]/td').text
        #mens_weight = driver.find_element_by_xpath('//*[@id="rr_facts"]/div/div[1]/div[1]/table/tbody/tr[3]/td/span/span/span[1]/span[1]').text
        #womens_weight = driver.find_element_by_xpath('//*[@id="rr_facts"]/div/div[1]/div[1]/table/tbody/tr[3]/td/span/span/span[2]/span').text
        #heel_to_toe_men =
        #heel_to_toe_women =
        #fit =
        #pronation =
        #arch_type =
        #use =
        #material =
        #features =
        #release_date =
        #width =
        #print(product)
        #print(terrain)
        #print(brand)
        #print(price)
        #print(sale_price)
        #print(core_score)
        #print(reviews)
        #print(expert_score)


        # Unpack spec_dict into item fields
        #item['terrain'] = spec_dict.get('Terrain')
        #item['updated_prod'] = spec_dict.get('Update', 'No product')

        time.sleep(1)


#    #page_num = 1

#while True:
    #print(f'Scraping page {page_num}')
    #products = driver.find_elements_by_xpath('.//div[@class="product-name hidden-sm hidden-xs"]/a/@href')
