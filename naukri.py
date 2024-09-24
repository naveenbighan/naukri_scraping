from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()

data_list = []

for i in range(1000):
    url = f"https://www.naukri.com/software-developer-jobs-{i}?k=software+developer&nignbevent_src=jobsearchDeskGNB"
    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "row1")))
        html = driver.page_source
        soup = BS(html, "html.parser")
        
        titles = soup.find_all("div", class_="row1")
        company_names = soup.find_all("span", class_="comp-dtls-wrap")
        experiences = soup.find_all("span", class_="exp-wrap")
        locations = soup.find_all("span", class_="ni-job-tuple-icon ni-job-tuple-icon-srp-location loc")
        salaries = soup.find_all("span", class_="ni-job-tuple-icon ni-job-tuple-icon-srp-rupee sal")
        descriptions = soup.find_all("div", class_="row4")
        
        
        for title, company_name, experience, location, salary, description in zip(titles, company_names, experiences, locations, salaries, descriptions):
            name = title.text.strip() if title else "N/A"
            company_name = company_name.text.strip()
            
           
            if "Reviews" in company_name:
                cleaned_company_name = company_name.split("Reviews")[0].strip()
                cleaned_company_name = ''.join([char for char in cleaned_company_name if not char.isdigit() and char != '.']).strip()
            else:
                cleaned_company_name = company_name
            
            experience = experience.text.strip() if experience else "N/A"
            location = location.text.strip() if location else "N/A"
            salary = salary.text.strip() if salary else "N/A"
            
            
            description_text = description.find("span", class_="job-desc").get_text(separator=" ").strip('.') if description.find("span", class_="job-desc") else "N/A"
            
            
            print(f"name: {name}, company-name: {cleaned_company_name}, experience: {experience}, location: {location}, salary: {salary}, description: {description_text}")

            
            naukri_data = {
                "Name": name,
                "Company-Name": cleaned_company_name,
                "Experience": experience,
                "Location": location,
                "Salary": salary,
                "Requirement": description_text
            }
            data_list.append(naukri_data)
            
    except Exception as e:
        print(f"An error occurred: {e}")

df = pd.DataFrame(data_list)
df.to_csv("naukri1_com.csv", index=False, encoding='utf-8-sig')

driver.quit()
