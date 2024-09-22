from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the webdriver
driver = webdriver.Chrome()

# Navigate to the URL
driver.get("https://www.shine.com/job-search/data-entry-jobs-?q=data-entry")

# Wait until the job cards are loaded
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "jobCard_jobCard__jjUmu")))

# Get page source and parse it with BeautifulSoup
html = driver.page_source
soup = BS(html, "html.parser")

# Find all job cards
job_cards = soup.find_all("div", class_="jobCard_jobCard__jjUmu")

# Iterate through each job card and print the title
for job in job_cards:
    title = job.find("a")
    if title:
        print(title.text.strip())  # Use .strip() to remove leading/trailing whitespace

# Cleanup - Close the driver
driver.quit()
