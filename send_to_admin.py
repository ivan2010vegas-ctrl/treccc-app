from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import CHANNEL_MODERATION

async def send_ad_to_admin(update, context: ContextTypes.DEFAULT_TYPE, ad: dict):
    """
    Отправляет объявление в канал модерации с кнопкой "Опубликовать"
    """
    try:
        user = update.effective_user
        text = (
            f"📝 Новое объявление на модерацию:\n\n"
            f"Пользователь: {user.full_name} (@{user.username})\n"
            f"ID Пользователя: {user.id}\n"
            f"Название: {ad['name']}\n"
            f"Цена: {ad['price']}\n"
            f"Страна: {ad['country']}\n"
            f"Доставка: {ad['delivery']}"
        )

        # Мы передаем ТОЛЬКО ID пользователя, чтобы не превысить лимит в 64 байта.
        # Данные будем брать из словаря ads по этому ID.
        keyboard = [
    [InlineKeyboardButton("Опубликовать ✅", callback_data=f"pub_{user.id}")],
    [
        InlineKeyboardButton("❌ Спам", callback_data=f"rej_{user.id}_spam"),
        InlineKeyboardButton("❌ Фото", callback_data=f"rej_{user.id}_photo"),
        InlineKeyboardButton("❌ Цена", callback_data=f"rej_{user.id}_price")
    ],
    [InlineKeyboardButton("🚫 Просто отклонить", callback_data=f"rej_{user.id}_common")]
]


        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=CHANNEL_MODERATION,
            text=text,
            reply_markup=reply_markup
        )
        print(f"DEBUG: Объявление от {user.id} отправлено на модерацию")
    except Exception as e:
        print("Ошибка отправки на модерацию:", e)
