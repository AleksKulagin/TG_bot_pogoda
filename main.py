import logging
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram import Router
import aiohttp
import asyncio  # Для использования asyncio.run
from config import TOKEN, WEATHER_API_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO)

API_TOKEN = TOKEN
WEATHER_API_KEY = WEATHER_API_KEY

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

class WeatherStates(StatesGroup):
    waiting_for_city = State()

@router.message(F.text == '/start')
async def start_command(message: Message):
    await message.answer("Привет! Отправь мне 'погода', чтобы узнать прогноз.")

@router.message(F.text == '/help')
async def start_command(message: Message):
    await message.answer("Отправь мне 'погода', я спрошу 'В каком городе', выбери любой, чтобы узнать прогноз.")

@router.message(F.text.lower() == 'погода')
async def weather_command(message: Message, state: FSMContext):
    await message.answer("В каком городе?")
    await state.set_state(WeatherStates.waiting_for_city)

@router.message(WeatherStates.waiting_for_city)
async def process_city(message: Message, state: FSMContext):
    city = message.text
    async with aiohttp.ClientSession() as session:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        async with session.get(weather_url) as response:
            if response.status == 200:
                data = await response.json()
                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']
                await message.answer(f"Погода в {city}: {weather_description}, температура: {temperature}°C")
            else:
                await message.answer("Не удалось получить данные о погоде. Проверьте название города.")
    await state.clear()

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())



#


# from aiogram import Bot, Dispatcher, types
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.utils import executor
# from aiogram.types import ParseMode
# import aiohttp
# import os
# from config import TOKEN, WEATHER_API_KEY
#
# API_TOKEN = TOKEN
# WEATHER_API_KEY = WEATHER_API_KEY
#
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
# dp.middleware.setup(LoggingMiddleware())
#
#
# class WeatherStates(StatesGroup):
#     waiting_for_city = State()
#
#
# @dp.message_handler(commands='start')
# async def start_command(message: types.Message):
#     await message.answer("Привет! Отправь мне 'Погода', чтобы узнать прогноз.")
#
#
# @dp.message_handler(lambda message: message.text.lower() == 'погода')
# async def weather_command(message: types.Message):
#     await message.answer("В каком городе?")
#     await WeatherStates.waiting_for_city.set()
#
#
# @dp.message_handler(state=WeatherStates.waiting_for_city)
# async def process_city(message: types.Message, state: FSMContext):
#     city = message.text
#     async with aiohttp.ClientSession() as session:
#         weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
#         async with session.get(weather_url) as response:
#             if response.status == 200:
#                 data = await response.json()
#                 weather_description = data['weather'][0]['description']
#                 temperature = data['main']['temp']
#                 await message.answer(f"Погода в {city}: {weather_description}, температура: {temperature}°C")
#             else:
#                 await message.answer("Не удалось получить данные о погоде. Проверьте название города.")
#     await state.finish()
#
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)