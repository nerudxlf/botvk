from vk_api.longpoll import VkEventType
import random
import VkBot

token = 'fe86ae7960ef3db6d61df4954f582353194cc8f935f1457d99c73a94a79239d15357b0c65878b558dccac'
main_bot = VkBot.VKBot(token)


def send_messages():
    """Обработка сообщений"""
    c_box = False
    coord_box = False
    for event in main_bot.set_longpoll().listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                number = random.getrandbits(64)  # number for send msg
            print("Send new message:"+str(event.user_id))
            if request == "/выход":
                main_bot.send_main_msg(number, event)
                c_box = False
                coord_box = False
            if request == "/коронавирус":
                c_box = main_bot.check_covid(event, number)
            elif request and c_box:
                main_bot.send_info_covid(number, event, request)
            if request == "/симптомы":
                main_bot.send_symptoms(number, event)
            if request == "/карта":
                coord_box = main_bot.check_covid(event, number)
            elif request and coord_box:
                main_bot.link_ya_map(number, event, request)
            if request:
                main_bot.send_main_msg(number, event)


def main():
    send_messages()


if __name__ == '__main__':#enter
    main()
