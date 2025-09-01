"""
Парсер оценок фильмов с Letterboxd.
Собирает: название, год, рейтинг, дату просмотра.
Экспортирует в Excel и JSON.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from datetime import datetime


def collect_user_rates(user_login: str, max_pages: int = None) -> list:
    """
    Собирает все оценённые фильмы пользователя.

    :param user_login: Логин пользователя
    :param max_pages: Максимум страниц (None = все)
    :return: Список словарей с данными
    """
    base_url = f"https://letterboxd.com/{user_login}/films/diary/"
    data = []
    page_num = 1

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print(f"Парсинг профиля: {user_login}")

    while True:
        # Формируем URL
        if page_num == 1:
            url = base_url
        else:
            url = f"{base_url}page/{page_num}/"

        print(f"Загрузка: {url}")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

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
                    # Пропускаем фильмы без оценки
                    if 'not-rated' in entry.get('class', []):
                        continue

                    # Название фильма
                    td_film = entry.find('td', class_='td-film-details')
                    film_name = td_film.find('a').get_text(strip=True) if td_film else "Неизвестно"

                    # Год выпуска
                    td_release = entry.find('td', class_='td-released center')
                    release_date = td_release.get_text(strip=True) if td_release else "Неизвестно"

                    # Оценка
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

                    # Дата просмотра
                    date_td = entry.find('td', class_='td-day diary-day center')
                    watch_date = date_td.get_text(strip=True) if date_td else "Неизвестно"

                    data.append({
                        'film_name': film_name,
                        'release_date': release_date,
                        'rating': rating,
                        'watch_date': watch_date
                    })

                except Exception as e:
                    print(f"Ошибка при обработке записи: {e}")
                    continue

            page_num += 1

            # Ограничение по страницам
            if max_pages and page_num > max_pages:
                print(f"Достигнут лимит в {max_pages} страниц.")
                break

            time.sleep(1)  # Вежливая задержка

        except requests.RequestException as e:
            print(f"Ошибка запроса: {e}")
            break
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
            break

    print(f"Собрано: {len(data)} оценённых фильмов.")
    return data


def save_to_excel( list, filename: str):
    """Сохраняет данные в Excel."""
    if not 
        print("Нет данных для сохранения.")
        return

    df = pd.DataFrame(data)
    try:
        df.to_excel(filename, index=False)
        print(f"Сохранено в Excel: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении Excel: {e}")


def save_to_json( list, filename: str):
    """Сохраняет данные в JSON."""
    if not 
        print("Нет данных для сохранения.")
        return

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Сохранено в JSON: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении JSON: {e}")


def main():
    print("Парсер оценок с Letterboxd")
    user_login = input("Введите логин пользователя: ").strip()
    if not user_login:
        print("Логин не может быть пустым.")
        return

    max_pages_input = input("Макс. страниц (Enter = все): ").strip()
    max_pages = int(max_pages_input) if max_pages_input.isdigit() else None
    if max_pages and max_pages < 1:
        max_pages = None

    data = collect_user_rates(user_login, max_pages)

    if not 
        print("Нет данных для сохранения.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_filename = f"{user_login}_rates_{timestamp}.xlsx"
    json_filename = f"{user_login}_rates_{timestamp}.json"

    save_to_excel(data, excel_filename)
    save_to_json(data, json_filename)


if __name__ == "__main__":
    main()
