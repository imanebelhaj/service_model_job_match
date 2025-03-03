from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import csv
import time
import re

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

# Define the Indeed job search URL
url = "https://ma.indeed.com/q-morocco-emplois.html"

# Open the page
driver.get(url)
time.sleep(3)

# Define a function to scroll and load more jobs
def scroll_to_load():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # wait for new jobs to load
        
        # Calculate new scroll height and compare it with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # No more jobs to load
            break
        last_height = new_height

# Start scraping after ensuring jobs are loaded
scroll_to_load()

# Initialize CSV file
with open('indeed_jobs.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Job Title', 'Company', 'Link', 'Description'])

    # Find all job listings after the page is fully loaded
    # job_listings = driver.find_elements(By.CSS_SELECTOR, ".jobsearch-SerpJobCard")
    
    job_listings = driver.find_elements(By.CSS_SELECTOR, ".css-1faftfv li ")
    print(f"Found {len(job_listings)} job listings.")

    for job in job_listings:
        try:
            # Click on the job listing to go to the detailed page
            job.click()
            time.sleep(2)  # Wait for job details to load

            # Get the page source after clicking the job
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Extract job details
            job_title = soup.find('h2', class_='jobsearch-JobInfoHeader-title')
            title_text = job_title.text.strip() if job_title else 'Not Available'

            print(title_text)            
            company = soup.find('a', class_='css-1ioi40n').text.strip() if soup.find('a', class_='css-1ioi40n') else 'Not Available'
            description = soup.find('div', id='jobDescriptionText').text.strip() if soup.find('div', id='jobDescriptionText') else 'No description available'
            description= re.sub(r'[^\w]', ' ', description)
            link = driver.current_url

            # Write to CSV
            writer.writerow([title_text, company, link, description])
            print(f"Saved job: {title_text}")

        except Exception as e:
            print(f"An error occurred with a job listing: {e}")
            continue  # Skip the current job listing and proceed

        time.sleep(1)  # Pause between job listings to avoid being blocked

# Close the browser after scraping
driver.quit()