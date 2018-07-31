import telegram
import pymongo
import secrets
import time, threading
from telegram.ext import Updater, Dispatcher, BaseFilter, MessageHandler, CommandHandler, Filters
from pymongo import MongoClient



#variables and settings
initotClient = MongoClient(0.0.0.0, 5000)
initotdb = initotClient["quentindb"]
initotadmins = initotdb["initotadmins"]
initotsubs = initotdb["initotsubs"]
admintokens = initotdb["admintokens"]
usedtokens = initotdb["usedtokens"]





#functions
def addAdmin(initot, update):
  #info
  adminId = update.message.chat_id
  adminName = update.message.from_user.first_name
  adminLink = update.message.from_user.name
  adminInfo = {"adminId": adminId, "adminName": adminName, "adminLink": adminLink}
  #logic
  initotadmins.insert(adminInfo)


def addSub(initot, update):
  #info
  subId = update.message.chat_id
  subName = update.message.from_user.first_name
  subLink = update.message.from_user.name
  subInfo = {"subId": subId, "subName": subName, "subLink": subLink}
  #logic
  initotsubs.insert(subInfo)



def checkRank(initot, update):
  admin = initotadmins.find_one({"adminId": update.message.chat_id})
  sub = initotsubs.find_one({"subId": update.message.chat_id})
  return admin, sub

def getAdmins(initot, update):
  admingrp = initotadmins.find()
  for admins in admingrp:
    return admins

def deletetoken(admintoken):
  time.sleep(70)
  usedtokens.insert({"currenttoken": admintoken})
  admintokens.remove({"currenttoken": admintoken})

def genToken():
  admintoken = secrets.token_hex(16)
  currtoken = {"currenttoken": admintoken}
  admintokens.insert(currtoken)
  return admintoken

def createToken():
  genToken()
  admintoken = genToken()
  return admintoken

def checkToken():
  prestokens = admintokens.find()
  tokens = []
  for token in prestokens:
    tokens.append(token["currenttoken"])
  return tokens

