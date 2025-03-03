from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time
import random
import re
import undetected_chromedriver as uc

# Define a pool of User-Agent strings for rotation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
]

# Randomly pick a User-Agent from the pool
random_user_agent = random.choice(user_agents)

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument(f"user-agent={random_user_agent}")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Use undetected-chromedriver to bypass detection
driver = uc.Chrome(options=chrome_options)

# Define the Indeed job search URL
url = "https://ma.indeed.com/q-mobile-jobs.html"

# Open the page
driver.get(url)
time.sleep(random.uniform(3, 5))  # Add random delay

# Function to check if CAPTCHA is present
# def is_captcha_present():
#     try:
#         # Look for CAPTCHA specific elements (update as per your page structure)
#         captcha_element = driver.find_element(By.XPATH, '//div[@class="g-recaptcha"]')  # Update with the correct CAPTCHA element's XPath
#         return True
#     except:
#         return False

# # Function to bypass CAPTCHA
# def bypass_captcha():
#     print("CAPTCHA detected. Attempting to bypass or refresh.")
#     # Refresh the page or try another workaround
#     driver.refresh()  # Reload the page to potentially bypass CAPTCHA
#     time.sleep(random.uniform(5, 7))  # Wait for CAPTCHA to possibly disappear
#     return

# def scroll_to_load():
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         # Scroll down to the bottom
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(random.uniform(3, 5))  # Add random delay to mimic human behavior

#         # Calculate new scroll height and compare it with last height
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:  # No more jobs to load
#             break
#         last_height = new_height


# Initialize CSV file
with open('indeed_jobs.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Job Title', 'Company', 'Link', 'Description'])

    # Pagination loop
    while True:
        try:
            # Wait for the job listings to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1faftfv li "))#.job_seen_beacon
            )
            
            # Parse job listings
            # page_source = driver.page_source
            # soup = BeautifulSoup(page_source, 'html.parser')

            job_listings = driver.find_elements(By.CSS_SELECTOR, ".css-1faftfv li ")
            print(f"Found {len(job_listings)} job listings.")

            # scroll_to_load()
            
            for job in job_listings:
                try:
                    job.click()
                    time.sleep(random.uniform(2, 4))  # Wait for job details to load with random delay
                    
                    # if is_captcha_present():
                    #     bypass_captcha()  # Handle CAPTCHA by refreshing the page
                    #     continue  # Skip to the next job listing if CAPTCHA is detected

                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, 'html.parser')
                    
                    job_title = soup.find('h2', class_='jobsearch-JobInfoHeader-title').text.strip()
                    # job_title = soup.find('h2', class_='jobsearch-JobInfoHeader-title')
                    # title_text = job_title.text.strip() if job_title else 'Not Available'
                    print(job_title)

                    company = soup.find('a', class_='css-1ioi40n').text.strip() if soup.find('a', class_='css-1ioi40n') else 'Not Available'
                    description = soup.find('div', id='jobDescriptionText').text.strip() if soup.find('div', id='jobDescriptionText') else 'No description available'
                    description = re.sub(r'[^\w]', ' ', description)
                    link = driver.current_url
                    
                    

                    # Write to CSV
                    writer.writerow([job_title, company, link, description])
                    print(f"Saved job: {job_title}")

                except Exception as e:
                    print(f"Error processing job listing: {e}")
                    continue

            # Check if there is a next page
            next_button = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]')
            if next_button:
                next_button.click()
                time.sleep(random.uniform(3, 5))  # Random delay for page load
            else:
                print("No more pages to navigate.")
                break

        except Exception as e:
            print(f"Error during pagination or page load: {e}")
            break

# Close the browser after scraping
driver.quit()
