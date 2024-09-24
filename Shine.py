from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time
import pandas as pd

driver = webdriver.Chrome()

job_list = []

for page in range(776):  
    try:
        url = f"https://www.shine.com/job-search/executive-sales-n-marketing-field-executive-executive-jobs-jobs-in-india-{page}?q=executive-sales-marketing-field-executive-executive-jobs&loc=india&minexp=13"
        
        driver.get(url)

        time.sleep(5)

        html = driver.page_source

        soup = BS(html, "html.parser")

        jobs = soup.find_all("strong", class_="jobCard_pReplaceH2__xWmHg")

        for job in jobs:
            try:
                job_name = job.find("a")  
                company = job.find_next("div", class_="jobCard_jobCard_cName__mYnow")  
                location = job.find_next("div", class_="jobCard_jobCard_lists_item__YxRkV jobCard_locationIcon__zrWt2")
                timing = job.find_next("div", class_="jobCard_jobCard_lists_item__YxRkV jobCard_jobIcon__3FB1t")
                relation = job.find_next("div", class_="jobCard_skillList__KKExE")

                if job_name and company and location and timing and relation:
                    job_list.append({
                        "Job name": job_name.text.strip(),
                        "Company": company.text.strip(),
                        "Location": location.text.strip(),
                        "Experience": timing.text.strip(),
                        "Skills/Relation": relation.text.strip()
                    })
                    print(f"Job Name: {job_name.text.strip()}, Company: {company.text.strip()}, Location: {location.text.strip()}, Experience: {timing.text.strip()}, Skills: {relation.text.strip()}")

            except Exception as e:
                print(f"Error parsing job: {e}")

        time.sleep(2)

    except Exception as e:
        print(f"Error processing page {page}: {e}")

df = pd.DataFrame(job_list)
df.to_csv("Shine_jobs.csv", index=False,encoding='utf-8-sig')

driver.quit()