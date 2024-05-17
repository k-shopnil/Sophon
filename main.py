import telebot
import wikipedia
import datetime
import requests
import json
import os
from config import *
from data import *
from math import sqrt
from dotenv import load_dotenv
from fin_se_price import get_current_stock_price
from wiki import wikiengine
from functools import wraps
from telebot.types import Message
# from telegram import Update
# from telegram.ext import CallbackContext


urlx = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
BASE_URL="http://api.openweathermap.org/data/2.5/weather?"


def config():
    load_dotenv()

config()

def ktoc(k):
    return k-273

api_keyx=os.getenv("Rapid_KEY")

headers = {
	"X-RapidAPI-Key": api_keyx,
	"X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
}
API_KEY=os.getenv("weather_token")
CITY="Dhaka"
url=BASE_URL+"q="+CITY+"&appid="+API_KEY

res=requests.get(url).json()
temp=ktoc(res['main']['temp'])
feels_like=ktoc(res['main']['feels_like'])
weather=res['weather'][0]['description']
humidity=res['main']['humidity']

bot=telebot.TeleBot(os.getenv("tele_token"))

#@bot.message_handler(commands=['mute'])
#@group_chat_only
# def mute(message: Message):
#     #Check if the user issuing the command is an administrator
#     print("Mute command recieved")
#     if is_administrator(message):
#         print("Commander is admin")
#         #Extract the user_id to be muted from the command
#         user_id = extract_user_id_from_command(message)
#         print("User ID to be muted:", user_id)
#         #Mute the user
#         print(message.chat.id)
#         bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=False)
#         bot.reply_to(message, f"User {user_id} has been muted in the group.")
#     else:
#         print("User is not an administrator.")

#Function to check if the user issuing the command is an administrator
# def is_administrator(message: Message) -> bool:

#     if message.from_user and message.chat.type == "supergroup":
#         user_id = message.from_user.id
#         chat_id = message.chat.id
#         chat_member = bot.get_chat_member(chat_id, user_id)
#         print("User status:", chat_member.status)
#         return chat_member.status in ["administrator", "creator"]
#     return False

#Function to extract the user ID from the command message
# def extract_user_id_from_command(message: Message) -> int:
#     print("Extracting user ID from command.")
#     command_parts = message.text.split()
#     print("Command parts:", command_parts)
#     if len(command_parts) >= 2:
#         username = command_parts[1].lstrip('@')
#         #Extract the username and remove '@'
#         print("Username extracted:", username)
#         chat = bot.get_chat(username)
#         user_id = chat.id
#         print(user_id)
#         return user_id
#         # chat_id = message.chat.id
#         # userx = bot.get_chat_member(chat_id, username)
#         # print("User object:", userx)
#         # user_id = userx.user.id
#         # print("User ID:", user_id)
#         try:
#             userx = bot.get_chat_member(chat_id, username)
#             print("User object:", userx)
#             user_id = userx.user.id
#             print("User ID:", user_id)
#             return user_id
#         except Exception as e:
#             print("Error:", e)
#             bot.reply_to(message, "User not found.")
#             return None
#     bot.reply_to(message, "Invalid command format. Please specify the username.")
#     return None

def group_chat_only(func):
    @wraps(func)
    def wrapper(message: Message, *args, **kwargs):
        if message.chat.type == "group" or message.chat.type == "supergroup":
            return func(message, *args, **kwargs)
        else:
            print(f"status-> {message.from_user.first_name} is denied the faculty info.")
            bot.reply_to(message, "This command is only accessible in group chats. Please join and ask through the section's group.")
    return wrapper


f = r"https://official-joke-api.appspot.com/random_ten"
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_info = bot.get_chat_member(message.chat.id, user_id)
    user_first_name = user_info.user.first_name
    print(f"status-> {user_first_name} has initiated the bot.")
    bot.reply_to(message, f"Hello {user_first_name}! I am Sophon, a Cloudbot. I'm here to offer some small help to the students of section 13. What can I assist you with today?")

@bot.message_handler(commands=['help'])
def help(message):
    print(f"status-> {message.from_user.first_name} accessed help menu.")
    bot.reply_to(message,"""Here's what I can do for you:
                 /start - Start the bot
                 /help - Get started with me
                 /compute - Perform calculations
                 /stock - Get the current stock price(use the ticker symbol after the command)
                 /classes - Get today's classes
                 /faculty - Get the contact information of the teachers
                 /weather - Get the current weather in Dhaka/BUBT
                 /support - Contact the developer
                 /about - Learn the story behind the project
                 /repo - View the source code of the project""")

@bot.message_handler(commands=['support'])
def support(message):
    print("status-> Delivering support info.")
    bot.reply_to(message, "You can contact the developer at: \n Shopnil Karmakar : shopnilkarmakar1@gmail.com \n Koushik Hasan : mdkoushikhasan709@gmail.com ")

@bot.message_handler(commands=['about'])
def about(message):
    print("status-> Delivering about info.")
    bot.reply_to(message, "This project was created by Group 4(led by Shopnil, Meghla, Koushik) as a part of their presentation on Cloud Comptuting. This mini project's sole purpose is to demonstrate the capabilities of cloud computing.")

@bot.message_handler(commands=['repo'])
def repo(message):
    print(f"status-> {message.from_user.first_name} accessed the repository.")
    bot.reply_to(message, "You can view and fork the source code of this project at: https://github.com/k-shopnil/Sophon")

@bot.message_handler(commands=['weather'])
def weather(message):
    print(f"status-> {message.from_user.first_name} requested the weather info.")
    bot.reply_to(message, f"The current temperature in Dhaka/BUBT is {temp:.0f}°C. It feels like {feels_like:.0f}°C. With a humidity of {humidity}%.")

@bot.message_handler(commands=['stock'])
def stock(message):
    # if message.chat.type == "group" or message.chat.type == "supergroup":
    #     message.txt=message.text.lower().replace(f"@{usern}", "").strip()
    print(f"status-> {message.from_user.first_name} requested the stock info.")
    try:
        ticker = message.text.split(maxsplit=1)[1]
        current_price,company_name = get_current_stock_price(ticker)
        rep=f"The current stock price for {company_name} is: ${current_price:.2f}"
        bot.reply_to(message, rep)
    except Exception as e:
        print(f"Error: {e}")
        responsex = "Sorry. You may check your input and try again. For example, type /stock AAPL to get the current stock price of Apple Inc."
        bot.reply_to(message, responsex)

@bot.message_handler(commands=['compute'])
def compute(message):
    try:
        # response = eval(message.text.strip())
        expression = message.text.split(maxsplit=1)[1]  # Extract the expression after the command
        response = eval(expression)
        # print("Expression:", expression)  Debugging statement
        print("status-> Computing the result...")
        print(f"Result: {response}")
        response = "The answer is: " + str(response)
        bot.reply_to(message, response)
    except Exception as e:
        print(f"Error: {e}")
        responsex = "Sorry. You may check your input and try again. For example, type /compute 2+2 to get the result."
        bot.reply_to(message, responsex)

# @bot.message_handler(commands=['wiki'])
# def wiki(message):
#     wikipedia.set_lang("en")
#     topic = message.text.split(maxsplit=1)[1]
#     print(topic)
#     print(wikipedia.summary("Twitter", sentences=2))
#     #print(reply)
#     bot.reply_to(message, wikipedia.summary(topic, topic))

@bot.message_handler(commands=['classes'])
@group_chat_only
def classes(message):
    now = datetime.datetime.now()
    print(f"status-> {message.from_user.first_name} requested the classes info.")
    current_day = now.strftime("%A")
    if current_day == "Sunday":
        bot.reply_to(message, sunday)

    elif current_day == "Monday":
        bot.reply_to(message, monday)

    elif current_day == "Wednesday":
        bot.reply_to(message, wednesday)

    elif current_day == "Thursday":
        bot.reply_to(message, thursday)

    else:
        bot.reply_to(message,"Hooray!! No classes today. Enjoy your day off! ")

@bot.message_handler(commands=['faculty'])
def faculty(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        print(f"status-> {message.from_user.first_name} requested the faculty info.")
        bot.reply_to(message, ess_str)
    else:
        print(f"status-> {message.from_user.first_name} is denied the faculty info.")
        bot.reply_to(message, "This command is only accessible in group chats. Please join and ask through the section's group.")

def joker():
    def jokes(f):
        data = requests.get(f)
        tt = json.loads(data.text)
        return tt
    a = jokes(f)
    return a[0]["setup"] + "\n" + a[0]["punchline"]
    # for i in (a):
    #     print(i["type"])
    #     print(i["setup"])
    #     print(i["punchline"], "\n")

usern="kosmiccr_bot"
@bot.message_handler(func=lambda message: message.chat.type == "group" or message.chat.type == "supergroup")
def g_chat(message):
    message.txt=message.text.lower()
    message.txt=message.txt.replace("?", "")
    message.txt=message.text.lower().replace(f"@{usern}", "").strip()
    if usern in message.text.lower():

        if message.txt in ["hello","hey!","hi","hi!","hey","hello!","hi there","hi there!","hey there","hey there!","hello there","hello there!", "hi sophon","hello sophon","hey sophon","hi sophon!","hello sophon!","hey sophon!","hi sophon.","hello sophon.","hey sophon."]:
            bot.reply_to(message, f"Hello {message.from_user.first_name} ! How can I help you today?")
        elif message.txt in ["current date", "current day","date","day","today","today's date","today's day","time","what's the time","what's the day","what's the date"]:
            now = datetime.datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_day = now.strftime("%A")
            reply_message = f"The date is {current_date} and today is {current_day}."
            print("Reporting the current date and day.")
            bot.reply_to(message, reply_message)

        elif message.txt in["thanks","thanks!","thank you","thank you!","thank you so much","thanks a lot","thank you very much","thanks for the help"]:
            bot.reply_to(message, "You're welcome! Have a great day.")
        elif message.txt in["bye","goodbye","see you later","exit","quit","stop","close","end","tata"]:
            bot.reply_to(message, "Goodbye! Have a nice day.")
        elif message.txt in["who are you","what's your name","what's your name","what are you","what is your name","what is your name?","whats your purpose","what is your purpose"]:
            bot.reply_to(message, "I am Sophon, a Cloudbot. I am here to offer some small help to the students of section 13.")
        elif message.txt in["how are you?","how do you do?","how are you doing?","how are you","how do you do","how are you doing","how are u","how r u","how r you","how are you today","how do you do today","how are you doing today","how are u today","how r u today","how r you today"]:
            bot.reply_to(message, "I'm doing great! How can I help you today?")
        elif message.txt in["who created you","who made you","who developed you","who is your creator","who is your developer","who is your maker"]:
            bot.reply_to(message, "I was created by Group 4(led by Shopnil, Meghla, Koushik) as a part of their presentation on Cloud Comptuting.")
        elif message.txt in["whats my name","do you know my name","what's my name","do you know me","do you remember me","have we met before","do you recognize me","do you know who i am","do you know me?","do you remember me?","have we met before?","do you recognize me?","do you know who i am?"]:
            bot.reply_to(message,f"Yes, I know you. You are {message.from_user.first_name}. Always nice to meet you!")
        elif message.txt in["tell me a joke","tell a joke","joke please","joke","another joke","one more joke","more jokes","tell me another joke","tell me one more joke","tell me more jokes","tell me a joke!","tell a joke!","joke please!","joke!","another joke!","one more joke!","more jokes!","tell me another joke!","tell me one more joke!","tell me more jokes!","another one"]:
            bot.reply_to(message, joker())
        elif "search" in message.txt.lower():
            print("status-> User requested a search in group.")
            topic = message.text.split("search", 1)[1].strip()
            d,l,u=wikiengine(topic)
            dat=f"{d}.\n Learn more about {l} at http:{u}"
            bot.reply_to(message, dat)
        elif "define" in message.txt.lower():
            print("status-> User requested a term definition.")
            term_index = message.txt.lower().find("define") + len("define")
            term = message.txt[term_index:].strip()
            querystring = {"term":term}
            response = requests.get(urlx, headers=headers, params=querystring)
            try:
                ans=response.json()["list"][0]["definition"]
                bot.reply_to(message, ans)
            except Exception as e:
                print("Error:", e)
                bot.reply_to(message, "Sorry, I couldn't find anything like that. Please check for any typo/misspelling.")
        else:
            print(message.txt)
            bot.reply_to(message, "I am sorry, I don't understand what you are saying. Try again.")
            print("status-> System ambiguity detected, stored the logs for further improvement.")

@bot.message_handler(func=lambda message: message.chat.type == "private")
def p_chat(message):
    message.txt=message.text.lower()
    message.txt=message.txt.replace("?", "")

    if message.txt in ["hello","hey!","hi","hi!","hey","hello!","hi there","hi there!","hey there","hey there!","hello there","hello there!", "hi sophon","hello sophon","hey sophon","hi sophon!","hello sophon!","hey sophon!","hi sophon.","hello sophon.","hey sophon."]:
        bot.reply_to(message, f"Hello {message.from_user.first_name} ! How can I help you today?")
    elif message.txt in ["current date", "current day","date","day","today","today's date","today's day","time","what's the time","what's the day","what's the date"]:
        now = datetime.datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_day = now.strftime("%A")
        reply_message = f"The date is {current_date} and today is {current_day}."
        print("Reporting the current date and day.")
        bot.reply_to(message, reply_message)

    elif message.txt in["thanks","thanks!","thank you","thank you!","thank you so much","thanks a lot","thank you very much","thanks for the help"]:
        bot.reply_to(message, "You're welcome! Have a great day.")
    elif message.txt in["bye","goodbye","see you later","exit","quit","stop","close","end","tata"]:
        bot.reply_to(message, "Goodbye! Have a nice day.")
    elif message.txt in["who are you","what's your name","what's your name","what are you","what is your name","what is your name?","whats your purpose","what is your purpose"]:
        bot.reply_to(message, "I am Sophon, a Cloudbot. I am here to offer some small help to the students of section 13.")
    elif message.txt in["how are you?","how do you do?","how are you doing?","how are you","how do you do","how are you doing","how are u","how r u","how r you","how are you today","how do you do today","how are you doing today","how are u today","how r u today","how r you today"]:
        bot.reply_to(message, "I'm doing great! How can I help you today?")
    elif message.txt in["who created you","who made you","who developed you","who is your creator","who is your developer","who is your maker"]:
        bot.reply_to(message, "I was created by Group 4(led by Shopnil, Meghla, Koushik) as a part of their presentation on Cloud Comptuting.")
    elif message.txt in["whats my name","do you know my name","what's my name","do you know me","do you remember me","have we met before","do you recognize me","do you know who i am","do you know me?","do you remember me?","have we met before?","do you recognize me?","do you know who i am?"]:
        bot.reply_to(message,f"Yes, I know you. You are {message.from_user.first_name}. Always nice to meet you!")
    elif message.txt in["tell me a joke","tell a joke","joke please","joke","another joke","one more joke","more jokes","tell me another joke","tell me one more joke","tell me more jokes","tell me a joke!","tell a joke!","joke please!","joke!","another joke!","one more joke!","more jokes!","tell me another joke!","tell me one more joke!","tell me more jokes!","another one"]:
        bot.reply_to(message, joker())
    elif "search" in message.txt.lower():
        print("status-> User requested a search in private.")
        topic_index = message.txt.lower().find("search") + len("search")
        topic = message.txt[topic_index:].strip()
        d,l,u=wikiengine(topic)
        if l:
            dat=f"{d}.\n Learn more about {l} at http:{u}"
            bot.reply_to(message, dat)
        else:
            bot.reply_to(message,d)
    elif "define" in message.txt.lower():
        print("status-> User requested a term definition.")
        term_index = message.txt.lower().find("define") + len("define")
        term = message.txt[term_index:].strip()
        querystring = {"term":term}
        response = requests.get(urlx, headers=headers, params=querystring)
        try:
            ans=response.json()["list"][0]["definition"]
            bot.reply_to(message, ans)
        except Exception as e:
            print("Error:", e)
            bot.reply_to(message, "Sorry, I couldn't find anything like that. Please check for any typo/misspelling.")
    else:
        print(message.txt)
        bot.reply_to(message, "I am sorry, I don't understand what you are saying. Try again.")
        print("status-> System ambiguity detected, stored the logs for further improvement.")

bot.polling()
