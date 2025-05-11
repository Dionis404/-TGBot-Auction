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
    await message.answer("👋 Привет! Я где-то тебя видел! \n"
    "А точно! Ты пробегал мимо меня на плазе! \n"
    )

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
        "Привет! Тебе стало интересно чем я занимаюсь? \n"
        "Я просто уведомляю Бампкинов об аукционах \n"
        "Делаю я это только в этой группе https://t.me/URGSFL"
    )

# Команда /feedback
@router.message(Command("feedback"))
async def cmd_feedback(message: types.Message, state: FSMContext):
    # Переход в состояние ожидания отзыва
    await state.set_state(FeedbackForm.waiting_for_feedback)
    await message.answer("✉️ У вас есть что сказать? \n"
    "Буду рад передать Главному гоблину ваши пожелания."
    )

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
    await message.answer("Я передам все слово в слово.")
    await state.reset_state()  # Завершаем состояние
