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

commands = {  # command description used in the "help" command

              'start': 'Arranca a este bot',
              'help': 'Ayuda de este bot',
			  'mencionar_todos': 'menciona a todos',

}

#############################################
#Listener
def listener(messages): # Con esto, estamos definiendo una función llamada 'listener', que recibe como parámetro un dato llamado 'messages'.
	for m in messages: # Por cada dato 'm' en el dato 'messages'
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
	bot.send_message(cid, "Arrancando Mencionar_todos_bot")
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
	
"""	
##############################
m.from_user.username
m.from_user.username.first_name+"+"m.from_user.username.last_name

##Vector Usuarios
#vector_user(numero id del grupo, alias)for j in self.players:
def vector_user(cid, self):
			for i in range(0, len(self.user)):
				if (self.user[i].user.id == cid):
					return i
			return -1

nombre = j.user.username
	if (nombre == None):
		nombre = j.user.first_name + ' ' + j.user.last_name
	else:
	nombre = '@' + nombre
	
vector_user(cid, j)=nombre
	
def add_group(self, cid, user):
	    self.groups[cid] = Groupuser(user, cid)

class group_user:
	def __init__(self, usuario
		if (type(usuario).__name__ == 'User'):
			self.user = usuario
		elif (type(usuario).__name__ == 'TextIOWrapper'):
			self.read(usuario)
		elif (type(usuario).__name__ == 'dict'):
			userdict = ast.literal_eval(usuario['user'])
			self.user = types.User(userdict['id'], userdict['is_bot'],
				userdict['first_name'], userdict['username'],
				userdict['last_name'], userdict['language_code'])
		else:
			raise TypeError("Argumento 'usuario' es de un tipo no válido")	
	
	
					     

"""	

##MENCIONAR
@bot.message_handler(commands=['mencionar']) # Indicamos que lo siguiente va a controlar el comando '/chiste'
def command_mencionar(m): # Definimos una función que resuleva lo que necesitemos.
    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
    bot.send_message(cid, "@eloypripan")
    #bot.send_message(cid, vector_user(cid, ))


##ALL
@bot.message_handler(func=lambda message: message.content_type == "text" and "@all" in message.text.lower())
def all(m):
    cid = m.chat.id
    bot.reply_to(m, "@eloypripan")

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
