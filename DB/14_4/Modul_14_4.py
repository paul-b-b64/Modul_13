from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from crud_functions import *


api = ''
bot = Bot(token=api)
disp = Dispatcher(bot, storage=MemoryStorage())

kb_repl = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ],
        [
            KeyboardButton(text='Купить')
        ]
             ], resize_keyboard=True
)

kb_inl = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Продукт 1', callback_data='product_buying'),
            InlineKeyboardButton(text='Продукт 2', callback_data='product_buying'),
            InlineKeyboardButton(text='Продукт 3', callback_data='product_buying'),
            InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
        ]
    ]
)

@disp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот, тебе помогающий!', reply_markup=kb_repl)

@disp.message_handler(text='Купить')
async def get_buying_list(message):
    products = {1: 'tabl.png', 4: 'ball.png', 3: 'canz_tov.png', 2: 'globus.png', 5: 'sewing.png'}
    list_prod = get_all_products()
    for i in list_prod:
        await message.answer(f'Название: {i[1]} '
                             f'\nОписание: {i[2]} '
                             f'\nЦена: {i[3]}')
        with open(f'../14_3/Products_foto/{products[i[0]]}', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_inl)


@disp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()



if __name__ == '__main__':
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    executor.start_polling(disp, skip_updates=True)
    connection.commit()
    connection.close()

