from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Setup Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URLs of the pages to scrape
urls = [
    ("https://www.ifood.com.br/delivery/sao-paulo-sp/coco-bambu---analia-franco-vila-gomes-cardim/4cdd2e7d-36b6-47e3-b435-428a77a7d967", "Coco Bambu"),
    ("https://www.ifood.com.br/delivery/sao-paulo-sp/republica-dos-camaroes-chacara-california/8c7e9b76-7963-4258-8f7d-4727a241543d", "República dos Camarões")
]

# List to store all dishes
all_dishes = []

# Function to extract dishes from a given URL
def extract_dishes(url, source):
    driver.get(url)
    time.sleep(10)
    dish_elements = driver.find_elements(By.CSS_SELECTOR, 'div.dish-card__info.dish-card__info--horizontal')
    dishes = []
    for element in dish_elements:
        name = element.find_element(By.CSS_SELECTOR, 'h3.dish-card__description').text
        price = element.find_element(By.CSS_SELECTOR, 'span.dish-card__price[data-test-id="dish-card-price"]').text
        details = element.find_element(By.CSS_SELECTOR, 'span.dish-card__details').text
        
        if 'camarão' in name.lower():
            price_cleaned = price.replace('R$', '').strip()
            if 'A partir de' in price_cleaned:
                price_cleaned = price_cleaned.replace('A partir de', '').strip()
            try:
                price_float = float(price_cleaned.replace(',', '.'))
                dishes.append((name, details, price_float, source))
            except ValueError:
                continue
    return dishes

# Loop through each URL and extract dishes
for url, source in urls:
    dishes_from_url = extract_dishes(url, source)
    all_dishes.extend(dishes_from_url)

# Close the WebDriver
driver.quit()

# Sort dishes by price
all_dishes.sort(key=lambda dish: dish[2])

# Print the filtered and sorted dishes
for dish in all_dishes:
    print(f"Name: {dish[0]}\nDetails: {dish[1]}\nPrice: R$ {dish[2]:.2f}\nSource: {dish[3]}\n")

# Define the CSV file name
csv_file_name = 'camarao_dishes_with_color.csv'

# Write the data to a CSV file
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Details', 'Price', 'Source'])  # Writing the header
    writer.writerows(all_dishes)

print(f"Data has been written to {csv_file_name}")
