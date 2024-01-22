import requests
import re
import sqlite3
from selenium import webdriver
import sqlite3
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    
from selenium.webdriver.common.by import By
import time






#Тут могла быть ваша реклама






login = "LOGIN_MOODLE"
pwd = "PWD_MOODLE"

conn = sqlite3.connect('mydatabase.db')
c = conn.cursor()
c.execute('SELECT name FROM group_names')
names = c.fetchall()

driver = webdriver.Firefox()

driver.get("https://moodle.preco.ru/login/index.php")
driver.find_element(By.ID, "username").send_keys(login)
driver.find_element(By.ID, "password").send_keys(pwd)
driver.find_element(By.ID, "loginbtn").click()

# Клиним
c.execute('DROP TABLE IF EXISTS schedule_210')
c.execute('DROP TABLE IF EXISTS schedule_218')

# Криэйтим
c.execute('CREATE TABLE schedule_210 (date text, schedule_raw text)')
c.execute('CREATE TABLE schedule_218 (date text, schedule_raw text)')

for name in names:
    driver.get("https://moodle.preco.ru/blocks/lkstudents/sheduleonline.php")
    option = driver.find_element(By.XPATH, f'//option[text()="{name[0]}"]')
    driver.execute_script("arguments[0].setAttribute('selected', '')", option)
    
    form = driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(1)

    # Парсинг 'urk_scheduleblock'
    schedule_blocks = driver.find_elements(By.CLASS_NAME, 'urk_sheduleblock')
    schedule_raw = [block.text for block in schedule_blocks]
    time.sleep(1)

    # Высер больного ебан... Форматируем ячейки
    schedule_formatted = []
    for day in schedule_raw:
        day = re.sub(r'(\d{1,2}:\d{2})\n?(\d{1,2}:\d{2})', r'\1-\2', day)  # объединяем время
        day = re.sub(r'([А-Яа-я]+) ([А-Яа-я]+) ([А-Яа-я]+)', r'\1 \3', day)  # удаляем лишние имена
        schedule_formatted.append(day)

    # Импорт в бд
    for i, day in enumerate(schedule_formatted, 1):
        # разбиваем дни на строки и берем первую строку в качестве даты
        date = day.split('\n')[0]
        # ponooooos
        if 'П-210' in name[0]:
            c.execute(f"INSERT INTO schedule_210 VALUES (?, ?)", (date, day))
        elif 'ПД-218' in name[0]:
            c.execute(f"INSERT INTO schedule_218 VALUES (?, ?)", (date, day))

# Сохраняем изменения
conn.commit()
conn.close()
driver.close()