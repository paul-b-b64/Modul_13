from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

api = '7502385552:AAEYeqGY7MEDC_o7hRo1ljFTgpNZhseYXxM'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

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

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот, тебе помогающий!', reply_markup=kb_repl)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = ['ball.png', 'canz_tov.png', 'globus.png', 'sewing.png']
    for i in range(0, 4):
        await message.answer(f'Название: Product{i+1} '
                             f'\nОписание: Описание{i+1} '
                             f'\nЦена: {(i+1)*100}')
        with open(f'Products_foto/{products[i]}', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_inl)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
