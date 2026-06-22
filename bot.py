import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я бесплатный AI-бот 🤖")


@dp.message()
async def chat(message: types.Message):
    user_text = message.text

    if not user_text:
        await message.answer("Я понимаю только текст")
        return

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "Ты полезный ассистент."},
                    {"role": "user", "content": user_text}
                ]
            }
        )

        answer = response.json()["choices"][0]["message"]["content"]
        await message.answer(answer)

    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())