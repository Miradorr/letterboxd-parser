import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from datetime import datetime


def collect_user_rates(user_login: str, max_pages: int = None) -> list:
    """Собирает все оценённые фильмы пользователя."""
    base_url = f"https://letterboxd.com/{user_login}/films/diary/"
    data = []
    page_num = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    print(f"Парсинг профиля: {user_login}")

    while True:
        if page_num == 1:
            url = base_url
        else:
            url = f"{base_url}page/{page_num}/"

        print(f"Загрузка: {url}")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 404:
                print("Пользователь не найден.")
                break
            elif response.status_code != 200:
                print(f"Ошибка: {response.status_code}")
                break

            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            entries = soup.find_all('tr', class_='diary-entry-row viewing-poster-container')

            if not entries:
                print("Конец пагинации.")
                break

            for entry in entries:
                try:
                    if 'not-rated' in entry.get('class', []):
                        continue

                    td_film = entry.find('td', class_='td-film-details')
                    film_name = td_film.find('a').get_text(strip=True) if td_film else "Неизвестно"

                    td_release = entry.find('td', class_='td-released center')
                    release_date = td_release.get_text(strip=True) if td_release else "Неизвестно"

                    td_rating = entry.find('td', class_='td-rating rating-green')
                    if not td_rating:
                        continue

                    rating_span = td_rating.find('span', class_='rating')
                    if not rating_span:
                        continue

                    classes = rating_span.get('class', [])
                    if len(classes) < 2 or not classes[1].startswith('rated-'):
                        continue

                    rating = int(classes[1].split('-')[1])

                    # Добавим дату просмотра
                    date_td = entry.find('td', class_='td-day diary-day center')
                    watch_date = date_td.get_text(strip=True) if date_td else "Неизвестно"

                    data.append({
                        'film_name': film_name,
                        'release_date': release_date,
                        'rating': rating,
                        'watch_date': watch_date
                    })
                except Exception as e:
                    print(f"Ошибка записи: {e}")
                    continue

            page_num += 1
            if max_pages and page_num > max_pages:
                break
            time.sleep(1)

        except Exception as e:
            print(f"Ошибка: {e}")
            break

    print(f"Собрано: {len(data)} фильмов.")
    return data


def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Сохранено в Excel: {filename}")


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Сохранено в JSON: {filename}")


def main():
    user_login = input("Логин: ").strip()
    max_pages = input("Макс. страниц (Enter = все): ")
    max_pages = int(max_pages) if max_pages.isdigit() else None

    data = collect_user_rates(user_login, max_pages)

    if not data:
        print("Нет данных.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_to_excel(data, f"{user_login}_rates_{timestamp}.xlsx")
    save_to_json(data, f"{user_login}_rates_{timestamp}.json")


if __name__ == "__main__":
    main()