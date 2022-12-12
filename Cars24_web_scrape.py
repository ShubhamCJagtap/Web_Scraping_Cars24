"""
    Developed By : Shubham Jagtap
    linkedIn : https://www.linkedin.com/in/shubham-jagtap-scj4497/
    
    Please install Beautiful Soup and Selenium 4
    
    How to use program:
    1. Run the File
    2. Provide the city name you want to scrape from
    3. Program will automatically scrape the data and it will store it in CSV format
    
    
    Enjoy Cars24 scraping

"""
#------------------------------------ IMPORT LIBRARIES
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import time

#-------------------------------------------------------------------------------
def start_browser():
    """
    Start the Edge web browser 
    """
    options = webdriver.EdgeOptions()
    options.use_chromium = True
    options.add_argument("start-maximized")
    driver = webdriver.Edge(options=options)
    print('Browser Started...')
    return driver
#--------------------------------------------------------------------------------
def get_url():
    print('Searching cars24.com...')
    template = "https://www.cars24.com/buy-used-car?sort=P&storeCityId=2&pinId=110001"
    print(template)
    print('....')
    return template
#--------------------------------------------------------------------------------
def get_city(driver):
    soup = BeautifulSoup(driver.page_source,'html.parser')
    cities = []
    try:
        cities = (soup.find('ul',{'class':'popularCities'})).children
        print('Great Mega City present')
    except:
        print('I think your mega city is not present')
        print('trying one more time')
        try:
            cities = (soup.find('ul',{'class':'otherCities'})).children
            print('Hurray!!! City Present')
        except:
            print('Oops!! city is not present')
            print('Try any big city near you')
    return soup,cities
#--------------------------------------------------------------------------------
def click(driver):
    try:
        soup,cities = get_city(driver)
        driver.find_element(By.CSS_SELECTOR,"img[data-title='{}']".format(next(cities).get('data-title'))).click()
        print('Done')
        return
    except:
        soup,cities = get_city(driver)
        print('first pass failed!!! trying second pass')
    try:
        driver.find_element(By.XPATH,"//li[text()='{}']".format(next(cities).text)).click()
        print('Done')
        return
    except:
        soup,cities = get_city(driver)
        print('second pass failed!!! trying second pass')
    try:
        driver.find_element(By.LINK_TEXT,"{}".format(next(cities).text)).click()
        print('Done')
        return
    except:
        print('Oops..... no city is present to click')
#--------------------------------------------------------------------------------
def print_title(soup):
    title = "As per cars24 details : "+str(soup.find('div',{'class':'js-content'}).find("h1").text)
    print(title)
    print('NOTE: total cars on website can be different')
#--------------------------------------------------------------------------------
def save_file(cars):
    all_cars = []
    print("observed entries: ",len(cars))
    for i,j in enumerate(tqdm(cars,desc = "Collecing data :...")):
        try:
            title = cars[i].find('h2',{'class':'_3FpCg'}).text
            model = (" ").join(cars[i].find('p',{'class':'cvakB'}).text.split(' ')[:-1])
            gear_type = cars[i].find('p',{'class':'cvakB'}).text.split(' ')[-1]
            km = cars[i].find_all('li')[0].text
            owner = cars[i].find_all('li')[1].text
            fuel = cars[i].find_all('li')[2].text
            state_passing = cars[i].find_all('li')[3].text
            price = cars[i].find('div',{'class':'_7udZZ'}).text.replace("₹","")
            all_cars.append((title,model,gear_type,km,owner,fuel,state_passing,price))
        except:
            pass
    print("total cars collected ",len(all_cars))
    print("Saving in CSV file")
    filename='cars data-'+str(city_name)+str('.csv')
    with open(filename,'w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Car_Name','version','Gear Type','Running_kn','Owner','Fuel Type','Passing State','Price'])
        writer.writerows(all_cars)
#--------------------------------------------------------------------------------
# MAIN CODE

city_name = str(input('Please share city name: '))
driver = start_browser()
driver.get(get_url())
soup = BeautifulSoup(driver.page_source,'html.parser')
driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/header/div/div[1]/div[2]/p").click()
a = driver.find_element(By.XPATH,"/html/body/div[1]/div[6]/div/div/div/div/div[1]/div/div[2]/div/input")
try:
    driver.find_element(By.XPATH,"/html/body/div[1]/div[6]/div/div/div/div/div[1]/div/div[2]/img").click()
except:
    print('Search box is clear.....')
a.send_keys(city_name)
click(driver)
time.sleep(5)
print_title(BeautifulSoup(driver.page_source,'html.parser'))

l = 0
while(True):
    soup = BeautifulSoup(driver.page_source,'html.parser')
    cars = soup.find_all('div',{'class':'col-4'})
    if l == len(cars):
        print("reached to end")
        break
    else:
        l = len(cars)
        print('scrolling Down')
        print('current_count :'+str(len(cars))+" "+str(l))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(8)

save_file(cars)
driver.quit()
print('Browser Closed')
