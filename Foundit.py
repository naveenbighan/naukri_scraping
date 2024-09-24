from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time
import pandas as pd

driver = webdriver.Chrome()

job_list = []

def scrape_page(page_number):
    
    url = f"https://www.foundit.in/srp/results?query=engineer&searchId=c681d960-ec7b-4ce9-96eb-8e07087990fe&start={page_number*15}"  # Adjust based on the pagination structure
    driver.get(url)
    
    time.sleep(5)
    
    html = driver.page_source
    soup = BS(html, 'html.parser')
    
    jobs = soup.find_all("div", class_="srpResultCardContainer")
    
    for job in jobs:
        job_name = job.find("div", class_="jobTitle")
        company = job.find("div", class_="companyName")
        requirments = job.find("div", class_="skillDetails")
        
        details = job.find_all("div", class_="details")
        
        if len(details) >= 3:
            timing = details[0].text.strip()  
            location = details[1].text.strip()  
            years = details[2].text.strip()
        else:
            timing = "N/A"
            location = "N/A"
            years = "N/A"
        if job_name and company:
            job_list.append({
                "Job name": job_name.text.strip(),
                "Company": company.text.strip(),
                "Timings": timing,
                "Location": location,
                "Experience": years,
                "Requirments": requirments.text.strip()
            })
      
        if job_name and company:
            print(f"Job Name: {job_name.text.strip()}, Company: {company.text.strip()}, Timing: {timing}, Location: {location}, Experience: {years}, Requirements: {requirments.text.strip() if requirments else 'N/A'}")


for page in range(670):  
    scrape_page(page)


driver.quit()

df = pd.DataFrame(job_list)

df.to_csv("Foundit_jobs.csv",index=False)