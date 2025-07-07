import telebot

# === Bot token ===
BOT_TOKEN = '8186601135:AAFt6yPShtqe89YSF1oowsLZuvZRYIYguUI'
bot = telebot.TeleBot(BOT_TOKEN)

# === Admin ID ===
ADMIN_ID = 5091776192

# === Kanal usernamelari ===
KANALLAR = ['@Daqiqauzb24', '@TarjimaKinoPlusbot']

# === Kinolar bazasi ===
KINOLAR = {
    "1": {
        "file_id": "VIDEO_FILE_ID_1",
        "nomi": "Ultrabinavsha",
        "yili": "2006"
    },
    "9": {
        "file_id": "VIDEO_FILE_ID_2",
        "nomi": "Batman",
        "yili": "2023"
    }
}

# === Foydalanuvchilarni kuzatish uchun to‘plam ===
foydalanuvchilar = set()

# === Obuna tekshiruvchi funksiya ===
def obuna_tekshir(user_id):
    for kanal in KANALLAR:
        try:
            member = bot.get_chat_member(kanal, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except:
            return False
    return True

# === /start komandasi ===
@bot.message_handler(commands=['start'])
def boshlash(message):
    foydalanuvchilar.add(message.from_user.id)
    bot.send_message(message.chat.id, "🎬 Kino kodini kiriting (masalan: 1, 9):")

# === Kod yuborilganda ishlovchi funksiya ===
@bot.message_handler(func=lambda m: m.text.isdigit())
def kino_ber(message):
    user_id = message.from_user.id
    kod = message.text.strip()

    foydalanuvchilar.add(user_id)

    if not obuna_tekshir(user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        for kanal in KANALLAR:
            markup.add(telebot.types.InlineKeyboardButton("➕ Obuna bo‘lish", url=f"https://t.me/{kanal.strip('@')}"))
        markup.add(telebot.types.InlineKeyboardButton("✅ Tekshirish", callback_data='check_sub'))
        bot.send_message(message.chat.id, "📛 Iltimos, quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)
        return

    if kod in KINOLAR:
        kino = KINOLAR[kod]
        bot.send_video(message.chat.id, kino["file_id"], caption=f"🎬 {kino['nomi']}\n📅 {kino['yili']}")
    else:
        bot.send_message(message.chat.id, "❌ Bunday koddagi kino topilmadi.")

# === Obunani qayta tekshiruvchi tugma ===
@bot.callback_query_handler(func=lambda call: call.data == 'check_sub')
def tekshir_callback(call):
    user_id = call.from_user.id
    if obuna_tekshir(user_id):
        bot.answer_callback_query(call.id, "✅ Obuna tasdiqlandi.")
        bot.send_message(call.message.chat.id, "✅ Endi kino kodini kiriting:")
    else:
        bot.answer_callback_query(call.id, "❌ Hali obuna bo‘lmagansiz.")

# === Faqat admin fayl ID olishi mumkin ===
@bot.message_handler(content_types=['video'])
def video_qabul(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, f"📽 file_id: `{message.video.file_id}`", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ Kechirasiz, faqat admin fayl ID olishi mumkin.")

# === Statistika komandasi (faqat admin uchun) ===
@bot.message_handler(commands=['stat'])
def statistika(message):
    if message.from_user.id == ADMIN_ID:
        foydalanuvchilar_soni = len(foydalanuvchilar)
        bot.send_message(message.chat.id, f"📊 Foydalanuvchilar soni: {foydalanuvchilar_soni} ta")
    else:
        bot.send_message(message.chat.id, "❌ Bu buyruq faqat admin uchun.")

# === Botni ishga tushurish ===
bot.polling()