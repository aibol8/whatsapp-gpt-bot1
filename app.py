from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
from config import OPENAI_API_KEY, BOOKING_LINK, SALON_NAME
import time

app = Flask(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = f"""Ты вежливый администратор салона {SALON_NAME}.
Отвечай на любые вопросы клиентов о салоне, мастерах, услугах и ценах.
Если клиент хочет записаться, отправляй ссылку {BOOKING_LINK}.
Не записывай клиентов сам. Всегда дружелюбен и краток."""

# 👇 антиспам по частоте (в памяти)
user_last_message = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "")
    from_number = request.values.get("From")
    resp = MessagingResponse()

    # ---------- ЗАЩИТА ----------
    incoming_msg = incoming_msg.strip()

    # 1️⃣ Пустое сообщение
    if not incoming_msg:
        resp.message("Напишите ваш вопрос, пожалуйста 🙂")
        return str(resp)

    # 2️⃣ Лимит длины
    MAX_LEN = 500
    if len(incoming_msg) > MAX_LEN:
        resp.message(
            f"Сообщение слишком длинное 🙏\n"
            f"Пожалуйста, сократите до {MAX_LEN} символов."
        )
        return str(resp)

    # 3️⃣ Антиспам по частоте
    now = time.time()
    last_time = user_last_message.get(from_number, 0)

    if now - last_time < 3:
        resp.message("Пожалуйста, не так быстро 🙂")
        return str(resp)

    user_last_message[from_number] = now
    # ---------- КОНЕЦ ЗАЩИТЫ ----------

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        print("ERROR:", e)
        reply = "Извините, произошла ошибка. Попробуйте позже."

    resp.message(reply)
    return str(resp)




