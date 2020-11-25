#!/usr/bin/python3
# -*- coding: utf-8 -*-

import configparser
import datetime
import requests
import telebot
import mysql.connector as mariadb
from mysql.connector import Error
from telebot import types
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import Filters, MessageHandler
from aiohttp import web
import ssl

config = configparser.ConfigParser()
config.read('config_botreposter.conf')

bot_token = config.get('botconfig','bot_token')
chat_id_from = config.get('botconfig','chat_id_from')
chat_id_to = config.get('botconfig','chat_id_to')

send_to = config.get('botconfig', 'send_to')

db_user = config.get('botconfig','db_user')
db_password = config.get('botconfig','db_password')
db_database = config.get('botconfig','db_database')

webhook_host = config.get('botconfig','webhook_host')
webhook_port = config.get('botconfig','webhook_port')
webhook_listen = config.get('botconfig','webhook_listen')

webhook_ssl_cert = '/root/sa/bots/tg_reposter/certificate.crt'
webhook_ssl_priv = '/root/sa/bots/tg_reposter/private_key.pem'

webhook_url_base = "https://%s:%s" % (webhook_host, webhook_port)
webhook_url_path = "/%s/" % (bot_token)

bot = telebot.TeleBot(bot_token)

app = web.Application()

@bot.message_handler(content_types=["text"])
def reaction(message):
    if ('результат' in message.text or 'Результат' in message.text) and (message.chat.id == chat_id_from):
        send_text = message.text + "\n\n" + send_to
        bot.send_message(chat_id_to, send_text)

    elif message.text == 'календарь' or message.text == 'Календарь':
        mariadb_connection = mariadb.connect(user=db_user, password=db_password, database=db_database)
        sql_select_tour = "SELECT MIN(tour) FROM (SELECT tour, SUM(h_goals) as home, SUM(a_goals) as away FROM champloko$
        cursor = mariadb_connection.cursor()

        cursor.execute(sql_select_tour)
        current_tour = cursor.fetchall()

        for row in current_tour:
            current_tour = row[0]
            
        try:
            mariadb_connection = mariadb.connect(user=db_user, password=db_password, database=db_database)
            sql_select_calendar = "SELECT * FROM champlokofans WHERE tour <= " + str(current_tour) + " AND h_goals IS NU$
            cursor = mariadb_connection.cursor()

            cursor.execute(sql_select_calendar)
            calendar = cursor.fetchall()

            text_calendar = 'Ближайшие игры\n\n'

            for row in calendar:
                text_calendar = text_calendar + "{} тур Л{}{} : {} – {}\n".format(row[3], row[1], row[2], row[4], row[5]$

            bot.send_message(chat_id_from, text_calendar)

        except Exception as e:
#            print(e)
            pass

        finally:
            if (mariadb_connection.is_connected()):
                mariadb_connection.close()
                
    elif 'тур' in message.text and len(message.text) <= 6:
        tour = message.text.split(' ')[0]
        try:
            mariadb_connection = mariadb.connect(user=db_user, password=db_password, database=db_database)
            sql_select_calendar_tour = "SELECT * FROM champlokofans WHERE tour = " + str(tour) + " ORDER BY id;"
            cursor = mariadb_connection.cursor()

            cursor.execute(sql_select_calendar_tour)
            calendar_tour = cursor.fetchall()

            text_calendar_tour = str(tour) + ' тур' + '\n\n'

            for row in calendar_tour:
                text_calendar_tour = text_calendar_tour + "Л{}{} : {} {} – {} {}\n".format(row[1], row[2], row[4], row[6$

            bot.send_message(chat_id_from, text_calendar_tour)

        except Exception as e:
#            print(e)
            pass

        finally:
            if (mariadb_connection.is_connected()):
                mariadb_connection.close()

#updater = Updater(token=bot_token)
#
#updater.start_polling()

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(webhook_ssl_cert, webhook_ssl_priv)

web.run_app(
    app,
    host=webhook_listen,
    port=webhook_port,
    ssl_context=context,
)

#if __name__ == '__main__':
#    bot.polling(none_stop=True)
