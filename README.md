# Letterboxd Parser 🎬

Простой и надёжный парсер оценок фильмов с [Letterboxd](https://letterboxd.com).

Собирает:
- Название фильма
- Год выпуска
- Оценку (в баллах: 1–10)
- Количество просмотров

Собранные данные экспортируются в 2-х форматах:

* JSON
* Excel
---

## Как использовать

1. Установите зависимости:
   ```bash 

   pip install requests beautifulsoup4 pandas openpyxl
или
 
     
    python -m pip install requests beautifulsoup4 lxml pandas openpyxl

2. Запустите скрипт:
   python main.py


   
3. Введите логин пользователя Letterboxd (например, rfeldman9)

 ## Пример работы :
 
   == Парсер Litterboxd ==

 Название фильма - Чужой 
 Дата выпуска - 1979
 






4. Получите файл вида: ваш_логин_letterboxd_rates.xlsx
