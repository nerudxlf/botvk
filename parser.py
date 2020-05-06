import requests
from bs4 import BeautifulSoup
import json
import sqlite3
from datetime import datetime


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


def accept_data():
    """parse site"""
    url = 'https://xn--80aesfpebagmfblc0a.xn--p1ai/information/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    line = soup.find("cv-spread-overview")
    jsonLine = json_line_info(str(line))
    toJson = json.loads(jsonLine)  # create json string for send msg in bd
    return toJson


def send_russian_data_to_bd():
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    jsonLine = accept_data()
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


def main():
    print("Update table Y/N")
    if str(input()) == "Y":
        send_russian_data_to_bd()
    else:
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        current_date = datetime.now().date()
        print(current_date)
        sql = "SELECT * FROM covid WHERE (title=? AND data LIKE ?)"
        cursor.execute(sql, (["Москва", current_date]))
        print(cursor.fetchall()[0])


if __name__ == '__main__':
    main()
