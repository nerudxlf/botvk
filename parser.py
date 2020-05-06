import requests
from bs4 import BeautifulSoup
import json
import sqlite3
from datetime import datetime

url_arr = [
    'https://xn--80aesfpebagmfblc0a.xn--p1ai/information/',
    'https://www.who.int/ru/emergencies/diseases/novel-coronavirus-2019/advice-for-public/q-a-coronaviruses',
    'http://alextyurin.ru/2014/04/%D0%B3%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5-%D0%BA%D0%BE%D0%BE%D1%80%D0%B4%D0%B8%D0%BD%D0%B0%D1%82%D1%8B-%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D1%8B%D1%85/'
]


def json_line_info(line):
    """create psevdo json"""
    newLine = ""
    checkBox = False
    for i in range(len(line)):
        if line[i] == "[" or checkBox:
            newLine += line[i]
            checkBox = True
        if line[i] == "]":
            return newLine


def accept_data(url):
    """parse site"""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    line = soup.find("cv-spread-overview")
    jsonLine = json_line_info(str(line))
    toJson = json.loads(jsonLine)  # create json string for send msg in bd
    return toJson


def send_russian_data_to_bd(url):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    jsonLine = accept_data(url)
    current_date = datetime.now().date()
    for i in range(len(jsonLine)):
        jsonLine[i].pop("is_city")
        jsonLine[i].update({"data": current_date})
        cursor.execute(
            "INSERT INTO covid VALUES(?,?,?,?,?,?,?,?,?,?,?)", [
                jsonLine[i]["title"], jsonLine[i]["code"], jsonLine[i]["coord_x"],
                jsonLine[i]["coord_y"], jsonLine[i]["sick"], jsonLine[i]["healed"], jsonLine[i]["died"],
                jsonLine[i]["sick_incr"], jsonLine[i]["healed_incr"], jsonLine[i]["died_incr"], jsonLine[i]["data"]])
    conn.commit()


def parse_symptoms(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    line = soup.findAll("p")[7].getText()
    dict_covid_data = {"covid-19": {"symptoms": line}}
    with open("data.json", "w") as write_file:
        json.dump(dict_covid_data, write_file)


def parse_coord(url):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    data = soup.find("tbody")
    arr_data = []
    x = 0
    y = 1
    z = 2
    for line in data.findAll("tr"):
        for word in line.findAll("td"):
            arr_data.append(word.getText())
        cursor.execute(
            "INSERT INTO covid_coord VALUES(?,?,?)",[
                arr_data[x], arr_data[y], arr_data[z]
            ]
        )
        x += 4
        y += 4
        z += 4
    conn.commit()


def main():
    print("Menu:\n1-update db covid\n2-update coord")
    num = int(input())
    while True:
        if num == 1:
            send_russian_data_to_bd(url_arr[0])
        elif num == 2:
            parse_coord(url_arr[2])
        else:
            parse_symptoms(url_arr[1])


if __name__ == '__main__':
    main()
