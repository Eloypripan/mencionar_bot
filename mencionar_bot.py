#!/usr/bin/python3
# -*- coding: utf-8 -*-

import telebot # Libreria de la API del bot.
from telebot import types # Tipos para la API del bot.
import time # Librería para hacer que el programa que controla el bot no se acabe
import logging
import sympy
import ast

token_file = open("TOKEN.txt", "r") # "TOKEN.txt" tiene el token que Bot Father nos dio en la primera línea
TOKEN = token_file.readline()
token_file.close()

bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.

def lee_grupos(groupsfile, dic):
	f = open(groupsfile, "r+")
	group = f.readline()
	usr = f.readline()
	f.readline()
	while (group != '' and usr != ''):
		dic[int(group)] = usr
		group = f.readline()
		usr = f.readline()
		f.readline()
		
def guarda_grupos(groupsfile, dic, m):
	if (m.chat.type != "private"):
		f = open(groupsfile, "w+")
		for key in dic:
			f.write(str(key) + "\n" + dic[key] + "\n")
	
grupos = {} # Diccionario de chats de Telegram, con diccionarios de users
lee_grupos("grupos.txt", grupos)

commands = {  # command description used in the "help" command

              'start': 'Arranca a este inteligente bot',
              'help': 'Ayuda de este bot',
			  'mencionar_todos': 'menciona a todos',

}

#############################################
#Listener
def listener(messages): # Con esto, estamos definiendo una función llamada 'listener', que recibe como parámetro un dato llamado 'messages'.
	for m in messages: # Por cada dato 'm' en el dato 'messages'
		if (not(m.chat.id in grupos)):
			grupos[m.chat.id] = ""
		
		nombre = m.from_user.username
		if (nombre == None):
			try:
				nombre = m.from_user.first_name + ' ' + m.from_user.last_name
			except:
				nombre = m.from_user.first_name
			else:
				return
		else:
			nombre = '@' + nombre
	
		if (not(nombre in grupos[m.chat.id])):
			grupos[m.chat.id] = nombre + ' ' + grupos[m.chat.id]
			guarda_grupos("grupos.txt", grupos, m)
			
		if m.content_type == 'text': # Filtramos mensajes que sean tipo texto.
			cid = m.chat.id # Almacenaremos el ID de la conversación.
			print("[" + str(cid) + "]: " + m.text) # Y haremos que imprima algo parecido a esto -> [52033876]: /start

bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.
#############################################

##FUNCIONES

##START
@bot.message_handler(commands=['start'])
def command_start(m):
	cid = m.chat.id
	bot.send_message(cid, "Arrancando Mencionar_todos...\n¡Buenas! ¿En qué puedo servirle?")
	command_help(m)

##HELP
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Los siguientes comandos están disponibles:\n\n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page
##STATUS
@bot.message_handler(commands=['status'])
def command_status(m):
    cid = m.chat.id
    bot.send_message(cid, "Estoy vivo y 99% operativo")

##MSG	
@bot.message_handler(commands=['msg'])
def send_mensaje(m):
    text = m.text[len("/msg "):]
    tam = len(text)

    i = 0
    while (i < tam and text[i] != ' '):
        i += 1
    if (i == tam):
        return
    cid = text[:i]
    mensaje = text[i+1:]

    bot.send_message(cid, mensaje)

##ID	
@bot.message_handler(commands=['id'])
def command_id(m):
    cid = m.chat.id
    username = m.from_user.username
    uid = m.from_user.id
    bot.send_message(uid, "You are: @" + str(username)+ " " + "And your Telegram ID is: " + str(uid))
    bot.send_message(uid, "This group is: " + str(m.chat.title)+ " " + "And group Telegram ID is: " + str(cid))


##MENCIONAR
@bot.message_handler(commands=['mencionar_todos']) # Indicamos que lo siguiente va a controlar el comando '/chiste'
def command_mencionar_toh(m): # Definimos una función que resuleva lo que necesitemos.
	cid = m.chat.id
	st = bot.get_chat_member(cid, m.from_user.id).status
	if ((st == "creator" or st == "administrator") and cid in grupos):
		bot.reply_to(m, grupos[cid])

##ALL
@bot.message_handler(func=lambda message: message.content_type == "text" and ("@all" in message.text.lower() or "@todos" in message.text.lower()))
def all(m):
	cid = m.chat.id
	st = bot.get_chat_member(cid, m.from_user.id).status
	if ((st == "creator" or st == "administrator") and cid in grupos):
		bot.reply_to(m, grupos[cid])

############################################
#Peticiones
##LOGING TO TELEGRAM
logger = logging.getLogger(__name__)

while True:

    try:

            bot.polling(none_stop=True)

    except Exception as err:

            logger.error(err)

            time.sleep(10)

            print('Error en la conexión')
