# Letterboxd Parser 🎬

Простой и надёжный парсер оценок фильмов с [Letterboxd](https://letterboxd.com).

Собирает:
- Название фильма
- Год выпуска
- Оценку (в баллах: 1–10)

и экспортирует всё в **Excel-файл**.

---

## Как использовать

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   либо :
   python -m pip install requests beautifulsoup4 lxml pandas openpyxl

2. Запустите скрипт:
   python main.py
   
3. Введите логин пользователя Letterboxd (например, rfeldman9)


4. Получите файл вида: ваш_логин_letterboxd_rates.xlsx
