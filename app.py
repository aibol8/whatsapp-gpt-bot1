from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
from config import OPENAI_API_KEY, BOOKING_LINK, SALON_NAME

app = Flask(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = f"""Ты вежливый администратор салона {SALON_NAME}.
Отвечай на любые вопросы клиентов о салоне, мастерах, услугах и ценах.
Если клиент хочет записаться, отправляй ссылку {BOOKING_LINK}.
Не записывай клиентов сам. Всегда дружелюбен и краток."""

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "")
    resp = MessagingResponse()

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

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


