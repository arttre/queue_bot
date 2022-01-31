import logging
import requests
import os
from dotenv import load_dotenv, find_dotenv

from aiogram import Bot, Dispatcher, executor, types

load_dotenv(find_dotenv())

API_TOKEN = os.environ['API_TOKEN']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

URL = os.environ['URL']

QUEUE_NOW = 4


@dp.message_handler(commands=['start'])
async def func_now(message: types.Message):
    await message.reply("Вітаємо вас! За допомогою цього боту ви можете слідкувати за чергою онлайн.")


@dp.message_handler(commands=['now'])
async def func_now(message: types.Message):

    r = requests.get(url=URL)
    arr = r.json()

    if not arr:
        await message.reply("У приймальній комісії нікого немає!")
    else:
        queue_list = "Зараз у приймальній комісії:"+os.linesep

        if len(arr) >= QUEUE_NOW:
            for i in arr[0:QUEUE_NOW]:
                queue_list += str(i) + os.linesep
            await message.reply(queue_list)
        else:
            for i in arr:
                queue_list += str(i) + os.linesep
            await message.reply(queue_list)


@dp.message_handler(commands=['next'])
async def func_help(message: types.Message):

    r = requests.get(url=URL)
    arr = r.json()
    queue_list = "Наступні 4 людини у черзі:"+os.linesep

    if not arr:
        await message.reply("У приймальній комісії нікого немає!")
    elif len(arr) <= QUEUE_NOW:
        await message.reply("У черзі нікого немає!")
    elif len(arr)-QUEUE_NOW <= 3:
        for i in arr[QUEUE_NOW:len(arr)]:
            queue_list += str(i) + os.linesep
        await message.reply(queue_list)
    else:
        for i in arr[QUEUE_NOW:QUEUE_NOW+4]:
            queue_list += str(i) + os.linesep
        await message.reply(queue_list)


@dp.message_handler(commands=['queue'])
async def func_queue(message: types.Message):

    r = requests.get(url=URL)
    arr = r.json()
    queue_list = "Загальна черга:"+os.linesep
    if not arr:
        await message.reply("У приймальній комісії нікого немає!")
    else:
        for i in arr:
            queue_list += str(i) + os.linesep
        await message.reply(queue_list)


@dp.message_handler(text_startswith=['change_now_to_'])
async def func_help(message: types.Message):
    if str(message.chat.id) == os.environ['ADMIN_ID']:
        msg = str(message.text)
        new_queue_now = int(msg[14:len(msg)])
        global QUEUE_NOW
        if not new_queue_now:
            QUEUE_NOW = 4
            await message.reply("Кількість людей у ПК було змінено на 4!")
        else:
            QUEUE_NOW = new_queue_now
            await message.reply(f"Зміна кількості людей у ПК на {QUEUE_NOW} пройшла успішно")
    else:
        await message.reply("Чєл, успокойся, ти не адмін..(")


@dp.message_handler()
async def func_trash(message: types.Message):
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
