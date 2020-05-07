import requests
from bs4 import BeautifulSoup
import json
import sqlite3
from datetime import datetime

url_arr = [  # массив с ссылками на ресурсы
    'https://xn--80aesfpebagmfblc0a.xn--p1ai/information/',
    'https://www.who.int/ru/emergencies/diseases/novel-coronavirus-2019/advice-for-public/q-a-coronaviruses',
    'http://alextyurin.ru/2014/04/%D0%B3%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5-%D0%BA%D0%BE%D0%BE%D1%80%D0%B4%D0%B8%D0%BD%D0%B0%D1%82%D1%8B-%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D1%8B%D1%85/'
]


def json_line_info(line):
    """функция которая из возвращает строку из всего текста полученного со страницы"""
    new_line = ""
    check_box = False
    for i in range(len(line)):  # считыват символы между двумя скобками, возвращает полученную строку
        if line[i] == "[" or check_box:
            new_line += line[i]
            check_box = True
        if line[i] == "]":
            return new_line


def accept_data(url):
    """получаю данные с сайта они там лежат в атрибуте тега в виде json строки"""
    page = requests.get(url)  # получаю страницу
    soup = BeautifulSoup(page.text, 'lxml')  # с помощбю парсера преобразу ее текст
    line = soup.find("cv-spread-overview")  # нахожу необходимый тег
    json_line = json_line_info(str(line))  # забираю от туда необходиммые данные
    to_json = json.loads(json_line)  # преобразую эти данные в json строку
    return to_json  # возвращаю эту json строку


def send_russian_data_to_bd(url):
    """отправляю данные с коронавирусом в базу данных"""
    conn = sqlite3.connect("mydatabase.db")  # подключась к базе данных
    cursor = conn.cursor()  # взаимодействую с бд
    json_line = accept_data(url)  # получаю json строку
    current_date = datetime.now().date()  # актуальная дата
    for i in range(len(json_line)):  # цикл загрузки данных в бд
        json_line[i].pop("is_city")  # удаляю не нужную информацию из словоря
        json_line[i].update({"data": current_date})  # добавляю дату в словал
        cursor.execute(  # здесь просто формирование данных в таблице
            "INSERT INTO covid VALUES(?,?,?,?,?,?,?,?,?,?,?)", [
                json_line[i]["title"], json_line[i]["code"], json_line[i]["coord_x"],
                json_line[i]["coord_y"], json_line[i]["sick"], json_line[i]["healed"], json_line[i]["died"],
                json_line[i]["sick_incr"], json_line[i]["healed_incr"], json_line[i]["died_incr"], json_line[i]["data"]])
    conn.commit()  # а тут коммит в таблицу


def parse_symptoms(url):
    """полученние симптомов коронавирса"""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    line = soup.findAll("p")[7].getText()  # получаю текст из необходимого тега (надеюсь они не добавят новый параграф)
    dict_covid_data = {"covid-19": {"symptoms": line}}  # создаю словарь с инофрмацией (мб еще понадобится)
    with open("data.json", "w") as write_file:  # записываю все в json файл
        json.dump(dict_covid_data, write_file)


def parse_coord(url):
    """получаю координаты городов россии (самых крупны(+-))"""
    conn = sqlite3.connect("mydatabase.db")  # подключаюсь к бд
    cursor = conn.cursor()
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    data = soup.find("tbody")  # нахожу на странице таблицу
    arr_data = []  # массив для заполнения его информацией
    x = 0  # переменны для заполнения по индексу
    y = 1
    z = 2
    for line in data.findAll("tr"):  # прохожусь по каждой строчку и забираю необходимые данные
        for word in line.findAll("td"):
            arr_data.append(word.getText())
        cursor.execute(  # формирую таблицу
            "INSERT INTO covid_coord VALUES(?,?,?)", [
                arr_data[x], arr_data[y], arr_data[z]
            ]
        )
        x += 4
        y += 4
        z += 4
    conn.commit()  # добавляю данные в таблицу


def main():
    """меня для использование использования всего этого"""
    print("Menu:\n1-update db covid\n2-update coord")
    num = int(input())
    while True:
        if num == 1:
            send_russian_data_to_bd(url_arr[0])
        elif num == 2:
            parse_coord(url_arr[2])
        else:
            parse_symptoms(url_arr[1])


if __name__ == '__main__':  # точка фхода
    main()
