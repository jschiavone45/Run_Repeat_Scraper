from selenium import webdriver
import time
import re
import csv
import math


#set up to write to csv_file
csv_file = open('running_shoes.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['product', 'brand', 'core_score', 'expert_score', 'reviews', 'retail_price', 'sale_price',
                    'terrain', 'arch_support', 'weight_men', 'weight_women', 'heel_to_toe_men', 'heel_to_toe_women', 'release_date', 'width', 'update', 'url', 'summary'])

driver = webdriver.Chrome()
driver.get("https://runrepeat.com/ranking/rankings-of-running-shoes?page=1")


# creating list of product pagesgi

num_products = driver.find_element_by_xpath('//*[@id="rankings-header"]/h1').text
num_products = int(re.findall('\d+', num_products)[0])
total_pages = math.ceil(num_products / 30)
url_list = [f'https://runrepeat.com/ranking/rankings-of-running-shoes?page={i + 1}' for i in range(total_pages)]


product_links = driver.find_elements_by_xpath('//div[@class="product-name hidden-sm hidden-xs"]/a')
product_links = [x.get_attribute('href') for x in product_links]



page_num = 1

#begin cycle through each url
for url in url_list:
    print(f'Scraping page {page_num}')
    # create list of product links to click for current page
    driver.get(url)
    product_links = driver.find_elements_by_xpath('//div[@class="product-name hidden-sm hidden-xs"]/a')
    product_links = [x.get_attribute('href') for x in product_links]

    #cycle through each product_page and scrape fields
    for link in product_links:
        driver.get(link)

        driver.execute_script("window.scrollTo(0, 1900);")
        time.sleep(3)
        #clicking to expand table
        try:
            more_facts_button = driver.find_element_by_xpath('//div[@class="btn-more-container"]')
            more_facts_button.click()
        except Exception as e:
            print(type(e), e)
            print(f'Button not found on {link}')

        time.sleep(2)


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
            # checking to see what data is missing
        if 'Update' not in spec_dict:
            spec_dict['Update'] = 'NaN'
        if 'Release date' not in spec_dict:
            spec_dict['Release date'] = 'NaN'
        if 'Brand' not in spec_dict:
            spec_dict['Brand'] = 'NaN'
        if 'Width' not in spec_dict:
            spec_dict['Width'] = 'NaN'
        if 'Arch support' not in spec_dict:
            spec_dict['Arch support'] = 'NaN'
        if 'Terrain' not in spec_dict:
            spec_dict['Terrain'] = 'NaN'
        if 'Price' not in spec_dict:
            retail_price = 'NaN'
            sale_price = 'NaN'
        try:
            product = driver.find_element_by_xpath('//*[@id="product-title"]/h1/span').text
        except:
            product = "NaN"
        try:
            core_score = int(driver.find_element_by_xpath('//*[@id="corescore"]/span').text)
        except:
            core_score = 'NaN'
        try:
            reviews = int(re.findall('\d+', driver.find_element_by_xpath('//*[@id="rr-top-section"]/div[2]/div[1]/div[2]/div/span[2]/button').text)[0])
        except:
            reviews = 'NaN'
        try:
            expert_score = int(driver.find_element_by_xpath('//*[@id="experts_reviews_section"]/div/p').text[0:2])
        except:
            expert_score = 'NaN'
        try:
            summary = driver.find_element_by_xpath('//*[@id="bottom_line_section"]/div[2]').text
        except:
            summary = 'NaN'

        try:
            price_list = spec_dict['Price'].strip().split(' ', 1)
            retail_price, sale_price = price_list
        except:
            try:
                retail_price = spec_dict['Price']
                sale_price = 'NaN'
            except:
                retail_price = 'NaN'
                sale_price = 'NaN'
        try:
            weight_men, weight_women = spec_dict['Weight'].split('|')
        except:
            weight_men, weight_women = 'NaN', 'NaN'
        try:
            heel_to_toe_men, heel_to_toe_women = spec_dict['Heel to toe drop'].split('|')
        except:
            heel_to_toe_men, heel_to_toe_women = 'NaN', 'NaN'


        # writing next row of csv file with current product_page
        write_row = [product, spec_dict['Brand'], core_score, expert_score, reviews, retail_price, sale_price, spec_dict['Terrain'],
                    spec_dict['Arch support'], weight_men, weight_women, heel_to_toe_men, heel_to_toe_women, spec_dict['Release date'], spec_dict['Width'], spec_dict['Update'], link, summary]
        csv_writer.writerow(write_row)


    page_num +=1
