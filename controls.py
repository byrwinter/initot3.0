import telegram, time, threading
from telegram.ext import Updater, Dispatcher, BaseFilter, MessageHandler, CommandHandler, Filters
from emoji import emojize
from controls import *
from db import *




#variables and settings
token = "667772958:AAHzUzttA2c_dLQumYixYXQaTMbVzPTCFDU"
initot = telegram.Bot(token=token)
updater = Updater(token=token)
dispatcher = updater.dispatcher

#emojis
smiley = emojize(":smiley:", use_aliases=True)
simple_smile = emojize(":blush:", use_aliases=True)
wink = emojize(":wink:", use_aliases=True)
smile = emojize(":smile:", use_aliases=True)
confused = emojize(":confused:", use_aliases=True)
envelope = emojize(":envelope:", use_aliases=True)
thumbsup = emojize(":thumbsup:", use_aliases=True)
thumbsdown = emojize(":thumbsdown:", use_aliases=True)
point_down = emojize(":point_down:", use_aliases=True)
wave = emojize(":wave:", use_aliases=True)
warning = emojize(":warning:", use_aliases=True)



#functions



#start
def startHandle(initot, update):
  checkRank(initot, update)
  rankResults = checkRank(initot, update)
  admin = rankResults[0]
  sub = rankResults[1]
  if admin:
    buttons = [["Reply Messages", "Add Admin"]]
    keyboard = telegram.ReplyKeyboardMarkup(buttons,resize_keyboard=True)
    initot.send_message(chat_id=update.message.chat_id, text="Hello Admin " + smile + "\n What do you wanna do?" , reply_markup=keyboard)
  elif sub:
    initot.send_message(chat_id=update.message.chat_id, text="Heyy " + confused + "\nYou've already started the bot. " + simple_smile + "  You can send your messages now " + envelope)
  else:
    initot.send_message(chat_id=update.message.chat_id, text="Heyy There " + wave + smile + ",\nI'm Initot, the official bot for the admins of @marvel_newz. "+ simple_smile + "\nSend any message " + envelope + " to them through me. " + simple_smile)
    addSub(initot, update)



#sub messages
def subMsgHandle(initot, update):
  rankResults = checkRank(initot, update)
  sub = rankResults[1]
  admin = getAdmins(initot, update)
  checkToken()
  tokens = checkToken()
  if update.message.text in tokens:
    initot.send_message(chat_id=update.message.chat_id, text= smiley + " Congrats, you're now an admin.")
    addAdmin(initot, update)
    buttons = [["Reply Messages", "Add Admin"]]
    keyboard = telegram.ReplyKeyboardMarkup(buttons,resize_keyboard=True)
    initot.send_message(chat_id=update.message.chat_id, text="Hello Admin " + smile + "\n What do you wanna do?" , reply_markup=keyboard)
  else:
    if sub:
      initot.send_message(chat_id=update.message.chat_id, text="Message recieved " + thumbsup + ".\nWe'll get back to you " + simple_smile)
      initot.forward_message(chat_id=admin["adminId"], from_chat_id=update.message.chat_id, message_id=update.message.message_id)
    else:
      initot.send_message(chat_id=update.message.chat_id, text=smile + simple_smile + update.message.text)


#replymessage command
def replyMsgHandle(initot, update):
  rankResults = checkRank(initot, update)
  admin = rankResults[0] 
  if admin:
    initot.send_message(chat_id=update.message.chat_id, text=thumbsup + " Please  tap/right-click  the message you want to reply and reply it to me... " + simple_smile)
  else:
    initot.send_message(chat_id=update.message.chat_id, text=thumbsdown + " You're not authorized") 

#replied message handler
def repliedMsgHandle(initot, update):
  rankResults = checkRank(initot, update)
  admin = rankResults[0] 
  if admin:
    initot.send_message(chat_id=update.message.reply_to_message.forward_from.id, text="Reply: " + point_down +"\n" + update.message.text) 
    initot.send_message(chat_id=update.message.chat_id, text=thumbsup + " Reply sent " + simple_smile) 
  else:
    initot.forward_message(chat_id=admin["adminId"], from_chat_id=update.message.chat_id, message_id=update.message.message_id)

#add admin handle

def addAdminHandle(initot, update):
  admintoken = createToken()
  rankResults = checkRank(initot, update)
  admin = rankResults[0] 
  if admin:
    initot.send_message(chat_id=update.message.chat_id, text= thumbsup + "We've recieved your message to add an administrator.\n" + warning + "We're about to send a token to you. Give this token to your desired admin and tell him to send it to us. The token will expire within 24hours")
    createToken()
    initot.send_message(chat_id=update.message.chat_id, text=admintoken)
    deletetokenThread = threading.Thread(target=deletetoken, args=(admintoken, ))
    deletetokenThread.start()
  else:
    initot.send_message(chat_id=update.message.chat_id, text=thumbsdown + " You're not authorized")
