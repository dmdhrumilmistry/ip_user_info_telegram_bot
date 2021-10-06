import telebot
import requests
from telebot.types import Message as tele_message

access_token = 'ipinfo.io access token'
API_KEY = 'telegram bot api key'
bot = telebot.TeleBot(API_KEY)
help_message = '''
IP User info bot 
Written by Dhrumil Mistry
https://github.com/dmdhrumilmistry

---------------------------------------
command : description
---------------------------------------
/start : get chat id and user details
/help : get help menu
/getinfo [IP] : get details of IP
'''


def get_user_details(message: tele_message):
    '''
    returns user's details as string
    '''
    return f'Details:\nID : {message.from_user.id}\nName :{message.from_user.full_name}\n[UserName] {message.from_user.username}\nIS BOT : {message.from_user.is_bot}'


def get_ip_details_str(ip_address):
    '''
    returns user details as formatted string
    '''
    details = requests.get(
        url=f"http://ipinfo.io/{ip_address}/?token={access_token}")
    if details.status_code == 200:
        details = details.json()
        formatted_details = f'{"-"*30}\nIP Details\n{"-"*30}\n'
        for key in details:
            formatted_details += f'[+] {key} : {details[key]}\n'
    elif details.status_code == 404:
        formatted_details = '[+] IP : Invalid'

    return formatted_details


@bot.message_handler(commands=['start'])
def start(message: tele_message):
    '''
    replies user with their details 
    '''
    reply_message = get_user_details(message)
    bot.reply_to(message=message, text=reply_message)


@bot.message_handler(commands=['help'])
def help(message: tele_message):
    '''
    returns help menu to the user
    '''
    bot.reply_to(message=message, text=help_message)


@bot.message_handler(commands=['getinfo'])
def get_ip_info(message: tele_message):
    '''
    get ip details
    '''
    # extract ip from the message
    ip_address = message.text.split('/getinfo')[-1].strip()

    # get ip details and reply to the user
    details = get_ip_details_str(ip_address)
    bot.reply_to(message=message, text=details)


# if no command is valid, return invalid message
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "INVALID OPTION")


def start_bot():
    '''
    starts the bot
    '''
    print('[*] Starting Bot...')
    bot.polling()
    print('[!] Bot Stopped...')


if __name__ == '__main__':
    start_bot()
