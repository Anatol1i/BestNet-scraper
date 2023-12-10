pip install selenium
import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.service import Service
from itertools import cycle
from webdriver_manager.chrome import ChromeDriverManager
pd.set_option('display.max_colwidth', None)



chromedriver_path = 'path to driver'

def get_proxies():
    
    return ['http:// proxy...']


def scrape_mail_with_selenium(url, proxy, driver_path):
    try:
        chrome_options = Options()
        chrome_options.add_argument(f'--proxy-server={proxy}')
        
       
        service = Service(executable_path=driver_path)
        
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        
        driver.get(url)
        time.sleep(5)
        
        
        email_element = driver.find_element(By.CSS_SELECTOR, "a[href^='mailto']")
        email = email_element.text 
        
        driver.quit()
        
        return email
    except Exception as e:
        print(f"Error accessing {url} with proxy {proxy}: {e}")
        driver.quit()  
        return None


df = pd.read_csv('file name ')  


df['E-mail'] = pd.NaT


proxies = get_proxies()
proxy_pool = cycle(proxies)


proxy_use_count = {proxy: 0 for proxy in proxies}



row_counter = 0
for index, row in df.iterrows():
   


    if pd.isna(row['E-mail_link']): 
        row_counter += 1
        continue
    time.sleep(5)
    
    proxy = next(proxy_pool)
    
    
    mail = scrape_mail_with_selenium(row['E-mail_link'], proxy, chromedriver_path)
    
    
    df.at[index, 'E-mail'] = mail

    
    proxy_use_count[proxy] += 1
    if proxy_use_count[proxy] >= 10:
        proxy_use_count[proxy] = 0  
        proxy = next(proxy_pool)
        proxy_use_count[proxy] += 1


df.to_csv('new file name', index=False)
print(df)