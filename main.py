import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import sqlite3

vk_session = vk_api.VkApi(
token='fe86ae7960ef3db6d61df4954f582353194cc8f935f1457d99c73a94a79239d15357b0c65878b558dccac')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def sendMessages():
    
    """Обработка сообщений"""
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                number = random.getrandbits(64)# number for send msg
            if request:
                conn = sqlite3.connect("mydatabase.db")# connect with bd
                cursor = conn.cursor()
                sql = "SELECT * FROM covid WHERE title=?"# info for message
                cursor.execute(sql, ([request]))
                msg = cursor.fetchall()# read info
                city = msg[0][0]
                code = msg[0][1]
                cX = msg[0][2]
                cY = msg[0][3]
                sick = msg[0][4]
                healed = msg[0][5]
                died = msg[0][6]
                sick_incr = msg[0][7]
                healed_incr = msg[0][8]
                died_incr = msg[0][9]
                data = msg[0][10]

                vk.messages.send(#send message
                    user_id=event.user_id,
                    message=(
                        'Город: '+str(city)+'\n'
                        'Всего больных: '+str(sick)+'\n'
                        'Всего вылечившихся: '+str(healed)+'\n'
                        'Всего умерших: '+str(died)+'\n'
                        'Новых больных за сегодня: '+str(sick_incr)+'\n'
                        'Выздоровевших за сегодня: '+str(healed_incr)+'\n'
                        'Умерших за сегодня: '+str(died_incr)+'\n'
                        ),
                    random_id=number
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    message='Не понял',
                    random_id=number
                )


def main():
    sendMessages()

if __name__ == '__main__':
    main()
