pip install selenium 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import urllib.parse
import re



driver = webdriver.Chrome('path to driver')  

url = 'url of starting page'
start_number = 16
finish_number = 430


all_persons = []


driver.get(url)

try:
    
    while start_number <= finish_number:
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2"))
        )
        
        
        buttons = driver.find_elements(By.XPATH, "//a[.//span[@style='font-weight:bold;']]")
        
        
        for button in buttons:
            
            button.click()
            
            
            time.sleep(5)
            
            
            person_details = {'Name': 'NaN', 'Title': 'NaN','Adresse':'NaN','Telefonnummer':'NaN','Website':'NaN','E-mail_link':'NaN'}
            
            try:
                name_element = driver.find_element(By.XPATH, "//div[@class='subtitle2']/h2")
                
                person_details['Name'] = name_element.text.replace('Detail-Infos zu ', '')
            except NoSuchElementException:
                
                pass
            
            
            try:
                title_element = driver.find_element(By.XPATH, "//li[text()]")
                
                person_details['Title'] = title_element.text
            except NoSuchElementException:
                
                pass
    
            try:
                
                address_element = driver.find_element(By.XPATH, "//div[@style='float:left;padding:1px;']")
                
                address_full_text = address_element.text
                address_text = address_full_text.split('\n')[0] if '\n' in address_full_text else address_full_text
                person_details['Adresse'] = address_text
            except NoSuchElementException:
                pass
    
            try:
                phone_element = driver.find_element(By.XPATH, "//a[contains(@href, 'tel:')]")
                phone_number = phone_element.get_attribute('href').replace('tel:', '')
                person_details['Telefonnummer'] = phone_number
            except NoSuchElementException:
                pass
    
    
    
            try:
                website_element = driver.find_element(By.XPATH, "//a[contains(@href, '/link.asp?link=')]")
                
                website_url = website_element.get_attribute('href')
                
                decoded_url = urllib.parse.unquote(website_url.split('=')[1])
                person_details['Website'] = decoded_url
            except NoSuchElementException:
                
                try:
                    alternative_website_element = driver.find_element(By.XPATH, "//u")
                    
                    alternative_website_url = alternative_website_element.text
                    person_details['Website'] = alternative_website_url
                except NoSuchElementException:
                    
                    pass
        
        
            try:
                email_element = driver.find_element(By.XPATH, "//a[contains(@onclick, 'emailcontactform')]")
                
                email_link_partial = email_element.get_attribute('href')
                
                email_link = urllib.parse.urljoin(url, email_link_partial)
                person_details['E-mail_link'] = email_link
            except NoSuchElementException:
                
                pass
    

        

            
            all_persons.append(person_details)
            
            
            driver.back()
            
        
        button_text = f"{start_number} - {start_number + 14}"
        
        
        button_xpath = f"//a[contains(@class, 'button is-primary') and .//span[contains(text(), '{button_text}')]]"
        
        
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        
        
        button.click()
        
        
        start_number += 15

        
        if start_number > finish_number:
            print("Reached the last button.")
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    
    df = pd.DataFrame(all_persons)
    df = df.astype(str)
    
    driver.quit()

    
    print(df)
    df.to_csv('name of a file', index=False)