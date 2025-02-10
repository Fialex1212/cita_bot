from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from data_base.dao import set_user
from keyboards.reply_other_kb import main_kb
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.utils import get_users_list_from_db

start_router = Router()


@start_router.message(F.text == '🏠 Main menu')
@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user = await set_user(tg_id=message.from_user.id,
                          username=message.from_user.username,
                          full_name=message.from_user.full_name)
    greeting = f"Hello, {message.from_user.full_name}! Select what you want to do"
    if user is None:
        greeting = f"Hello, new User! Select what you want to do"

    await message.answer(greeting, reply_markup=main_kb())


@start_router.message(F.text == '❌ Stop everything')
async def stop_fsm(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Everything stop. user keyboard below",
                         reply_markup=main_kb())


@start_router.callback_query(F.data == 'main_menu')
async def main_menu_process(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer('Вы вернулись в главное меню.')
    await call.message.answer(f"Привет, {call.from_user.full_name}! Выбери необходимое действие",
                              reply_markup=main_kb())
    
@start_router.message(F.text == 'Users list')
async def get_users_list(message: Message, state: FSMContext):
    await state.clear()
    users = await get_users_list_from_db()

    if not users:
        await message.answer("Нет пользователей.")
        return

    users_text = "\n".join([f"ID: {user.id}, Name: {user.username}, FullName: {user.full_name}" for user in users])

    await message.answer(f"Список пользователей:\n{users_text}", reply_markup=main_kb())