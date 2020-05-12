from vk_api.longpoll import VkEventType
import random
import VkBot

token = 'fe86ae7960ef3db6d61df4954f582353194cc8f935f1457d99c73a94a79239d15357b0c65878b558dccac'
main_bot = VkBot.VKBot(token)


def send_messages():
    """цикл работы бота"""
    c_box = False   # флаги переключения
    coord_box = False
    for event in main_bot.get_longpoll().listen():  # цикл обработки событий от пользователя
        if event.type == VkEventType.MESSAGE_NEW:  # обработка нового ответа
            if event.to_me:
                request = event.text  # преобразуем в текст
                number = random.getrandbits(64)  # случайное число для функции message
            print("Send new message:"+str(event.user_id))  # вывожу информацюи о новом событи в консоль
            if request == "/выход":  # команда выход
                main_bot.send_main_msg(number, event)  # выкидываю сообщение о доступных командах
                c_box = False  # выключаю флаги
                coord_box = False
            if request == "/коронавирус":  # команда коронавирус
                c_box = main_bot.check_covid(event, number)  # сообщение для пользователя, функция возвращает True
            elif request and c_box:  # запускает обработку города
                main_bot.send_info_covid(number, event, request)  # выводлит информацию для пользователя по городу
            if request == "/симптомы":  # команда симтомы
                main_bot.send_symptoms(number, event)  # выводит симптомы коронавирса
            if request == "/карта":  # команда карта
                coord_box = main_bot.check_covid(event, number)  # сообщение для пользователя, функция возвращает True
            elif request and coord_box:  # запускает обработку города для возвращения ссылки
                main_bot.link_ya_map(number, event, request)  # отправляет сообщения ссылкой на город на картах
            if request:
                main_bot.send_main_msg(number, event)  # выводит список команд


def main():
    send_messages()


if __name__ == '__main__':  # точка входа в программу
    main()