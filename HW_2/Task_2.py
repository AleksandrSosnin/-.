import requests
from bs4 import BeautifulSoup
import json

def get_html(url):
    response = requests.get(url)
    return response.text

def parse_book_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    book_data = {}
    
    # Извлечение названия книги
    book_data['title'] = soup.find('div', class_='product_main').h1.text
    
    # Извлечение цены книги
    price = soup.find('p', class_='price_color').text
    # Удаляем символы '£' и 'Â' и преобразуем в число
    price = price.replace('£', '').replace('Â', '').strip()
    book_data['price'] = float(price)
    
    # Извлечение количества товара в наличии
    stock = soup.find('p', class_='instock availability').text.strip()
    stock = stock.replace('In stock (', '').replace(' available)', '')
    book_data['stock'] = int(stock)
    
    # Извлечение описания книги
    description = soup.find('div', id='product_description')
    if description:
        book_data['description'] = description.find_next_sibling('p').text.strip()
    else:
        book_data['description'] = ''
    
    return book_data

def get_all_books():
    base_url = "http://books.toscrape.com/"
    categories_url = base_url + "index.html"
    
    # Получаем список всех категорий
    categories_html = get_html(categories_url)
    categories_soup = BeautifulSoup(categories_html, 'html.parser')
    categories = categories_soup.find('ul', class_='nav nav-list').find_all('a')
    
    all_books = []
    
    for category in categories[1:]:  # Пропускаем первую категорию "Books"
        category_name = category.text.strip()
        category_url = base_url + category['href']
        
        # Проходим по всем страницам категории
        while True:
            category_html = get_html(category_url)
            category_soup = BeautifulSoup(category_html, 'html.parser')
            
            # Извлекаем ссылки на книги
            books = category_soup.find_all('h3')
            for book in books:
                book_url = base_url + 'catalogue/' + book.a['href'].replace('../../../', '')
                book_html = get_html(book_url)
                book_data = parse_book_page(book_html)
                all_books.append(book_data)
            
            # Проверяем, есть ли следующая страница
            next_button = category_soup.find('li', class_='next')
            if next_button:
                next_page_url = next_button.a['href']
                category_url = base_url + 'catalogue/' + next_page_url
            else:
                break
    
    return all_books

def save_to_json(data, filename='books.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

all_books = get_all_books()
save_to_json(all_books)