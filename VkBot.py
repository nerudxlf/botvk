import vk_api
from vk_api.longpoll import VkLongPoll
import sqlite3
import json
from datetime import datetime


class VKBot:
    """"class bot"""
    def __init__(self, token):
        """констрокутор"""
        vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()
        self.current_date = datetime.now().date()
        self.sql_arr = [
            "SELECT * FROM covid_coord WHERE city=?",
            "SELECT * FROM covid WHERE (title=? AND data LIKE ?)"
        ]
        self.command = [
            "/коронавирус",
            "/выход",
            "/симптомы",
            "/карта"
        ]

    def get_longpoll(self):
        """получаем лонгпулл"""
        return self.longpoll

    def check_covid(self, event, number):
        """для обрабоки городов"""
        self.vk.messages.send(
            user_id=event.user_id,
            message=(
                "Введите название города или региона\n"
            ),
            random_id=number
        )
        return True

    def send_info_covid(self, number, event, request):
        """отправка сообщения с последней информацией по коронавирусу"""
        msg = self.sql_request(number, event, self.sql_arr[1], request)  # получаем массив с данными
        try:
            city = msg[0]  # обрабатываю данные для сообщения
            sick = msg[4]
            healed = msg[5]
            died = msg[6]
            sick_incr = msg[7]
            healed_incr = msg[8]
            died_incr = msg[9]
            data = msg[10]
            self.vk.messages.send(
                user_id=event.user_id,
                message=(  # отправляю сообщение пользователю
                        "Город: " + str(city) + "\n"
                        "Всего больных: " + str(sick) + "\n"
                        "Всего вылечившихся: " + str(healed) + "\n"
                        "Всего умерших: " + str(died) + "\n"
                        "Новых больных за сегодня: " + str(sick_incr) + "\n"
                        "Выздоровевших за сегодня: " + str(healed_incr) + "\n"
                        "Умерших за сегодня: " + str(died_incr) + "\n"
                        "Дата " + str(data) + "\n"
                        "Полезные ссылки:\n"
                        'https://xn--80aesfpebagmfblc0a.xn--p1ai/\n'
                ),
                random_id=number
            )
        except TypeError:
            print("Err")

    def send_main_msg(self, number, event):
        """вывожу список всех команд"""
        line_command = ""
        for i in range(len(self.command)):
            line_command += str(self.command[i]) + "\n"
        self.vk.messages.send(
            user_id=event.user_id,
            message=(
                    "Команды на данный момент:\n" + line_command
            ),
            random_id=number
        )

    def link_ya_map(self, number, event, request):
        """формирую ссылку на яндекс карты"""
        msg = self.sql_request(number, event, self.sql_arr[0], request, 0)  # получаю данные
        try:
            city = msg[0]  # формирую данные
            c_Y = msg[1][:5]  # получаю координаты до 3 знака после запятой
            c_X = msg[2][:5]
            self.vk.messages.send(  # отправляю сообщение
                user_id=event.user_id,
                message=(
                    "Ссылка на яндекс карту города "+str(city)+"\n"
                    "https://yandex.ru/web-maps/covid19?ll="+str(c_X)+"%2C"+str(c_Y)+"&z=10"+"\n"
                    "Чтобы выйти напишите /выход"
                ),
                random_id=number
            )
        except TypeError:
            print("Err")

    def sql_request(self, number, event, sql, arg1=0, arg2=1):
        """получаю данные из базы данных"""
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        try:
            if arg2 == 0:  # если второй аргумент равен нулю то отправляем данные из таблицы с координатами
                cursor.execute(sql, ([arg1]))
                line = cursor.fetchall()[0]
            else:  # отпалвяем данные из таблицы с информацией по коронавирусу
                cursor.execute(sql, ([arg1, self.current_date]))
                line = list(cursor.fetchall()[-1])
            return line
        except IndexError:  # если данные не найдены то отправляем это сообщение
            self.vk.messages.send(
                user_id=event.user_id,
                message=(
                    'Скорее всего, вы опечатались, попробуйте еще раз\n'
                    'Некоторые регионы не получается найти потому что\n'
                    'берется статистика за весь регион или область\n'
                    'Пример: Омская область; Краснодарский край\n'
                    'Или напишите команду /выход'
                ),
                random_id=number
            )
            return 0

    def send_symptoms(self, number, event):
        """обработка симптомов"""
        try:
            with open("data.json", "r") as read_file:  # считываем данные из файла
                data = json.load(read_file)
                string = data["covid-19"]["symptoms"]
            self.vk.messages.send(  # отправляем их пользователю
                user_id=event.user_id,
                message=(
                    "Сипмтомы covid-19:\n"+string
                ),
                random_id=number
            )
        except FileNotFoundError:
            print("Error File not found")
