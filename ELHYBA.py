from mody import Mody
import telebot, sqlite3, time, sys
from telebot import types
from keepAlive import keep_alive
API_TOKEN = Mody.ELHYBA
bot = telebot.TeleBot(API_TOKEN)

db = sqlite3.connect("main.db", check_same_thread=False)
cr = db.cursor()

cr.execute("create table if not exists whisper (id integer, sender text, recipient text, msg text,  PRIMARY KEY('id' AUTOINCREMENT) )")

def get_len_msgWhs():
    data = cr.execute(f'select id from whisper').fetchall()
    return str(len(data))


def USI():
    data = data = cr.execute(f'select sender from whisper').fetchall()
    if data == None:
        return ""
    else:
        dt4 = []
        for uss in data:
            dt4.append(uss[0])
        return dt4

def get_content_WH_MSG( id):
    dt4 = []
    data = cr.execute(f'select sender, recipient, msg from whisper where id= {id}').fetchone()
    if data == None:
        return ''
    else:
        return [data[0], data[1], data[2], "whisper"]


def insertWhisper(sender:str, recipient:str, msg:str):
    query = f"insert into whisper ('sender', 'recipient', 'msg') values ('{sender}', '{recipient}', '{msg}')"
    cr.execute(query)
    db.commit()



@bot.inline_handler(lambda query: True)
def query_text(inline_query:types.InlineQuery):
    text = inline_query.query
    tlst = text.split(' ')
    yto = tlst[-1]
    msg = ' '.join(tlst[:-1])
    def mrk():
        mrk = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text=f"همسة سرية 🔐", callback_data=get_len_msgWhs() + " " + "whisper" + ' ' + yto.replace("@", ""))
        mrk.add(btn)
        return mrk
    if tlst[-1].startswith("@") and len(tlst) > 1:
        # print(inline_query.from_user.username)
        # print(yto.replace("@", ""))
        insertWhisper(inline_query.from_user.username, yto.replace("@", "") ,msg)
        bot.answer_inline_query(inline_query.id, [types.InlineQueryResultArticle('Name', f'هذي همسه للحلو (  {yto}  هو الي يقدر يشوفها 🧨 ) ', types.InputTextMessageContent(f'هذي همسه للحلو (  {yto}  هو الي يقدر يشوفها 🧨 ) '), reply_markup=mrk())])



@bot.callback_query_handler(func=lambda call :True)
def n__(call:types.CallbackQuery):
    data = call.data
    if len(data.split(' ')) == 3:
        packList = data.split(' ')
        recipient = packList[2]
        NumMsg =int(packList[0])
        typeWh = packList[1]
        sender = call.from_user.username
        dat = get_content_WH_MSG(NumMsg )
        # print(dat)
        if len(dat) and dat[3] == "whisper":
            if sender in [dat[0], dat[1]] :
                bot.answer_callback_query(callback_query_id=call.id, text=f'الهمسة من  {call.from_user.first_name}: { dat[2]}', show_alert=True)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='هذي مو الك يا بطل ! :(', show_alert=True)

keep_alive()
def main_loop():
    bot.infinity_polling()
    while 1:
        time.sleep(3)


if name == 'main':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)