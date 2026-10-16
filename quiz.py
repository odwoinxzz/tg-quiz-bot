import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# Токен твоего бота
TOKEN = "8974105060:AAHTvQp8dVgy4qGbSogkPTAsnNB_H7mG-nI"

# Твой ID для получения заявок
ADMIN_CHAT_ID = 7079814743  

# Состояния для каждого шага анкеты
class MentorshipQuiz(StatesGroup):
    relations = State()
    debts = State()
    realization = State()
    health = State()
    want_mentorship = State()
    contact = State()

dp = Dispatcher(storage=MemoryStorage())

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отменить / Начать заново")]],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Ответь, пожалуйста, на несколько вопросов для анкеты.\n\n"
        "1. Есть ли у тебя проблемы в отношениях?",
        reply_markup=cancel_kb
    )
    await state.set_state(MentorshipQuiz.relations)

@dp.message(F.text == "Отменить / Начать заново")
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Анкета отменена. Напиши /start, чтобы пройти заново.", reply_markup=None)

@dp.message(MentorshipQuiz.relations)
async def process_relations(message: Message, state: FSMContext):
    await state.update_data(relations=message.text)
    await message.answer("2. Есть ли долги, кредиты?")
    await state.set_state(MentorshipQuiz.debts)

@dp.message(MentorshipQuiz.debts)
async def process_debts(message: Message, state: FSMContext):
    await state.update_data(debts=message.text)
    await message.answer("3. Смогла ли ты прийти к реализации?")
    await state.set_state(MentorshipQuiz.realization)

@dp.message(MentorshipQuiz.realization)
async def process_realization(message: Message, state: FSMContext):
    await state.update_data(realization=message.text)
    await message.answer("4. Есть ли проблемы со здоровьем?")
    await state.set_state(MentorshipQuiz.health)

@dp.message(MentorshipQuiz.health)
async def process_health(message: Message, state: FSMContext):
    await state.update_data(health=message.text)
    await message.answer("5. Хочешь ли ты ко мне на наставничество?")
    await state.set_state(MentorshipQuiz.want_mentorship)

@dp.message(MentorshipQuiz.want_mentorship)
async def process_want_mentorship(message: Message, state: FSMContext):
    await state.update_data(want_mentorship=message.text)
    await message.answer("Оставь свои контактные данные (username или номер телефона):")
    await state.set_state(MentorshipQuiz.contact)

@dp.message(MentorshipQuiz.contact)
async def process_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    
    # Формируем итоговый отчет для тебя
    report = (
        f"📩 Новая анкета на наставничество!\n\n"
        f"1️⃣ Проблемы в отношениях: {data.get('relations')}\n"
        f"2️⃣ Долги / кредиты: {data.get('debts')}\n"
        f"3️⃣ Реализация: {data.get('realization')}\n"
        f"4️⃣ Проблемы со здоровьем: {data.get('health')}\n"
        f"5️⃣ Хочет на наставничество: {data.get('want_mentorship')}\n"
        f"👤 Контакт от пользователя: {message.text}\n"
        f"🔗 Telegram: @{message.from_user.username} (ID: {message.from_user.id})"
    )
    
    # Отправляем отчет тебе в личку (без Markdown, чтобы избежать ошибок с символами)
    await message.bot.send_message(chat_id=ADMIN_CHAT_ID, text=report)

    await message.answer("Спасибо! Твои ответы успешно отправлены.", reply_markup=None)
    await state.clear()

async def main():
    bot = Bot(token=TOKEN)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())