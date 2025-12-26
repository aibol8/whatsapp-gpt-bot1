import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOOKING_LINK = os.getenv("BOOKING_LINK")
SALON_NAME = os.getenv("SALON_NAME")

openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = f"""Ты вежливый администратор салона {SALON_NAME}.
Отвечай на любые вопросы клиентов о салоне, мастерах, услугах и ценах.
Если клиент хочет записаться, отправляй ссылку {BOOKING_LINK}.
Не записывай клиентов сам. Всегда дружелюбен и краток."""

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.0-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply = response.choices[0].message.content
    except Exception:
        reply = "Извините, произошла ошибка, попробуйте позже."
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
