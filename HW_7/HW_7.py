from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

options = webdriver.ChromeOptions()
options.add_argument('--headless')  
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://books.toscrape.com/"
driver.get(url)
time.sleep(2)  

html_content = driver.page_source
driver.quit()

soup = BeautifulSoup(html_content, 'html.parser')
books = soup.find_all('article', class_='product_pod')

data = []
for book in books:
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text.strip()
    availability = book.find('p', class_='instock availability').text.strip()
    data.append([title, price, availability])

csv_file = "books_data.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Availability"])
    writer.writerows(data)

print(f"Данные сохранены в {csv_file}")
