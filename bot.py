import asyncio
import logging
import json
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, 
    PreCheckoutQuery, 
    LabeledPrice, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from aiogram.types.web_app_info import WebAppInfo
from aiogram.filters import CommandStart

# ==========================================
# 1. КОНФИГУРАЦИЯ (ВСТАВЬ СВОИ ДАННЫЕ СЮДА)
# ==========================================
# Токен от BotFather (например: '7123456:AAH...')
BOT_TOKEN = "8932233031:AAFqDGA4WTC4f-wgSgYP7iloGV5Ymqxy2bc" 

# Ссылка на твой GitHub Pages (которую ты сделал в прошлом шаге)
WEB_APP_URL = "https://github.com/vladpermakov64-lang/echo-core-app.git" 

# Цена в Telegram Stars (например, 50 звезд)
STARS_PRICE = 60 
# ==========================================

# Настройка логирования для отлова ошибок
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------------------------------------------------------
# ФАЗА 1: ТОЧКА ВХОДА (Запуск бота)
# ---------------------------------------------------------
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Обрабатывает команду /start и выдает кнопку для открытия Web App"""
    
    # Создаем кнопку с привязанным Web App
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚡ Открыть ECHO CORE", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    
    welcome_text = (
        "🧬 <b>ECHO CORE | Viral Engine</b>\n\n"
        "Я анализирую идеи для контента и предсказываю удержание зрителя (Retention).\n\n"
        "Нажми кнопку ниже, чтобы запустить сканирование."
    )
    
    await message.answer(welcome_text, reply_markup=markup, parse_mode="HTML")

# ---------------------------------------------------------
# ФАЗА 2: ПРИЕМ ИДЕИ ИЗ WEB APP И "РАЗГРОМ"
# ---------------------------------------------------------
@dp.message(F.web_app_data)
async def web_app_handler(message: Message) -> None:
    """Ловит текст, который юзер ввел на черном сайте, и выдает критику"""
    try:
        # Расшифровываем JSON от сайта
        data = json.loads(message.web_app_data.data)
        user_idea = data.get('user_idea', 'Нет идеи')
        
        # Симуляция работы ИИ (генерируем низкий балл для создания боли)
        fake_score = random.randint(12, 34)
        
        critique_text = (
            f"❌ <b>Анализ завершен.</b>\n\n"
            f"<b>Твоя идея:</b> <i>{user_idea}</i>\n\n"
            f"📉 <b>Прогноз удержания (Retention):</b> {fake_score}%\n\n"
            f"<b>Вердикт ИИ:</b> Идея слабая. Зритель свайпнет на 3-й секунде. "
            f"Не хватает визуального хука и дофаминового триггера в начале. "
            f"С таким сценарием алгоритм не даст тебе охватов."
        )
        
        # Отправляем критику
        await message.answer(critique_text, parse_mode="HTML")
        
        # Сразу после критики выставляем счет (ПЕЙВОЛЛ)
        prices = [LabeledPrice(label="Elite-Сценарий (99% Удержания)", amount=STARS_PRICE)]
        
        await bot.send_invoice(
            chat_id=message.chat.id,
            title="Генерация Elite-Сценария",
            description="ИИ полностью перепишет твою идею, добавив психологические триггеры и жесткую структуру удержания.",
            payload="elite_generation_payload",
            provider_token="", # Оставляем пустым! Для Telegram Stars токен не нужен!
            currency="XTR",    # XTR - это официальный код валюты Telegram Stars
            prices=prices
        )
        
    except Exception as e:
        logging.error(f"Ошибка парсинга Web App Data: {e}")

# ---------------------------------------------------------
# ФАЗА 3: ОБРАБОТКА ТРАНЗАКЦИИ (Telegram требует подтверждения за 10 сек)
# ---------------------------------------------------------
@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery) -> None:
    """Подтверждает телеграму, что мы готовы принять платеж"""
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# ---------------------------------------------------------
# ФАЗА 4: УСПЕШНАЯ ОПЛАТА И ВЫДАЧА РЕЗУЛЬТАТА
# ---------------------------------------------------------
@dp.message(F.successful_payment)
async def successful_payment_handler(message: Message) -> None:
    """Срабатывает мгновенно, когда юзер оплатил Stars"""
    
    # Симуляция выдачи дорогого результата
    success_text = (
        "💎 <b>Оплата подтверждена. Генерация Elite-Сценария:</b>\n\n"
        "<b>[ХУК - 0-3 сек]:</b> Быстрый зум. Ты смотришь прямо в камеру и говоришь: "
        "«Я потратил 3 года, чтобы понять одну ошибку, из-за которой ваши ролики набирают 0 просмотров...»\n\n"
        "<b>[УДЕРЖАНИЕ - 3-10 сек]:</b> На фоне резкая смена кадра (B-Roll). Ты показываешь "
        "падающий график аналитики. Говоришь: «Дело не в свете и не в монтаже. Дело в...»\n\n"
        "<b>[КУЛЬМИНАЦИЯ]:</b> ...\n\n"
        "<i>// В следующей версии здесь будет реальный ответ от Groq API //</i>"
    )
    
    await message.answer(success_text, parse_mode="HTML")

# ==========================================
# ЗАПУСК МОНОЛИТА
# ==========================================
async def main() -> None:
    logging.info("Система ECHO CORE запущена. Ожидание юзеров...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())