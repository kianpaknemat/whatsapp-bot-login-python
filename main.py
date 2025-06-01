from models.login import whatsapp_login
import os
import requests
from dotenv import load_dotenv
import subprocess
import time



load_dotenv()
user_token = os.getenv("user_token")
agent = os.getenv("agent")
token = os.getenv("TOKEN")
phone_number = input("شماره تلفن بدون کد کشور وارد کنید: ").strip()

# user_phone = input("شماره ای که میخوای براش بره رو بدون کد کشور بزن: ")
# user_phone = "98" + user_phone

prompt = "در مورد آروند توضیح بده و بگو چیکار میکنید و قیمت دقیق پلن هاتون رو بگو و نمونه کار هاتون رو هم بگو و بگو تو چه زمینه ای فعالیت میکنید"

driver = whatsapp_login(phone_number)


def send_whatsapp_message(phone):
    node_process = subprocess.Popen(['node', 'whatsapp_agent.js'])
    time.sleep(2)


    url = 'http://localhost:3000/start'
    print(node_process)
    print("hiiiiiiii")
    response = requests.post(url, json={'phone': phone})

    print('Response:', response.text)


if driver:
    send_whatsapp_message(phone_number)




