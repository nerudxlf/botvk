import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import sqlite3
from datetime import datetime


class VKBot:
    """"class bot"""
    def __init__(self, token):
        vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()
        self.current_date = datetime.now().date()
        self.sql_arr = [
            "SELECT * FROM covid WHERE title=?",
            "SELECT * FROM covid WHERE (title=? AND data LIKE ?)"
        ]
        self.command = [
            "/коронавирус",
            "/выход"
        ]

    def set_longpoll(self):
        return self.longpoll

    def check_covid(self, event, number):
        self.vk.messages.send(
            user_id=event.user_id,
            message=(
                "Введите название города или региона\n"
                "Пример: Москва, Краснодарский край, Орловская область"
            ),
            random_id=number
        )
        return True

    def send_info_covid(self, number, event, request):
        msg = self.sql_request(self.sql_arr[1], request)
        try:
            city = msg[0]
            sick = msg[4]
            healed = msg[5]
            died = msg[6]
            sick_incr = msg[7]
            healed_incr = msg[8]
            died_incr = msg[9]
            data = msg[10]
            self.vk.messages.send(
                user_id=event.user_id,
                message=(
                        "Город: " + str(city) + "\n"
                                                "Всего больных: " + str(sick) + "\n"
                                                                                "Всего вылечившихся: " + str(
                    healed) + "\n"
                              "Всего умерших: " + str(died) + "\n"
                                                              "Новых больных за сегодня: " + str(sick_incr) + "\n"
                                                                                                              "Выздоровевших за сегодня: " + str(
                    healed_incr) + "\n"
                                   "Умерших за сегодня: " + str(died_incr) + "\n"
                                                                             "Дата " + str(data) + "\n"
                                                                                                   "Полезные ссылки:\n"
                                                                                                   'https://xn--80aesfpebagmfblc0a.xn--p1ai/\n'
                ),
                random_id=number
            )
        except IndexError:
            self.vk.messages.send(
                user_id=event.user_id,
                message=(
                    'Скорее всего, вы опечатались, попробуйте еще раз\n'
                    'Некоторые регионы не получается найти потому что\n'
                    'берется статистика за весь регион или область\n'
                    'Пример: Омская область; Краснодарский край'
                ),
                random_id=number
            )

    def send_main_msg(self, number, event):
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

    def sql_request(self, sql, arg1=0):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        if arg1 == 0:
            line = cursor.execute(sql)
        else:
            cursor.execute(sql, ([arg1, self.current_date]))
            line = list(cursor.fetchall()[-1])
        return line
