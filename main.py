from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os


country = "united-states" # Change this to your country
time_wait = 1 #configure if you have a slow internet connection

pages = ["overview", "gdp", "labour", "prices", "health", "money", "trade", "government", "business", "consumer", "housing"]

url = "https://tradingeconomics.com/" + country + "/indicators"

driver = webdriver.Chrome()
driver.get(url)

menu = driver.find_element(By.ID, "pagemenutabs")
links = menu.find_elements(By.TAG_NAME, "a")

data_pages = {}

for i in  range(len(pages)):
    try:
        page = pages[i]
        data_pages[page] = []
        links[i].click()
        driver.implicitly_wait(time_wait)
        element = driver.find_element(By.ID, page)
        lines = element.find_elements(By.TAG_NAME, "tr")
        
        for line in lines:
            try:
                variable = line.find_element(By.TAG_NAME, "a").text
                data = line.find_elements(By.TAG_NAME, "td")
                value = data[1].text
                measurement = data[3].text
                month_year = data[4].text
                
                month_year = month_year.split("/")
                month = month_year[0]
                year = month_year[1]
                data_pages[page].append([variable, value, measurement, month, year])                       
            except:

                print("x - " + page)
    except Exception as err:
        print(err)
        print("Page not found: " + page)
driver.close()


for page in pages:
    try:
        if not os.path.exists(country):
            os.makedirs(country)

        filename = country + "/" + page + ".csv"
        #create file if it doesn't exist
        try:
            file = open(filename, "w")
            file.write("")
            file.close()       
        except Exception as err:
            print(err) 
            break

        with open(filename, "a") as file:
            for line_data in data_pages[page]:
                variable = line_data[0]
                value = line_data[1]
                measurement = line_data[2]
                month = line_data[3]
                year = line_data[4]
                file.write(variable + "," + value + "," + measurement + "," + month + "," + year + "\n")
    except Exception as err:
        print(err)
        print("Page not found: " + page)

    
    