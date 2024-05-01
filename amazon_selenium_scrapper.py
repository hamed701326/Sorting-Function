from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


options = Options()
# options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--disable-gpu')  # Disable GPU acceleration (needed for headless mode)

def scrap():
    # Configuration for headless browser
    options = Options()
    options.headless = True
    
    # URL of the Amazon product reviews page
    base_url = 'https://www.amazon.com/Amazon-Essentials-Snap-Front-Pullover-Fleece/product-reviews/B0D1YJLHHV/ref=cm_cr_arp_d_paging_btm_prev_1?ie=UTF8&pageNumber='
    
    # Product title and category (you can adjust these based on your specific needs)
    product_title = 'Amazon Essentials Men\'s Full-Zip Polar Fleece Jacket'
    product_category = 'Clothing'
    
    # CSV file to store the extracted data
    csv_file_path = 'amazon_reviews.csv'
    
    # Initialize CSV writer
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Ranking', 'Product Title', 'Product Category', 'Rating', 'Review Date', 'Helpful Votes', 'Has Image', 'Verified Purchase', 'Review Title', 'Review Text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        
        # Initialize WebDriver
        svc = Service(executable_path=binary_path)
        driver = webdriver.Chrome(service=svc, options=options)
        
        try:
            # Loop through pages from 1 to 10
            for page_number in range(1, 11):
                url = f'{base_url}{page_number}&reviewerType=all_reviews'
                driver.get(url)
                time.sleep(5)  # Wait for the page to fully load (adjust as needed)
                
                # Find all review elements on the page
                review_elements = driver.find_elements(By.XPATH, '//div[@data-hook="review"]')
                
                # Loop through each review element and extract data
                for idx, review in enumerate(review_elements, start=1):
                    # Extract ranking (review index)
                    ranking = (page_number - 1) * len(review_elements) + idx

                    # Extract rating (number of stars)
                    rating_element = review.find_element(By.XPATH, './/i[@data-hook="review-star-rating"]')
                    rating = rating_element.get_attribute('class').split(' ')[2].split('-')[-1]  # Extract the number of stars
                    
                    # Extract review text
                    review_text_element = review.find_element(By.XPATH, './/span[@data-hook="review-body"]')
                    review_text = review_text_element.text.strip()
                    
                    # Extract review title
                    try:
                        title_element = review.find_element(By.XPATH, './/a[@data-hook="review-title"]')
                        review_title = title_element.text.strip()
                    except:
                        review_title = "No title provided"
                    
                    # Extract review date
                    date_element = review.find_element(By.XPATH, './/span[@data-hook="review-date"]')
                    review_date = date_element.text.strip()
                    
                    # Extract helpful votes count
                    try:
                        helpful_element = review.find_element(By.XPATH, './/span[@data-hook="helpful-vote-statement"]')
                        helpful_votes = helpful_element.text.split()[0]
                    except:
                        helpful_votes = '0'
                    
                    # Check for presence of images in the review
                    has_image = bool(review.find_elements(By.XPATH, './/img[@class="review-image-tile"]'))
                    
                    # Check if the review is from a verified purchase
                    verified_purchase = bool(review.find_elements(By.XPATH, './/span[@data-hook="avp-badge"]'))
                    
                    # Write data to CSV
                    writer.writerow({
                        'Ranking': ranking,
                        'Product Title': product_title,
                        'Product Category': product_category,
                        'Rating': rating,
                        'Review Date': review_date,
                        'Helpful Votes': helpful_votes,
                        'Has Image': has_image,
                        'Verified Purchase': verified_purchase,
                        'Review Title': review_title,
                        'Review Text': review_text,
                    })
        
        finally:
            # Close the WebDriver session
            driver.quit()