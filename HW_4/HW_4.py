import requests
from lxml import html
import csv

url = 'https://www.x-rates.com/table/?from=USD&amount=1' # Был взят Сайт с курсами валют

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"❌ Ошибка при выполнении запроса: {e}")
    exit()

tree = html.fromstring(response.content)

try:
    table = tree.xpath('//table[contains(@class, "tablesorter")]')[0]
except IndexError:
    print("❌ Таблица не найдена на странице.")
    exit()

headers = [header.strip() for header in table.xpath('.//thead//th/text()')]

rows = table.xpath('.//tbody/tr')
data_rows = []

for row in rows:
    cells = [" ".join(cell.xpath('.//text()')).strip() for cell in row.xpath('.//td')]
    if len(cells) == len(headers):
        data_rows.append(cells)
    else:
        print(f"⚠️ Пропущена строка из-за несоответствия формата: {cells}")

output_file = 'currency_exchange_rates.csv'

try:
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data_rows)
    print(f"✅ Данные успешно сохранены в файл: {output_file}")
except IOError as e:
    print(f"❌ Ошибка при записи в CSV-файл: {e}")
