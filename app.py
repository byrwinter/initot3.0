import telegram
import pymongo
from telegram.ext import Updater, Dispatcher, BaseFilter, MessageHandler, CommandHandler, Filters
from controls import *


#variables and settings
token = "667772958:AAHzUzttA2c_dLQumYixYXQaTMbVzPTCFDU"
initot = telegram.Bot(token=token)
updater = Updater(token=token)
dispatcher = updater.dispatcher







#customfilters

#reply messages filter
class rep_filter(BaseFilter):
    def filter(self, message):
        return 'Reply Messages' in message.text

repFilter = rep_filter()

#add admin filter
class add_filter(BaseFilter):
    def filter(self, message):
        return 'Add Admin' in message.text

addAdminFilter = add_filter()





#handlers
#start
startHandler = CommandHandler("start", startHandle)
dispatcher.add_handler(startHandler)

#add admin handler
addAdminHandler = MessageHandler(addAdminFilter, addAdminHandle)
dispatcher.add_handler(addAdminHandler)

#replymessages
replyMsgHandler = MessageHandler(repFilter, replyMsgHandle)
dispatcher.add_handler(replyMsgHandler)

repliedMsgHandler = MessageHandler(Filters.reply, repliedMsgHandle)
dispatcher.add_handler(repliedMsgHandler)

#sub messages
subMsgHandler = MessageHandler(Filters.text, subMsgHandle)
dispatcher.add_handler(subMsgHandler)


updater.start_polling()