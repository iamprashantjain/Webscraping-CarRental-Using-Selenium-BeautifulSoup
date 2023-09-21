from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time



# Configure Chrome options
options = Options()
options.add_argument('--ignore-certificate-errors')


driver = webdriver.Chrome(
    executable_path=r"C:\Users\iampr\Downloads\chromedriver-win64\chromedriver.exe",
    options=options
)

driver.get('https://www.budget.com/en/home')
driver.maximize_window()
time.sleep(20)


try:
    driver.find_element(By.XPATH, '/html/body/div[18]/div[3]/div/div/div/div[2]/form/div[3]/div[3]/button').click()

except:
    box = driver.find_element(By.XPATH, '/html/body/div[4]/section/div[2]/div/div/form/div/div[2]/div[6]/div[1]/div[1]/div[1]/angucomplete-alt/div/input')
    box.send_keys('Boston')
    time.sleep(5)
    box.send_keys(Keys.DOWN)
    time.sleep(2)
    box.send_keys(Keys.ENTER)

    dte = driver.find_element(By.XPATH, '/html/body/div[4]/section/div[2]/div/div/form/div/div[2]/div[6]/div[1]/div[1]/div[2]/input')
    dte.clear()
    time.sleep(2)
    dte.send_keys('10/10/2023')
    time.sleep(5)


    return_dte = driver.find_element(By.XPATH, '/html/body/div[4]/section/div[2]/div/div/form/div/div[2]/div[6]/div[1]/div[4]/div[1]/div[2]/input')
    return_dte.clear()
    time.sleep(2)
    return_dte.send_keys('10/15/2023')
    time.sleep(5)

    #click on select my car
    driver.find_element(By.XPATH, '/html/body/div[4]/section/div[2]/div/div/form/div/div[2]/div[6]/div[2]/div/button').click()
    time.sleep(5)

    try:
        #discount_nothanks
        driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[1]/div/div/div[2]/section[1]/div[2]/div[3]/div/div/div/div[2]/form/div[2]/div[2]').click()
        time.sleep(2)
    except:
        pass

    # html = driver.page_source
    
    # with open('budget_bos1.html','w',encoding='utf-8') as f:
    #     f.write(html)

    
    #scraping_data
    soup = BeautifulSoup(driver.page_source, 'lxml')

    car_info = []

    car_boxes = soup.find_all('div', class_='row avilablecar available-car-box')
    
    for car_box in car_boxes:
        car_type = car_box.find('h3', {'ng-bind': 'car.carGroup'}).text.strip()
        car_description = car_box.find('p', class_='featurecartxt similar-car').text.strip()
        seats_large_small = car_box.find_all('span', class_='c-icon seat-icon')
        large_bags = car_box.find('span', class_='c-icon bag-large')
        small_bags = car_box.find('span', class_='c-icon bag-small')
        pay_later_rate = car_box.find('p', class_='payamntp').text.strip()
        pay_now_rate = car_box.find('p', class_='payamntr').text.strip()
        bluetooth = car_box.find('span', class_='c-icon bluetooth-icon')
        backup_camera = car_box.find('span', class_='c-icon backupcamera-icon')
        automatic_transmission = car_box.find('p', text='Automatic Transmission')

        car_info.append({
            'Car Type': car_type,
            'Description': car_description,
            'Seats': len(seats_large_small) if seats_large_small else 'N/A',
            'Large Bags': large_bags.text.strip() if large_bags else 'N/A',
            'Small Bags': small_bags.text.strip() if small_bags else 'N/A',
            'Pay Later Rate': pay_later_rate,
            'Pay Now Rate': pay_now_rate,
            'Bluetooth': 'Yes' if bluetooth else 'No',
            'Backup Camera': 'Yes' if backup_camera else 'No',
            'Automatic Transmission': 'Yes' if automatic_transmission else 'No'
        })


    for car in car_info:
        print(car)


df = pd.DataFrame(car_info)
print(df)

df.to_csv("budget_bos.csv")


#sample Output
# {'Car Type': 'Minivan', 'Description': 'Chrysler Pacifica or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': '', 'Pay Later Rate': '$923.99', 'Pay Now Rate': '$831.59', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'}   
# {'Car Type': 'Intermediate SUV', 'Description': 'Toyota Rav4 or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': '', 'Pay Later Rate': '$489.99', 'Pay Now Rate': '$440.99', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'}
# {'Car Type': 'Economy', 'Description': 'Ford Fiesta or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': '', 'Pay Later Rate': '$490.99', 'Pay Now Rate': '$441.89', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'}
# {'Car Type': 'Compact', 'Description': 'Kia Soul or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': '', 'Pay Later Rate': '$493.99', 'Pay Now Rate': '$444.59', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'}
# {'Car Type': 'Intermediate Electric', 'Description': 'Chevrolet Bolt or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': '', 'Pay Later Rate': '$496.99', 'Pay Now Rate': '$422.44', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'}
# {'Car Type': 'Standard SUV', 'Description': 'Ford Edge or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': '', 'Pay Later Rate': '$503.99', 'Pay Now Rate': '$453.59', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'}      
# {'Car Type': 'Standard', 'Description': 'Volkswagen Jetta or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': '', 'Pay Later Rate': '$513.99', 'Pay Now Rate': '$462.59', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'}   
# {'Car Type': 'Full-Size', 'Description': 'Toyota Camry or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': '', 'Pay Later Rate': '$513.99', 'Pay Now Rate': '$462.59', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'}      
# {'Car Type': 'Full-Size Hybrid', 'Description': 'Toyota Prius Hybrid or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': '', 'Pay Later Rate': '$523.99', 'Pay Now Rate': '$419.19', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'}
# {'Car Type': 'Intermediate', 'Description': 'Toyota Corolla or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': '', 'Pay Later Rate': '$538.99', 'Pay Now Rate': '$478.99', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'} 
# {'Car Type': 'Full-Size Pickup Truck', 'Description': 'RAM 1500 or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': 'N/A', 'Pay Later Rate': '$558.99', 'Pay Now Rate': '$447.19', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'}
# {'Car Type': 'Standard Recreational Vehicle', 'Description': 'Jeep Wrangler 4-Door or similar', 'Seats': 2, 'Large Bags': 'N/A', 'Small Bags': '', 'Pay Later Rate': '$594.99', 'Pay Now Rate': '$475.99', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'}
# {'Car Type': 'Standard Sport', 'Description': 'Dodge Challenger or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': '', 'Pay Later Rate': '$649.99', 'Pay Now Rate': '$519.99', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'}
# {'Car Type': 'Full Size SUV', 'Description': 'Kia EV6 or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': '', 'Pay Later Rate': '$1,190.99', 'Pay Now Rate': '$1,071.89', 'Bluetooth': 'No', 'Backup Camera': 'No', 'Automatic Transmission': 'Yes'}     
# {'Car Type': 'Premium Elite SUV', 'Description': 'Jeep Grand Wagoneer or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': '', 'Pay Later Rate': '$1,240.99', 'Pay Now Rate': '$992.79', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'}
# {'Car Type': 'Premium SUV', 'Description': 'Chevrolet Suburban or similar', 'Seats': 2, 'Large Bags': '', 'Small Bags': '', 'Pay Later Rate': '$1,378.99', 'Pay Now Rate': '$1,241.09', 'Bluetooth': 'Yes', 'Backup Camera': 'Yes', 'Automatic Transmission': 'Yes'}