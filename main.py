import requests as r
from bs4 import  BeautifulSoup as bs
from getuseragent import UserAgent
import json
import telebot

useragent = UserAgent("ios")

token = "5544482923:AAGX5pNSq_Bcj3c4XqAKPQoRpno66HWpGYI"
bot = telebot.TeleBot(token)


def find_link(url):
	headers = {
	    'User-Agent': useragent.Random()
	}
	link_id = r.get(url, headers=headers, stream=True, allow_redirects=True, timeout=5).url.split("/")[5].split("?", 1)[0]
	get_data = r.get("https://api.tiktokv.com/aweme/v1/multi/aweme/detail/?aweme_ids=%5B"+link_id+"%5D").text
	obj = json.loads(get_data)
	return obj["aweme_details"][0]["video"]["play_addr"]["url_list"][0]


@bot.message_handler(commands=['start'])
def start(message):
	chat_id = message.from_user.id
	bot.send_message(chat_id, "send me url tiktok")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
	pesan = message.text
	chat_id = message.from_user.id
	if "tiktok" in pesan:
		bot.send_video(chat_id, find_link(pesan), caption = "terimakasi, jangan lupa share")
	else:
		bot.send_message(chat_id, "send me url tiktok")

bot.polling()
