import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from db_postgres_funcs import get_secret_code, get_top_leaders

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
load_dotenv()

bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()


def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Получить кодовое слово по ID")],
            [KeyboardButton(text="Получить список лидеров")]
        ],
        resize_keyboard=True
    )

def get_back_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Назад")]],
        resize_keyboard=True
    )

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Привет! Я бот для работы с базой данных. Выбери действие:",
        reply_markup=get_main_keyboard()
    )

class Form(StatesGroup):
    waiting_for_user_id = State()


@dp.message(lambda message: message.text == "Получить кодовое слово по ID")
async def get_code_word(message: types.Message, state: FSMContext):
    await message.answer("Введите ID пользователя:")
    await state.set_state(Form.waiting_for_user_id)


@dp.message(Form.waiting_for_user_id)
async def process_user_id(message: types.Message, state: FSMContext):

    user_id = str(message.text).lower()
    secret_code = get_secret_code(user_id)
    if secret_code:
        secret_code = secret_code[0]
    await message.answer(f"Кодовое слово: {secret_code}" if secret_code else "Пользователь не найден")
    await state.clear()


@dp.message(lambda message: message.text == "Получить список лидеров")
async def get_leaders(message: types.Message):
    leaders = get_top_leaders()
    await message.answer(leaders if leaders else "Список пуст")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())