from login import whatsapp_login,send_whatsapp_message
from dotenv import load_dotenv
import os
import APIs


load_dotenv()
user_token = os.getenv("user_token")
agent = os.getenv("agent")
token = os.getenv("TOKEN")
phone = input("شماره تلفن بدون کد کشور وارد کنید: ").strip()

user_phone = input("شماره ای که میخوای براش بره رو بدون کد کشور بزن: ")
user_phone = "+98" + user_phone

prompt = "در مورد آروند توضیح بده و بگو چیکار میکنید و قیمت دقیق پلن هاتون رو بگو و نمونه کار هاتون رو هم بگو و بگو تو چه زمینه ای فعالیت میکنید"

driver = whatsapp_login(phone)

response = APIs.generate(agent, prompt, token)
response = response.text
if driver:
    send_whatsapp_message(driver, user_phone, response)




