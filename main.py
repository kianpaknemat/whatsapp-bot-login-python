from login import whatsapp_login

phone = input("شماره تلفن بدون کد کشور وارد کنید: ").strip()

driver = whatsapp_login(phone)
