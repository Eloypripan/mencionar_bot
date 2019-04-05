#!/usr/bin/python3
# -*- coding: utf-8 -*-

import telebot # Libreria de la API del bot.
from telebot import types # Tipos para la API del bot.
import time # Librería para hacer que el programa que controla el bot no se acabe
import logging
import sympy

token_file = open("TOKEN.txt", "r") # "TOKEN.txt" tiene el token que Bot Father nos dio en la primera línea
TOKEN = token_file.readline()
token_file.close()

partidas = {}

pole = AdminPole("polelog.txt")

commands = {  # command description used in the "help" command

              'start': 'Arranca a este inteligente pingüino',
              'help': 'Ayuda de este bot',
			  'mencionar_todos': 'menciona a todos',

}

bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.

#############################################
#Listener
def listener(messages): # Con esto, estamos definiendo una función llamada 'listener', que recibe como parámetro un dato llamado 'messages'.
	for m in messages: # Por cada dato 'm' en el dato 'messages'
		if m.content_type == 'text': # Filtramos mensajes que sean tipo texto.
			cid = m.chat.id # Almacenaremos el ID de la conversación.
			print("[" + str(cid) + "]: " + m.text) # Y haremos que imprima algo parecido a esto -> [52033876]: /start

bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.
#############################################
#Funciones

##START
@bot.message_handler(commands=['start'])
def command_start(m):
	cid = m.chat.id
	bot.send_message(cid, "Arrancando Pingüeinstein...\n¡Buenas! ¿En qué puedo servirle?")
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
def command_staus(m):
    cid = m.chat.id
    bot.send_message(cid, "Estoy 100% operativo")

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

##MENCIONAR
@bot.message_handler(commands=['mencionar']) # Indicamos que lo siguiente va a controlar el comando '/chiste'
def command_mencionar(m): # Definimos una función que resuleva lo que necesitemos.
	cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
	bot.send_message( cid,)

##ALL
@bot.message_handler(func=lambda message: message.content_type == "text" and "@all" in message.text.lower())
def all:
    bot.reply_to(m, )

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
