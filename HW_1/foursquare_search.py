import requests
import os
from dotenv import load_dotenv

# Загружаем API-ключ из .env (если используешь .env)
load_dotenv()
FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY", "fsq3EAVXJ0jBd53zV/fwdP1u0LmMgD6G0TZ4MLIT64aBTVo=")

# Базовый URL Foursquare API
BASE_URL = "https://api.foursquare.com/v3/places/search"

# Функция для поиска заведений
def search_places(query, location="Moscow, Russia", limit=5):
    headers = {
        "Accept": "application/json",
        "Authorization": FOURSQUARE_API_KEY
    }
    params = {
        "query": query,  # Поисковый запрос (например, "кофейня")
        "near": location,  # Город или место
        "limit": limit  # Количество результатов
    }
    
    response = requests.get(BASE_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")
        return []

# Основной код
if __name__ == "__main__":
    category = input("Введите категорию (например, кофейни, музеи, парки): ").strip()
    places = search_places(category)
    
    if places:
        print("\n🔎 Найденные заведения:")
        for place in places:
            name = place.get("name", "Неизвестно")
            address = place.get("location", {}).get("formatted_address", "Адрес не найден")
            rating = place.get("rating", "Нет рейтинга")
            print(f"🏠 {name}\n📍 {address}\n⭐ Рейтинг: {rating}\n")
    else:
        print("❌ Заведения не найдены. Попробуйте изменить запрос.")
