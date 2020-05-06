import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import sqlite3
import VkBot

token='fe86ae7960ef3db6d61df4954f582353194cc8f935f1457d99c73a94a79239d15357b0c65878b558dccac'

main_bot = VkBot.VKBot(token)


def send_messages():
    """Обработка сообщений"""
    c_box = False
    info_box = True
    for event in main_bot.set_longpoll().listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                number = random.getrandbits(64)  # number for send msg
            print("Send new message: https://vk.com/"+str(event.user_id))
            if request == "/коронавирус":
                c_box = main_bot.check_covid(event, number)
            elif request and c_box:
                main_bot.send_info_covid(number, event, request)
            if request == "/выход":
                main_bot.send_main_msg(number, event)
                c_box = False
            if request:
                main_bot.send_main_msg(number, event)


def main():
    send_messages()


if __name__ == '__main__':
    main()
