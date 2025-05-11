import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from auction import config
from auction.handlers import basic, admin  # Импорт обработчиков

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def main():
    # Зарегистрировать обработчики команд
    dp.include_router(basic.router)
    dp.include_router(admin.router)

    print("Бот запущен и ждёт сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
