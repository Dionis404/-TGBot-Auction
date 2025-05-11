import json
from datetime import datetime, timedelta
from pytz import timezone, utc
from functools import partial
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
from telegram.constants import ParseMode
from auction import config

TIMEZONE = timezone("Europe/Moscow")
scheduler = AsyncIOScheduler(timezone=utc)

bot = Bot(token=config.BOT_TOKEN)

async def send_auction_alert(auction, start_time):
    name = auction.get("wearable") or auction.get("collectible", "Неизвестный предмет")
    ingredients = auction.get("ingredients", {})
    ingredient_name = list(ingredients.keys())[0] if ingredients else "—"
    supply = auction.get("supply", "—")

    message = (
        f"\U0001F4E2 Аукцион начнётся через 5 минут!\n"
        f"Предмет: {name}\n"
        f"Ставка: {ingredient_name}\n"
        f"Саплай: {supply}\n"
        f"Удачи!"
    )

    await bot.send_message(chat_id=config.CHAT_ID, text=message, parse_mode=ParseMode.MARKDOWN)

def schedule_auctions():
    with open("auction.20250502.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for auction in data["auctions"]["auctions"]:
        timestamp = int(auction["startAt"]) // 1000
        start_time = datetime.fromtimestamp(timestamp, tz=utc)
        notify_time = start_time - timedelta(minutes=5)

        job = partial(send_auction_alert, auction=auction, start_time=start_time)
        scheduler.add_job(job, 'date', run_date=notify_time)
