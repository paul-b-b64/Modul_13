from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button1)
kb.add(button2)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Нажми кнопку!', reply_markup=kb)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    # Формула Миффлина
    Norm_Kal = float(data['weight']) * 10.0 + float(data['growth']) * 6.25 + float(data['age']) * 5.0
    Norm_Kal_m = Norm_Kal + 5
    Norm_Kal_f = Norm_Kal - 161
    await message.answer(f'Ваша норма калорий {Norm_Kal_m}, если Вы - мужчина, и {Norm_Kal_f} - если женщина.')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
