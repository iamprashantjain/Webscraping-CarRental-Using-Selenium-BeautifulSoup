from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import pdb


driver_path = r"C:\Users\jainprs\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://uhaul.com')
driver.maximize_window()
time.sleep(20)


pickup_location = driver.find_element(By.ID, "PickupLocation-TruckOnly")
pickup_location.send_keys("Boston, MA")
time.sleep(3)
pickup_location.send_keys(Keys.ENTER)
time.sleep(5)

dropoff_location = driver.find_element(By.ID, "DropoffLocation-TruckOnly")
dropoff_location.send_keys("Boston, MA")
time.sleep(3)
dropoff_location.send_keys(Keys.ENTER)
time.sleep(5)



pickup_date = driver.find_element(By.ID,"PickupDate-TruckOnly")
pickup_date.send_keys("10/15/2023")
time.sleep(3)
pickup_date.send_keys(Keys.ENTER)
time.sleep(5)


get_rates = driver.find_element(By.XPATH,"/html/body/main/div/div/div/div[1]/div[2]/div/div[2]/div/div/div/div[1]/form/div[3]/div[2]/button")
get_rates.click() 
time.sleep(5)


soup = BeautifulSoup(driver.page_source, 'lxml')
box = soup.find_all("li", class_="divider")

data_list = []

for i in box:
    truck_name = i.find('h3', class_='text-2x').text.strip()
    moving_type = i.find('dd', class_='text-bold text-xl').text.strip()
    dimension = i.find('ul', class_ = 'disc hide-for-small-only').text.strip()
    rate = i.find('b', class_='block text-3x medium-text-2x text-callout medium-text-base').text.strip()
    
    div_element = soup.find('div', text=lambda text: text and 'mile' in text)
    mileage_rate = div_element.get_text(strip=True) if div_element else None
    
    img_element = i.find('img')
    image_url = img_element['src'] if img_element else None


    truck_data = {
        'Truck Name': truck_name,
        'Moving Type': moving_type,
        'Dimension':dimension,
        'Rate': rate,
        'Mileage Rate': mileage_rate,
        'Image URL': image_url
    }

    data_list.append(truck_data)

df = pd.DataFrame(data_list)
print(df)

pdb.set_trace()




while True:
    pass
