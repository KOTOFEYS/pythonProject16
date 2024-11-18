from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from pyexpat.errors import messages

api = '7675818970:AAGREOEOIX5WdTA0XtEJANLQwc-vvIsBKbE'
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

start_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Рассчитать"),KeyboardButton(text="Информация")],
                                           [KeyboardButton(text="Купить")]],
                         resize_keyboard=True)

kb2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Рассчитать норму калорий", callback_data= "Calories"),
     InlineKeyboardButton(text = "Формулы расчёта", callback_data= "formulas")
            ]], resize_keyboard=True)
kb3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Product1", callback_data= "product_buying"),
    InlineKeyboardButton(text = "Product2", callback_data= "product_buying"),
    InlineKeyboardButton(text = "Product3", callback_data= "product_buying"),
    InlineKeyboardButton(text = "Product4", callback_data= "product_buying")]],
    resize_keyboard=True)
number_1 = 1
number_2 = 2
number_3 = 3
number_4 = 4

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=start_menu)

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:',reply_markup=kb2)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('(10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A')
    await call.answer()

@dp.callback_query_handler(text = 'Calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст.')
    await UserState.age.set()


@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    calories = 10 * int(data['weight']) + 6,25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма колорий{calories}.')
    await state.finish()

@dp.message_handler(text = "Купить")
async def get_buying_list(message):
    await message.answer(f"Название: Product {number_1}  | Описание: описание {number_1} | Цена: {number_1 * 100}")
    with open('png1/1.png',"rb") as img:
        await message.answer_photo(img)
    await message.answer(f"Название: Product {number_2}  | Описание: описание {number_2} | Цена: {number_2 * 100}")
    with open('png1/2.png','rb') as img:
        await message.answer_photo(img)
    await message.answer(f"Название: Product {number_3}  | Описание: описание {number_3} | Цена: {number_3 * 100}")
    with open('png1/3.jpg','rb') as img:
        await message.answer_photo(img)
    await message.answer(f"Название: Product {number_4}  | Описание: описание {number_4} | Цена: {number_4 * 100}")
    with open('png1/4.png','rb') as img:
        await message.answer_photo(img)
    await message.answer("Выберите продукт для покупки:", reply_markup=kb3)

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()









if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)