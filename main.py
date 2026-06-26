import os
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json

TOKEN = os.getenv("TOKEN")

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def keyboard():
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                {"action": {"type": "text", "label": "🍣 Меню"}, "color": "positive"}
            ],
            [
                {"action": {"type": "text", "label": "🛒 Заказ"}, "color": "primary"}
            ],
            [
                {"action": {"type": "text", "label": "🚚 Доставка"}, "color": "secondary"}
            ],
            [
                {"action": {"type": "text", "label": "📞 Контакты"}, "color": "secondary"}
            ]
        ]
    }, ensure_ascii=False)

def send(user_id, text, kb=None):
    vk.messages.send(
        user_id=user_id,
        message=text,
        random_id=0,
        keyboard=kb
    )

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        uid = event.user_id

        if msg in ["привет", "start", "меню"]:
            send(uid, "🍣 Добро пожаловать в Суши-бар!", keyboard())

        elif msg == "🍣 меню":
            send(uid, "Филадельфия — 420₽\nКалифорния — 390₽\nДракон — 450₽")

        elif msg == "🛒 заказ":
            send(uid, "Напиши заказ и адрес 🚚")

        elif msg == "🚚 доставка":
            send(uid, "Доставка 30–60 минут")

        elif msg == "📞 контакты":
            send(uid, "Тел: +7 000 000 00 00")

        else:
            send(uid, "Нажми кнопку 👇", keyboard())
