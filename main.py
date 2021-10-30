import os
import telebot
from telebot.types import InlineKeyboardButton
from lib import wallpaper as WP
from lib import Data, image
import time

os.system("cls")


API_KEY = os.getenv("API_KEY") if os.getenv("API_KEY")!=None else "2068683845:AAFsB-599frUUaUj6W_aTenovaBbV-xSNX4"
bot = telebot.TeleBot(API_KEY)    
 
wallpaper = telebot.types.InlineKeyboardMarkup()
contact = telebot.types.InlineKeyboardMarkup()

WALLPAPER = {
    "Anime" : "animewallpaper",
    "Cars" : "ForzaWallpapers",
    "Games" : "gamewallpaper",
    "Random" : "wallpaper"
}

items = list(WALLPAPER.keys())

wallpaper.add(
    InlineKeyboardButton(items[0],callback_data=items[0]),
    InlineKeyboardButton(items[1],callback_data=items[1])
    )

wallpaper.add(
    InlineKeyboardButton(items[2],callback_data=items[2]),
    InlineKeyboardButton(items[3],callback_data=items[3])
    )

contact.add(InlineKeyboardButton("Contact Developer",callback_data="contact"))
contact.add(InlineKeyboardButton("Explore Wallpaper",callback_data="explore"))

def sleep(seconds: int):
    start = time.time()
    while (time.time() - start < seconds):
        pass


@bot.message_handler(commands=['start'])
def start(message):

    data = [
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    ]

    try:
        Data.import_data(data)
    except Exception as e: print(f"Error: {e}")

    msg = rf'''
    Koniciwa!, {data[2]}
Nice to meet you 😊

I'm Asuna and I will send you wallpaper as per your interest.
If you have any suggestions, please feel free to contact my developer
    '''

    bot.send_photo(message.chat.id, caption=msg, photo=open('lib\pfp.jpg','rb'), reply_markup=contact)

    data = [
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    ]

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data in WALLPAPER.keys():

        while True:
            if str(WP.wallpaper(WALLPAPER.get(call.data))) == "None":
                continue
            else:
                photo_url = str(WP.wallpaper(WALLPAPER.get(call.data)))
                break

        filename = image.download(call.message.chat.id, photo_url)
        sleep(3)

        print(filename)
        bot.send_photo(call.message.chat.id, photo=open(filename, 'rb'), reply_markup=wallpaper)
        os.remove(filename)
    
    if call.data == 'explore':
        bot.send_message(call.message.chat.id, text="I only Provide High Quality Wallpaper 😁", reply_markup=wallpaper)
    
    if call.data == 'contact':
        bot.send_message(call.message.chat.id, text="[Saikat](https://t.me/saikat0326)", parse_mode='MarkdownV2')
    
bot.polling()
