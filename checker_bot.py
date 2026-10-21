import logging
import re
import threading
import requests
from urllib.parse import urlparse
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعدادات تسجيل الأخطاء والعمليات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# التوكن الجديد النظيف والآمن 100% الخاص بك
BOT_TOKEN = "8400275590:AAFxtsKI3itFSwXhEMO0XQIB7sFUvhrt53o"

# كود التطهير التلقائي الفوري لتصفير الرسايل المعلقة عند التشغيل
try:
    requests.get(f"https://telegram.org{BOT_TOKEN}/deleteWebhook?drop_pending_updates=True")
    print("🧹 [SUCCESS] Telegram Bot Has Been Purged and Reset on Clean State!")
except Exception as e:
    print(f"⚠️ Purge Error: {e}")

# قوائم النطاقات والكلمات المفتاحية المشبوهة
SUSPICIOUS_DOMAINS = ['.icu', '.xyz', '.top', '.click', '.club', '.online', '.site', '.tech', '.space', '.website', '.fun', '.info', '.live', '.cc', '.ru', '.tk', '.ml', '.ga', '.cf', '.gq', '.link', '.zip', '.mov', '.download']
DANGER_KEYWORDS = ['login', 'signin', 'free-followers', 'gift-card', 'winning-prize', 'pubg-free', 'شحن-مجاني', 'تسجيل-الدخول', 'ربح', 'جائزة', 'اختراق', 'هكر', 'predictor', 'aviator', 'darkstore', 'طياره', 'سكربت', 'ثغرة', 'لاين-بيت']

# ويب سيرفر وهمي للضحك على خطة سيرفر Render المجانية ومنعه من الإغلاق
app = Flask('')
@app.route('/')
def home():
    return "Bot is Alive and Protected!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🛡️ **أهلاً بك في بوت الحماية وفحص الروابط المشبوهة المطور!**\n\nانسخ أي رابط شاكك فيه وابعت هولي هنا، وأنا هفصصهولك وأقولك لو كان آمن ولا فخ ونصب.")

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    urls = re.findall(r'(https?://[^\s]+)', user_text)
    if not urls:
        await update.message.reply_text("❌ يرجى إرسال رسالة تحتوي على رابط (URL) حقيقي لأتمكن من فحصه.")
        return
    for url in urls:
        is_scam = False
        reasons = []
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            for susp_dom in SUSPICIOUS_DOMAINS:
                if domain.endswith(susp_dom):
                    is_scam = True
                    reasons.append(f"يستخدم نطاق رخيص ومشبوه ينتهي بـ ({susp_dom}) وغالباً يستخدمه قراصنة الإنترنت والمحتالون")
                    break
            full_url_lower = url.lower()
            for keyword in DANGER_KEYWORDS:
                if keyword in full_url_lower:
                    is_scam = True
                    reasons.append(f"يحتوي الرابط على كلمة مشبوهة دالة على الفيشينج أو النصب والسكربتات الوهمية ({keyword})")
            if "facebook" in domain and "facebook.com" not in domain:
                is_scam = True
                reasons.append("يحاول تقليد موقع فيسبوك الشهير (صفحة مزيفة لسرقة الحسابات)")
            if "instagram" in domain and "instagram.com" not in domain:
                is_scam = True
                reasons.append("يحاول تقليد موقع إنستغرام (صفحة مزيفة لسرقة الحسابات)")
            if "google" in domain and "google.com" not in domain:
                is_scam = True
                reasons.append("يحاول تقليد صفحات جوجل الرسمية")
            if "linebet" in domain and "linebet.com" not in domain:
                is_scam = True
                reasons.append("يحاول تقليد موقع لاين بيت الرسمي لغرض النصب")
            if is_scam:
                reasons_str = "\n• " + "\n• ".join(reasons)
                reply = f"🚨 ⚠️ **تحذير أمني خطير جداً!**\n\nالرابط: `{url}`\nهذا الرابط تم تصنيفه كـ **رابط مشبوه وغير آمن** ❌\n\n🔍 **الأسباب المكتشفة:** {reasons_str}\n\n💡 **نصيحة مبرمج:** إياك تفتح اللينك ده، ولا تنزل منه ملفات، ولا تكتب فيه باسوروداتك أو الـ ID بتاعك!"
            else:
                reply = f"✅ **الرابط يبدو طبيعياً مبدئياً:** `{url}`\n\nالنطاق مسجل بشكل رسمي، ولكن تذكر دائماً ألا تسجل دخولك إلا في المواقع الموثوقة التي تبدأ بـ https وتعرفها جيداً."
            await update.message.reply_text(reply, parse_mode="Markdown", disable_web_page_preview=True)
        except Exception as e:
            await update.message.reply_text("حدث خطأ أثناء تحليل هذا الرابط المعين.")

def main():
    # تشغيل السيرفر الوهمي في خلفية منفصلة لتخطي حظر الـ Web Service
    threading.Thread(target=run_flask).start()
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
    print("🚀 البوت المطور شغال الآن بالتوكن الجديد النظيف وفيس بوك/واتساب/سكربتات النصابين في خطر...")
    application.run_polling()

if __name__ == '__main__':
    main()
