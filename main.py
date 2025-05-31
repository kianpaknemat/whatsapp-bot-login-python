from models.login import whatsapp_login
from dotenv import load_dotenv
import os
import APIs
import asyncio
import websocket
import json


load_dotenv()
user_token = os.getenv("user_token")
agent = os.getenv("agent")
token = os.getenv("TOKEN")
phone = input("شماره تلفن بدون کد کشور وارد کنید: ").strip()

user_phone = input("شماره ای که میخوای براش بره رو بدون کد کشور بزن: ")
user_phone = "+98" + user_phone

prompt = "در مورد آروند توضیح بده و بگو چیکار میکنید و قیمت دقیق پلن هاتون رو بگو و نمونه کار هاتون رو هم بگو و بگو تو چه زمینه ای فعالیت میکنید"

driver = whatsapp_login(phone)




def send_whatsapp_message(phone: str, text: str):
    ws = websocket.create_connection("ws://localhost:3000")

    message = {
        "phone": phone,
        "text": text
    }

    ws.send(json.dumps(message))
    ws.close()


# تست

if driver:
    print(user_phone)
    send_whatsapp_message("989382885712", "سلام از طرف پایتون!")





