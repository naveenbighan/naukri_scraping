from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time
import pandas as pd

# Initialize the Chrome driver
driver = webdriver.Chrome()

job_list = []

# Function to extract jobs from a given page number
def scrape_page(page_number):
    # Construct the URL with the page number
    url = f"https://www.foundit.in/srp/results?query=engineer&searchId=c681d960-ec7b-4ce9-96eb-8e07087990fe&start={page_number*15}"  # Adjust based on the pagination structure
    driver.get(url)
    
    # Give the page time to load
    time.sleep(5)
    
    # Parse the page content
    html = driver.page_source
    soup = BS(html, 'html.parser')
    
    # Find all job cards
    jobs = soup.find_all("div", class_="srpResultCardContainer")
    
    # Loop through each job and extract information
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
        # Print the extracted information
        if job_name and company:
            print(f"Job Name: {job_name.text.strip()}, Company: {company.text.strip()}, Timing: {timing}, Location: {location}, Experience: {years}, Requirements: {requirments.text.strip() if requirments else 'N/A'}")

# Loop through multiple pages (e.g., first 5 pages)
for page in range(670):  # Adjust the range as needed (e.g., range(5) for 5 pages)
    scrape_page(page)

# Close the driver after extraction
driver.quit()

df = pd.DataFrame(job_list)

df.to_csv("Foundit_jobs.csv",index=False)