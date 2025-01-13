import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep, time
from random import randint
from fake_useragent import UserAgent
import sys

# Set the output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Initialize ChromeOptions
option = webdriver.ChromeOptions()

# Enable incognito mode
option.add_argument("--incognito")

# Rotate User-Agent
ua = UserAgent()
option.add_argument(f"user-agent={ua.random}")

# Suppress automation warning banner
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option("useAutomationExtension", False)

# Pagination URL with placeholders
paginaton_url = 'https://in.indeed.com/jobs?q={}&l={}&radius=35&sort=date&start={}'

# Job and location parameters
job_ = 'Engineer+Fresher'
location = 'Bengaluru'

# Initialize SQLite database
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

# Create jobs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company_location TEXT,
    url TEXT,
    job_id TEXT,
    salary TEXT
)
""")

# Initialize WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
sleep(randint(2, 6))

start = time()

# Scraping loop for multiple pages
max_iter_pgs = 10
for i in range(max_iter_pgs):
    current_url = paginaton_url.format(job_, location, i * 10)
    print(f"Scraping page {i + 1}: {current_url}")
    driver.get(current_url)
    sleep(randint(10, 20))

    try:
        job_page = driver.find_element(By.ID, "mosaic-jobResults")
        jobs = job_page.find_elements(By.CLASS_NAME, "job_seen_beacon")

        for jj in jobs:
            try:
                job_title = jj.find_element(By.CLASS_NAME, "jobTitle").text
                job_url = jj.find_element(By.CLASS_NAME, "jobTitle").find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                job_id = jj.find_element(By.CLASS_NAME, "jobTitle").find_element(By.CSS_SELECTOR, "a").get_attribute("id")
                company_location = jj.find_element(By.CLASS_NAME, "company_location").text

                # Handle salary information
                try:
                    salary = jj.find_element(By.CLASS_NAME, "salary-snippet-container").text
                except NoSuchElementException:
                    try:
                        salary = jj.find_element(By.CLASS_NAME, "estimated-salary").text
                    except NoSuchElementException:
                        salary = None

                # Insert into database
                cursor.execute("""
                INSERT INTO jobs (title, company_location, url, job_id, salary)
                VALUES (?, ?, ?, ?, ?)
                """, (job_title, company_location, job_url, job_id, salary))
                conn.commit()

            except NoSuchElementException:
                pass

    except NoSuchElementException:
        print(f"No job results found on page {i + 1}.")

driver.quit()
end = time()

print(f"{end - start} seconds to complete query!")

# Display stored jobs
print("Stored jobs in database:")
for row in cursor.execute("SELECT * FROM jobs"):
    print(row)

conn.close()
