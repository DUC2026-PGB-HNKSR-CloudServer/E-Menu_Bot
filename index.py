import telebot
from telebot import types
import random
import json
import os
import time
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from supabase import create_client, Client

# ===================== CONFIGURATION & SECURITY =====================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ===================== SUPABASE CONNECTION =====================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

bot = telebot.TeleBot(BOT_TOKEN)

user_cart = {}
user_data = {}
user_lang = {}

# ===================== MULTI-LANGUAGE SYSTEM =====================
LANG = {
    "km": {
        "btn_menu": "🛒 ម៉ឺនុយមុខម្ហូប",
        "btn_cart": "📦 កន្ត្រករបស់ខ្ញុំ",
        "btn_checkout": "✅ បញ្ជាទិញ",
        "btn_clear": "🗑 លុបកន្ត្រក",
        "btn_history": "📜 ប្រវត្តិការកុម្ម៉ង់",
        "btn_call": "🛎 ហៅអ្នករត់តុ",
        "btn_bill": "🧾 សុំគិតលុយ",
        "welcome": "👋 ស្វាគមន៍មកកាន់ E-Menu Bot 🍔\n\n\u3000\u3000\u3000សូមជ្រើសរើសប៊ូតុងខាងក្រោម 👇",
        "menu_title": "📋 *ជ្រើសរើសប្រភេទអាហារ*",
        "empty_cart": "🛒 កន្ត្រករបស់អ្នកទទេ! សូមទៅកាន់ម៉ឺនុយដើម្បីកុម្ម៉ង់។",
        "cart_title": "🛒 *ទំនិញក្នុងកន្ត្រករបស់អ្នក:*\n\n",
        "total": "សរុប",
        "add_to_cart": "🛒 បញ្ចូលទៅកន្ត្រក",
        "back": "🔙 ត្រលប់ក្រោយ",
        "price": "តម្លៃ",
        "qty": "ចំនួន",
        "ask_phone": "📱 សូមបញ្ចូល *លេខទូរស័ព្ទ* របស់អ្នក:",
        "ask_table": "🔢 សូមបញ្ចូល *លេខតុ* របស់អ្នក (ឧទាហរណ៍៖ តុលេខ 5):",
        "invoice_title": "🎉 *ការកុម្ម៉ង់ត្រូវបានទទួលជោគជ័យ!*\n\n*🧾 វិក័យបត្រលេខ:*",
        "wait_msg": "_(👨‍🍳 សូមរង់ចាំអាហារបន្តិច...)_",
        "no_history": "អ្នកមិនទាន់មានប្រវត្តិការកុម្ម៉ង់នៅឡើយទេ។",
        "history_title": "📜 *ប្រវត្តិការកុម្ម៉ង់ចុងក្រោយរបស់អ្នក៖*",
        "invoice_no": "វិក័យបត្រលេខ",
        "date": "កាលបរិច្ឆេទ",
        "table_no": "លេខតុ",
        "status": "ស្ថានភាព",
        "reorder_btn": "♻️ កុម្ម៉ង់របស់នេះម្ដងទៀត",
        "service_title": "🛎 *តើលោកអ្នកត្រូវការសេវាកម្មអ្វីដែរ?*",
        "ice": "🧊 សុំទឹកកក",
        "tissue": "🧻 សុំក្រដាស",
        "staff": "👨‍🍳 ហៅបុគ្គលិក",
        "cancel": "❌ បោះបង់",
        "req_sent": "✅ បានផ្ញើសំណើជូនបុគ្គលិកហើយ!",
        "bill_sent": "✅ បុគ្គលិកកំពុងរៀបចំវិក័យបត្រជូនលោកអ្នក!"
    },
    "en": {
        "btn_menu": "🛒 Menu",
        "btn_cart": "📦 My Cart",
        "btn_checkout": "✅ Checkout",
        "btn_clear": "🗑 Clear Cart",
        "btn_history": "📜 Order History",
        "btn_call": "🛎 Call Staff",
        "btn_bill": "🧾 Request Bill",
        "welcome": "👋 Welcome to E-Menu Bot 🍔\n\n\u3000\u3000\u3000Please select an option below 👇",
        "menu_title": "📋 *Select a Category*",
        "empty_cart": "🛒 Your cart is empty! Please go to Menu.",
        "cart_title": "🛒 *Items in your Cart:*\n\n",
        "total": "Total",
        "add_to_cart": "🛒 Add to Cart",
        "back": "🔙 Back",
        "price": "Price",
        "qty": "Qty",
        "ask_phone": "📱 Please enter your *Phone Number*:",
        "ask_table": "🔢 Please enter your *Table Number* (e.g., 5):",
        "invoice_title": "🎉 *Order Placed Successfully!*\n\n*🧾 Invoice No:*",
        "wait_msg": "_(👨‍🍳 Please wait for your food...)_",
        "no_history": "You have no order history yet.",
        "history_title": "📜 *Your Recent Orders:*",
        "invoice_no": "Invoice No",
        "date": "Date",
        "table_no": "Table",
        "status": "Status",
        "reorder_btn": "♻️ Reorder this",
        "service_title": "🛎 *What service do you need?*",
        "ice": "🧊 Ice",
        "tissue": "🧻 Tissue",
        "staff": "👨‍🍳 Call Staff",
        "cancel": "❌ Cancel",
        "req_sent": "✅ Request sent to staff!",
        "bill_sent": "✅ Staff is preparing your bill!"
    }
}

def get_lang(user_id):
    return user_lang.get(user_id, "km")

def get_main_markup(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    t = LANG[lang]
    markup.add(t['btn_menu'], t['btn_cart'])
    markup.add(t['btn_checkout'], t['btn_clear'])
    markup.add(t['btn_history'])
    markup.add(t['btn_call'], t['btn_bill'])
    return markup

def _t(user_id, key):
    return LANG[get_lang(user_id)].get(key, key)

# ===================== ADMIN BROADCAST =====================
@bot.message_handler(commands=['broadcast'])
def broadcast_start(message):
    if message.chat.id != ADMIN_ID:
        return bot.send_message(message.chat.id, "⚠️ អ្នកមិនមានសិទ្ធិប្រើប្រាស់មុខងារនេះទេ។")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('❌ បោះបង់ (Cancel)')
    
    msg = bot.send_message(ADMIN_ID, "📢 *មុខងារផ្ញើសារប្រូម៉ូសិន (Broadcast)*\n\nសូមវាយសារ ឬផ្ញើរូបភាព/វីដេអូ ដែលអ្នកចង់ផ្ញើទៅកាន់អតិថិជនទាំងអស់៖", reply_markup=markup, parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    lang = get_lang(ADMIN_ID)
    if message.text == '❌ បោះបង់ (Cancel)':
        return bot.send_message(ADMIN_ID, "❌ ការផ្ញើសារប្រូម៉ូសិនត្រូវបានបោះបង់។", reply_markup=get_main_markup(lang))

    bot.send_message(ADMIN_ID, "⏳ កំពុងដំណើរការផ្ញើសារ... សូមរង់ចាំបន្តិច។")
    
    try:
        response = supabase.table("all_users").select("user_id").execute()
        users = response.data
        
        success = 0
        failed = 0
        
        for user in users:
            uid = user['user_id']
            if uid == ADMIN_ID: continue
            try:
                bot.copy_message(chat_id=uid, from_chat_id=ADMIN_ID, message_id=message.message_id)
                success += 1
            except Exception:
                failed += 1 
                
        bot.send_message(ADMIN_ID, f"✅ *ការផ្ញើសារប្រូម៉ូសិនបានបញ្ចប់!*\n\nជោគជ័យ: {success} នាក់\nបរាជ័យ: {failed} នាក់", reply_markup=get_main_markup(lang), parse_mode="Markdown")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"⚠️ មានបញ្ហាក្នុងប្រព័ន្ធ Database: {e}")

# ===================== ADMIN DAILY REPORT =====================
@bot.message_handler(commands=['report'])
def generate_daily_report(message):
    if message.chat.id != ADMIN_ID:
        return bot.send_message(message.chat.id, "⚠️ អ្នកមិនមានសិទ្ធិប្រើប្រាស់មុខងារនេះទេ។")

    cambodia_time = datetime.now(timezone.utc) + timedelta(hours=7)
    today_str = cambodia_time.strftime('%Y-%m-%d')
    start_of_day = f"{today_str}T00:00:00+07:00"
    
    bot.send_message(ADMIN_ID, "⏳ កំពុងទាញយករបាយការណ៍លក់ថ្ងៃនេះ...")

    try:
        response = supabase.table("orders_history").select("*").gte("created_at", start_of_day).execute()
        orders = response.data

        total_orders = len([o for o in orders if o['status'] != 'Rejected'])
        total_revenue = sum(o['total_price'] for o in orders if o['status'] in ['Accepted', 'Serving'])
        
        item_counts = {}
        for o in orders:
            if o['status'] in ['Accepted', 'Serving']:
                items = o['items']
                if isinstance(items, str):
                    items = json.loads(items)
                for item in items:
                    name = item['item_name']
                    item_counts[name] = item_counts.get(name, 0) + 1
                    
        top_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        report_text = f"📊 *របាយការណ៍លក់ប្រចាំថ្ងៃ ({today_str})*\n\n"
        report_text += f"📦 ចំនួនកុម្ម៉ង់សរុប: *{total_orders} វិក័យបត្រ*\n"
        report_text += f"💰 ចំណូលសរុប: *${total_revenue:.2f}*\n\n"
        
        if top_items:
            report_text += "🏆 *មុខម្ហូបលក់ដាច់ជាងគេ (Top 5):*\n"
            for name, qty in top_items:
                report_text += f"• {name}: {qty} ដង\n"
        else:
            report_text += "គ្មានទិន្នន័យមុខម្ហូបដែលបានលក់នៅថ្ងៃនេះទេ។"
                
        bot.send_message(ADMIN_ID, report_text, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"⚠️ មានបញ្ហាក្នុងការទាញយករបាយការណ៍: {e}")

# ===================== START & LANGUAGE =====================
@bot.message_handler(commands=['start', 'lang', 'language'])
def start_and_lang(message):
    user_id = message.chat.id
    text_parts = message.text.split()
    qr_table = None
    
    if len(text_parts) > 1 and text_parts[0] == '/start':
        qr_table = text_parts[1]

    try:
        supabase.table("all_users").upsert({"user_id": user_id}).execute()
        res = supabase.table("users_profile").select("*").eq("user_id", user_id).execute()
        if res.data:
            user_lang[user_id] = res.data[0].get('language', 'km')
            if qr_table:
                supabase.table("users_profile").update({"table_number": qr_table}).eq("user_id", user_id).execute()
        else:
            supabase.table("users_profile").insert({"user_id": user_id, "phone": "N/A", "table_number": qr_table, "language": "km"}).execute()
            user_lang[user_id] = "km"
            
        if qr_table:
            bot.send_message(user_id, f"✅ បានស្កេន QR Code! / QR Code Scanned!\nតុលេខ / Table: *{qr_table}*", parse_mode="Markdown")
    except Exception:
        pass

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🇰🇭 ភាសាខ្មែរ", callback_data="setlang_km"),
        types.InlineKeyboardButton("🇬🇧 English", callback_data="setlang_en")
    )
    bot.send_message(user_id, "សូមជ្រើសរើសភាសា / Please select your language:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('setlang_'))
def handle_language_selection(call):
    try: bot.answer_callback_query(call.id)
    except: pass
    user_id = call.message.chat.id
    selected_lang = call.data.split('_')[1]
    user_lang[user_id] = selected_lang
    
    try: supabase.table("users_profile").update({"language": selected_lang}).eq("user_id", user_id).execute()
    except Exception: pass
        
    try: bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
    except Exception: pass
        
    bot.send_message(user_id, _t(user_id, 'welcome'), reply_markup=get_main_markup(selected_lang), parse_mode="Markdown")

# ===================== DYNAMIC MENU =====================
@bot.message_handler(func=lambda m: m.text in [LANG['km']['btn_menu'], LANG['en']['btn_menu']])
def show_dynamic_menu(message):
    user_id = message.chat.id
    try:
        res = supabase.table("menu_items").select("category").execute()
        categories = list(set([item['category'] for item in res.data]))
        markup = types.InlineKeyboardMarkup(row_width=2)
        for cat in sorted(categories):
            markup.add(types.InlineKeyboardButton(cat, callback_data=f"cat_{cat}"))
        bot.send_message(user_id, _t(user_id, 'menu_title'), reply_markup=markup, parse_mode="Markdown")
    except Exception:
        bot.send_message(user_id, "⚠️ Cannot load menu.")

# ===================== CART SYSTEM =====================
@bot.message_handler(func=lambda m: m.text in [LANG['km']['btn_cart'], LANG['en']['btn_cart']])
def show_cart(message):
    user_id = message.chat.id
    cart = user_cart.get(user_id, [])
    if not cart: return bot.send_message(user_id, _t(user_id, 'empty_cart'))
    
    summary = {}
    for item in cart:
        name = item['item_name']
        if name in summary:
            summary[name]['qty'] += 1
            summary[name]['total'] += item['price']
        else:
            summary[name] = {'qty': 1, 'price': item['price'], 'total': item['price']}

    text = _t(user_id, 'cart_title')
    total_all = 0
    i = 1
    for name, data in summary.items():
        text += f"{i}. {name} x{data['qty']} — ${data['total']:.2f}\n"
        total_all += data['total']
        i += 1
    text += f"\n*{_t(user_id, 'total')}: ${total_all:.2f}*"
    bot.send_message(user_id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text in [LANG['km']['btn_clear'], LANG['en']['btn_clear']])
def clear_cart(message):
    user_cart[message.chat.id] = []
    text = "🗑 ជម្រះកន្ត្រករួចរាល់!" if get_lang(message.chat.id) == 'km' else "🗑 Cart cleared successfully!"
    bot.send_message(message.chat.id, text)

# ===================== HISTORY & REORDER =====================
@bot.message_handler(func=lambda m: m.text in [LANG['km']['btn_history'], LANG['en']['btn_history']])
def show_order_history(message):
    user_id = message.chat.id
    try:
        response = supabase.table("orders_history").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(5).execute()
        orders = response.data

        if not orders: return bot.send_message(user_id, _t(user_id, 'no_history'))

        bot.send_message(user_id, _t(user_id, 'history_title'), parse_mode="Markdown")

        for order in orders:
            order_id = order['order_id']
            date_val = order['created_at']
            date_str = date_val[:16].replace('T', ' ') if isinstance(date_val, str) else "N/A"
            status = order['status']
            total = order['total_price']
            table_no = order['table_number']
            
            text = f"📦 *{_t(user_id, 'invoice_no')}:* #{order_id}\n📅 *{_t(user_id, 'date')}:* {date_str}\n🔢 *{_t(user_id, 'table_no')}:* {table_no}\n📊 *{_t(user_id, 'status')}:* {status}\n💰 *{_t(user_id, 'total')}:* ${total:.2f}\n\n"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(_t(user_id, 'reorder_btn'), callback_data=f"reorder_{order_id}"))
            bot.send_message(user_id, text, reply_markup=markup, parse_mode="Markdown")
    except Exception:
        bot.send_message(user_id, "⚠️ Error loading history.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('reorder_'))
def handle_reorder(call):
    try: bot.answer_callback_query(call.id)
    except: pass
    user_id = call.message.chat.id
    lang = get_lang(user_id)
    order_id = int(call.data.split('_')[1])
    try:
        response = supabase.table("orders_history").select("items").eq("order_id", order_id).execute()
        if response.data:
            items = response.data[0]['items']
            if isinstance(items, str): items = json.loads(items)
            if user_id not in user_cart: user_cart[user_id] = []
            user_cart[user_id].extend(items)
            
            msg = f"♻️ បានបញ្ចូលមុខម្ហូបពីវិក័យបត្រ `#{order_id}` ទៅកន្ត្រកវិញ!" if lang == 'km' else f"♻️ Re-added items from order `#{order_id}`!"
            bot.send_message(user_id, msg, parse_mode="Markdown")
        else:
            bot.send_message(user_id, "⚠️ Not found.")
    except Exception:
        pass

# ===================== CALL STAFF & BILL =====================
@bot.message_handler(func=lambda m: m.text in [LANG['km']['btn_call'], LANG['en']['btn_call']])
def call_staff(message):
    user_id = message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(_t(user_id, 'ice'), callback_data="svc_ice"),
        types.InlineKeyboardButton(_t(user_id, 'tissue'), callback_data="svc_tissue")
    )
    markup.add(
        types.InlineKeyboardButton(_t(user_id, 'staff'), callback_data="svc_staff"),
        types.InlineKeyboardButton(_t(user_id, 'cancel'), callback_data="svc_cancel")
    )
    bot.send_message(user_id, _t(user_id, 'service_title'), reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith('svc_'))
def handle_service(call):
    try: bot.answer_callback_query(call.id)
    except: pass
    user_id = call.message.chat.id
    action = call.data.split('_')[1]

    if action == 'cancel':
        try: return bot.delete_message(user_id, call.message.message_id)
        except: return
        
    svc_name = _t(user_id, action)

    try:
        res = supabase.table("users_profile").select("table_number").eq("user_id", user_id).execute()
        if res.data and res.data[0]['table_number'] and res.data[0]['table_number'] != "N/A":
            t_num = res.data[0]['table_number']
            bot.send_message(ADMIN_ID, f"🛎 *សេវាកម្មតុ:* តុលេខ `{t_num}`\nកំពុងសុំ: *{svc_name}*", parse_mode="Markdown")
            try: bot.edit_message_text(_t(user_id, 'req_sent'), chat_id=user_id, message_id=call.message.message_id)
            except: pass
        else:
            try: bot.delete_message(user_id, call.message.message_id)
            except: pass
            msg = bot.send_message(user_id, _t(user_id, 'ask_table'), parse_mode="Markdown")
            bot.register_next_step_handler(msg, process_service_table, svc_name)
    except Exception:
        pass

def process_service_table(message, svc_name):
    user_id = message.chat.id
    t_num = message.text
    bot.send_message(ADMIN_ID, f"🛎 *សេវាកម្មតុ:* តុលេខ `{t_num}`\nកំពុងសុំ: *{svc_name}*", parse_mode="Markdown")
    bot.send_message(user_id, _t(user_id, 'req_sent'))

@bot.message_handler(func=lambda m: m.text in [LANG['km']['btn_bill'], LANG['en']['btn_bill']])
def request_bill(message):
    user_id = message.chat.id
    try:
        res = supabase.table("users_profile").select("table_number").eq("user_id", user_id).execute()
        if res.data and res.data[0]['table_number'] and res.data[0]['table_number'] != "N/A":
            t_num = res.data[0]['table_number']
            bot.send_message(ADMIN_ID, f"🧾 *សុំគិតលុយ:* តុលេខ `{t_num}` កំពុងសុំគិតលុយ។", parse_mode="Markdown")
            bot.send_message(user_id, _t(user_id, 'bill_sent'))
        else:
            msg = bot.send_message(user_id, _t(user_id, 'ask_table'), parse_mode="Markdown")
            bot.register_next_step_handler(msg, process_bill_table)
    except Exception:
        pass

def process_bill_table(message):
    user_id = message.chat.id
    t_num = message.text
    bot.send_message(ADMIN_ID, f"🧾 *សុំគិតលុយ:* តុលេខ `{t_num}` កំពុងសុំគិតលុយ។", parse_mode="Markdown")
    bot.send_message(user_id, _t(user_id, 'bill_sent'))

# ===================== INLINE MENU LOGIC =====================
@bot.callback_query_handler(func=lambda call: call.data.startswith('cat_') or call.data.startswith('add_') or call.data.startswith('qty_') or call.data == "back_menu" or call.data == "ignore")
def handle_menu_callback(call):
    try: bot.answer_callback_query(call.id)
    except: pass
    user_id = call.message.chat.id
    lang = get_lang(user_id)
    
    try:
        if call.data == "ignore": return

        elif call.data.startswith('cat_'):
            category = call.data[4:]
            res = supabase.table("menu_items").select("*").eq("category", category).execute()
            items = res.data
            markup = types.InlineKeyboardMarkup(row_width=1)
            for item in items:
                name = item['name_km'] if lang == 'km' else item['name_en']
                markup.add(types.InlineKeyboardButton(f"🍽 {name} — ${item['price']:.2f}", callback_data=f"add_{item['id']}"))
            markup.add(types.InlineKeyboardButton(_t(user_id, 'back'), callback_data="back_menu"))
            try: bot.edit_message_text(f"*{category}*", chat_id=user_id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            except: pass

        elif call.data.startswith('add_'):
            item_id = int(call.data.split('_')[1])
            res = supabase.table("menu_items").select("*").eq("id", item_id).execute()
            if not res.data: return
            item = res.data[0]
            name = item['name_km'] if lang == 'km' else item['name_en']
            
            user_data[user_id] = {
                "item_id": item['id'], "item_name": name, "price": item['price'], 
                "qty": 1, "photo": item['photo_url'], "cat": item['category']
            }
            markup = types.InlineKeyboardMarkup(row_width=3)
            markup.add(
                types.InlineKeyboardButton("➖", callback_data="qty_minus"),
                types.InlineKeyboardButton("1", callback_data="ignore"),
                types.InlineKeyboardButton("➕", callback_data="qty_plus")
            )
            markup.add(types.InlineKeyboardButton(_t(user_id, 'add_to_cart'), callback_data="qty_confirm"))
            markup.add(types.InlineKeyboardButton(_t(user_id, 'back'), callback_data=f"cat_{item['category']}"))
            
            try: bot.send_photo(user_id, item['photo_url'], caption=f"*{name}*\n{_t(user_id, 'price')}: ${item['price']:.2f}\n\n*{_t(user_id, 'qty')}:* 👇", reply_markup=markup, parse_mode="Markdown")
            except Exception: bot.send_message(user_id, f"🍽 *{name}*\n{_t(user_id, 'price')}: ${item['price']:.2f}\n\n*{_t(user_id, 'qty')}:* 👇", reply_markup=markup, parse_mode="Markdown")

        elif call.data in ['qty_minus', 'qty_plus']:
            temp = user_data.get(user_id)
            if not temp: return
            if call.data == 'qty_minus' and temp['qty'] > 1: temp['qty'] -= 1
            elif call.data == 'qty_plus' and temp['qty'] < 20: temp['qty'] += 1
            markup = types.InlineKeyboardMarkup(row_width=3)
            markup.add(
                types.InlineKeyboardButton("➖", callback_data="qty_minus"),
                types.InlineKeyboardButton(str(temp['qty']), callback_data="ignore"),
                types.InlineKeyboardButton("➕", callback_data="qty_plus")
            )
            markup.add(types.InlineKeyboardButton(_t(user_id, 'add_to_cart'), callback_data="qty_confirm"))
            markup.add(types.InlineKeyboardButton(_t(user_id, 'back'), callback_data=f"cat_{temp['cat']}"))
            try: bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            except: pass

        elif call.data == 'qty_confirm':
            temp = user_data.get(user_id)
            if temp:
                if user_id not in user_cart: user_cart[user_id] = []
                for _ in range(temp['qty']): user_cart[user_id].append({"item_id": temp["item_id"], "item_name": temp["item_name"], "price": temp["price"]})
                try: bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
                except: pass
                msg = f"✅ បានបញ្ចូល {temp['qty']}x {temp['item_name']} ទៅក្នុងកន្ត្រក!" if lang == 'km' else f"✅ Added {temp['qty']}x {temp['item_name']} to Cart!"
                bot.send_message(user_id, msg)
                del user_data[user_id]

        elif call.data == "back_menu":
            try: bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            except: pass
            class FakeMsg: chat = type('Chat', (), {'id': user_id})()
            show_dynamic_menu(FakeMsg())
    except Exception:
        pass

# ===================== CHECKOUT FLOW (FORCE TABLE) =====================
@bot.message_handler(func=lambda m: m.text in [LANG['km']['btn_checkout'], LANG['en']['btn_checkout']])
def checkout(message):
    user_id = message.chat.id
    lang = get_lang(user_id)
    if not user_cart.get(user_id): return bot.send_message(user_id, _t(user_id, 'empty_cart'))
    user_data[user_id] = {} 
    
    try:
        response = supabase.table("users_profile").select("phone").eq("user_id", user_id).execute()
        if response.data and response.data[0].get('phone') and response.data[0]['phone'] != "N/A":
            profile = response.data[0]
            user_data[user_id]['saved_phone'] = profile['phone']
            
            text = f"📞 លេខចាស់: `{profile['phone']}`\nចង់ប្រើលេខនេះឬបញ្ចូលថ្មី?" if lang == 'km' else f"📞 Saved phone: `{profile['phone']}`\nUse this or enter new?"
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("✅ ប្រើលេខចាស់ / Use Old", callback_data="profile_old"),
                types.InlineKeyboardButton("📝 បញ្ចូលថ្មី / New", callback_data="profile_new")
            )
            bot.send_message(user_id, text, reply_markup=markup, parse_mode="Markdown")
        else:
            msg = bot.send_message(user_id, _t(user_id, 'ask_phone'), parse_mode="Markdown")
            bot.register_next_step_handler(msg, process_phone_step)
    except Exception:
        msg = bot.send_message(user_id, _t(user_id, 'ask_phone'), parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_phone_step)

@bot.callback_query_handler(func=lambda call: call.data.startswith('profile_'))
def handle_profile_choice(call):
    try: bot.answer_callback_query(call.id)
    except: pass
    user_id = call.message.chat.id
    choice = call.data.split('_')[1]

    if choice == "old":
        user_data[user_id]['phone'] = user_data[user_id].get('saved_phone', 'N/A')
        try: bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        except: pass
        msg = bot.send_message(user_id, _t(user_id, 'ask_table'), parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_table_step)

    elif choice == "new":
        try: bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        except: pass
        msg = bot.send_message(user_id, _t(user_id, 'ask_phone'), parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_phone_step)

def process_phone_step(message):
    user_id = message.chat.id
    user_data[user_id]["phone"] = message.text
    msg = bot.send_message(user_id, _t(user_id, 'ask_table'), parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_table_step)

def process_table_step(message):
    user_id = message.chat.id
    user_data[user_id]["table"] = message.text
    try: supabase.table("users_profile").upsert({"user_id": user_id, "phone": user_data[user_id]["phone"], "table_number": user_data[user_id]["table"]}).execute()
    except Exception: pass
    complete_order(message, user_id)

# ===================== COMPLETE ORDER =====================
def complete_order(message, user_id):
    cart = user_cart.get(user_id, [])
    info = user_data.get(user_id, {})
    
    order_id = random.randint(10000, 99999)
    total = sum(item['price'] for item in cart)
    
    summary = {}
    for item in cart:
        name = item['item_name']
        if name in summary:
            summary[name]['qty'] += 1
            summary[name]['total'] += item['price']
        else:
            summary[name] = {'qty': 1, 'price': item['price'], 'total': item['price']}

    cambodia_time = datetime.now(timezone.utc) + timedelta(hours=7)
    time_str = cambodia_time.strftime('%Y-%m-%dT%H:%M:%S+07:00')

    try:
        supabase.table("orders_history").insert({
            "order_id": order_id, "user_id": user_id, "customer_phone": info.get("phone", "N/A"),
            "table_number": info.get("table", "N/A"), "items": cart, "total_price": total,
            "dining_type": "Dine-in", "payment_method": "Pay at Cashier", "status": "Pending", "created_at": time_str
        }).execute()
    except Exception:
        pass
    
    text = f"{_t(user_id, 'invoice_title')} #{order_id}\n📞 {_t(user_id, 'ask_phone').replace('*','').split(' ')[-1]} {info.get('phone', 'N/A')}\n🔢 {_t(user_id, 'ask_table').replace('*','').split(' ')[-1]} {info.get('table', 'N/A')}\n\n"
    for name, data in summary.items():
        text += f"• {name} x{data['qty']} — ${data['total']:.2f}\n"
    text += f"\n*{_t(user_id, 'total')}: ${total:.2f}*\n\n{_t(user_id, 'wait_msg')}"
    bot.send_message(user_id, text, parse_mode="Markdown")
    
    admin_text = f"🛎 *កុម្ម៉ង់ថ្មី! #{order_id}*\n\nអតិថិជន: {user_id}\nទូរស័ព្ទ: {info.get('phone', 'N/A')}\n🔢 លេខតុ: *{info.get('table', 'N/A')}*\nTotal: ${total:.2f}"
    admin_markup = types.InlineKeyboardMarkup(row_width=2)
    admin_markup.add(
        types.InlineKeyboardButton("✅ ទទួលយក", callback_data=f"adm_acc_{order_id}_{user_id}"),
        types.InlineKeyboardButton("❌ បដិសេធ", callback_data=f"adm_rej_{order_id}_{user_id}")
    )
    admin_markup.add(types.InlineKeyboardButton("🍽 កំពុងយកទៅតុ", callback_data=f"adm_del_{order_id}_{user_id}"))
    try: bot.send_message(ADMIN_ID, admin_text, reply_markup=admin_markup, parse_mode="Markdown")
    except: pass
    
    user_cart[user_id] = []
    if user_id in user_data: del user_data[user_id]

# ===================== ADMIN ORDER MANAGEMENT =====================
@bot.callback_query_handler(func=lambda call: call.data.startswith('adm_'))
def handle_admin_actions(call):
    try: bot.answer_callback_query(call.id)
    except: pass
    
    parts = call.data.split('_')
    action = parts[1]
    order_id = int(parts[2])
    customer_id = int(parts[3])
    
    new_status = ""
    customer_message = ""
    
    if action == "acc":
        new_status = "Accepted"
        customer_message = f"✅ សួស្ដី! ការកុម្ម៉ង់លេខ *#{order_id}* ត្រូវបានហាង *ទទួលយក* ហើយ។ អាហារកំពុងរៀបចំចំអិន! 👨‍🍳"
    elif action == "rej":
        new_status = "Rejected"
        customer_message = f"❌ សុំទោស! ការកុម្ម៉ង់លេខ *#{order_id}* ត្រូវបានហាង *បដិសេធ* (អាចដោយសារអស់ស្តុក)។"
    elif action == "del":
        new_status = "Serving"
        customer_message = f"🍽 ការកុម្ម៉ង់លេខ *#{order_id}* របស់អ្នកកំពុង *រៀបចំយកទៅតុ* ហើយ! សូមរង់ចាំបន្តិច។"

    try: supabase.table("orders_history").update({"status": new_status}).eq("order_id", order_id).execute()
    except Exception: pass

    try: bot.send_message(customer_id, customer_message, parse_mode="Markdown")
    except Exception: pass

    try: bot.edit_message_text(f"ការកុម្ម៉ង់ #{order_id}\nស្ថានភាព: *{new_status}*", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")
    except Exception: pass

# ===================== RUN BOT & SET COMMANDS =====================
if __name__ == "__main__":
    print("🤖 Bot កំពុងដំណើរការ... 🚀")
    
    try:
        bot.delete_my_commands(scope=None, language_code=None)
        bot.set_my_commands(
            [types.BotCommand("start", "ចាប់ផ្តើម និងបើកផ្ទាំងកុម្ម៉ង់អាហារ")],
            scope=types.BotCommandScopeDefault()
        )
        bot.set_my_commands(
            [
                types.BotCommand("start", "ចាប់ផ្តើម និងបើកផ្ទាំងកុម្ម៉ង់អាហារ"),
                types.BotCommand("broadcast", "ផ្ញើសារប្រូម៉ូសិន (សម្រាប់តែ Admin)"),
                types.BotCommand("report", "របាយការណ៍លក់ប្រចាំថ្ងៃ (សម្រាប់តែ Admin)")
            ],
            scope=types.BotCommandScopeChat(ADMIN_ID)
        )
        print("✅ បានកំណត់ Menu Commands រួចរាល់!")
    except Exception as e:
        pass

    while True:
        try:
            bot.delete_webhook()
            bot.infinity_polling(none_stop=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            print("⚠️ ដាច់ការតភ្ជាប់ពី Telegram... កំពុងភ្ជាប់ឡើងវិញក្នុងពេល ៥ វិនាទី...")
            time.sleep(5)