import logging, asyncio, re, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. AYARLAR
TOKEN = '8774452779:AAG2-8zBEkcbJGcmSfNv9c6DBKNnsxE5Rig'
ADMIN_ID = 8110392783  

# GENİŞLƏNDİRİLMİŞ AĞIR SÖYÜŞ BAZASI
bad_regex = r"(sik|s1k|amk|amq|peys|göt|got|pox|fahiş|qəhb|bic|biç|oğraş|daşşaq|suka|cyka|blyat|ananivi|bacvi|cindir|anavi sikim|neslivi sikim|doganvi sikim|oluvu sikim|dirivi sikim|bicbala|gijdllax|peyser|qandom|sik babos|bayram nurlu|dava|ogras|bic|mamavi sikim|mamasi gehbe|fahişə|peysər|gijdıllaq|qancıq)"

# 2. START MENYUSU (Dizaynlı)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"🚀 **Xoş gəldin, {user.first_name}!**\n\n"
        "🛡 **Mən Qrup Keşikçisiyəm!**\n"
        "Söyüşləri, reklamları təmizləyirəm və qrupu əyləncəli edirəm.\n\n"
        "🎮 **Əyləncə Əmrləri:**\n"
        "🔹 /hack - Birini 'hack' et (reply ilə)\n"
        "🔹 /mal - Mal testi\n"
        "🔹 /sevgi - Sevgi testi (reply ilə)\n"
        "🔹 /zar - Bəxtini yoxla\n\n"
        "📊 Məlumat: /stat yazaraq qrupa bax."
    )
    keyboard = [
        [InlineKeyboardButton("📢 Kanal", url='https://t.me/nosoyusbot'), InlineKeyboardButton("👑 Sahib", url=f'tg://user?id={ADMIN_ID}')],
        [InlineKeyboardButton("➕ Məni Qrupa Əlavə Et", url=f'https://t.me/{context.bot.username}?startgroup=true')]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# 3. YENİ FUNKSİYALAR
async def sevgi_testi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user1 = update.effective_user.first_name
        user2 = update.message.reply_to_message.from_user.first_name
        faiz = random.randint(0, 100)
        await update.message.reply_text(f"❤️ {user1} və {user2} arasındakı sevgi: {faiz}% 🌹", parse_mode='Markdown')
    else:
        await update.message.reply_text("❗ Bu əmri kiməsə cavab (reply) verərək istifadə et!")

async def zar_at(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_dice(emoji="🎲")

async def hack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message.reply_to_message.from_user.first_name if update.message.reply_to_message else "Sistem"
    msg = await update.message.reply_text(f"🔍 {target} üçün terminal açılır...")
    await asyncio.sleep(1)
    await msg.edit_text("🛰️ IP ünvanı tapıldı...")
    await asyncio.sleep(1)
    await msg.edit_text("📂 Şəxsi şəkillər yüklənir... [85%]")
    await asyncio.sleep(1)
    await msg.edit_text(f"✅ {target} darmadağın edildi! 😎")

async def mal_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    faiz = random.randint(0, 100)
    await update.message.reply_text(f"🤡 Hesablamalarıma görə sən {faiz}% malsan.")

async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = await context.bot.get_chat_member_count(update.effective_chat.id)
    await update.message.reply_text(f"📊 **Qrup Statistikası:**\n\n👤 Üzv sayı: {count}\n🛡️ Bot statusu: Aktiv", parse_mode='Markdown')

# 4. SÖYÜŞ VƏ AVTO-CAVAB
async def cleaner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    msg = update.message.text.lower()

    # Söyüş qoruması
    if (re.search(bad_regex, msg) or "t.me/" in msg) and update.effective_user.id != ADMIN_ID:
        try:
            await update.message.delete()
            return
        except: pass

    # Avto-Cavablar
    if msg == "sa":
        await update.message.reply_text("Aleykum salam, xoş gəldin!")
    elif msg == "necəsən":
        await update.message.reply_text("Şükür, sən necəsən? 😊")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hack", hack))
    app.add_handler(CommandHandler("mal", mal_test))
    app.add_handler(CommandHandler("sevgi", sevgi_testi))
    app.add_handler(CommandHandler("zar", zar_at))
    app.add_handler(CommandHandler("stat", stat))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cleaner))
    print("🚀 Canavar Bot aktivdir!")
    app.run_polling()

if name == '__main__':
    main()
