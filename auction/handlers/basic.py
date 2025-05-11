from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from auction import config
import logging

router = Router()

# Определение состояний для сбора отзыва
class FeedbackForm(StatesGroup):
    waiting_for_feedback = State()

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Привет! Я бот, который будет напоминать о начале аукционов.")

# Команда /help
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📌 Список доступных команд:\n"
        "/start — Приветствие\n"
        "/help — Справка\n"
        "/info — О боте\n"
        "/feedback — Оставить отзыв"
    )

# Команда /info
@router.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(
        "ℹ️ Этот бот создан для демонстрации универсальной структуры.\n"
        "В будущем он может быть расширен для выполнения конкретных задач."
    )

# Команда /feedback
@router.message(Command("feedback"))
async def cmd_feedback(message: types.Message, state: FSMContext):
    # Переход в состояние ожидания отзыва
    await state.set_state(FeedbackForm.waiting_for_feedback)
    await message.answer("✉️ Напишите сюда свой отзыв:")

# Обработка отзыва
@router.message(FeedbackForm.waiting_for_feedback)
async def process_feedback(message: types.Message, state: FSMContext):
    feedback_text = message.text
    logging.info(
        feedback_text,
        extra={
            'username': message.from_user.username or "Без username",
            'user_id': message.from_user.id
        }
    )
    await message.answer("✅ Спасибо! Твой отзыв сохранён.")
    await state.reset_state()  # Завершаем состояние
