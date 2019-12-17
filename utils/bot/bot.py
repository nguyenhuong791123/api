# -*- coding: UTF-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

from ..cm.utils import is_empty

class DATA_MODE():
    def __init__(self):
        self.ja = 'japanese'
        self.en = 'english'

class STORAGE_ADAPTER():
    SQLLITE = 'chatterbot.storage.SQLStorageAdapter'
    MONGODB = 'chatterbot.storage.MongoDatabaseAdapter'

def get_bot(bot_mode, storage_adapter, logic_adapters, database_uri):
    if is_empty(bot_mode):
        return None

    if is_empty(storage_adapter) == False and is_empty(logic_adapters) == False and is_empty(database_uri) == False:
        return ChatBot(bot_mode, storage_adapter=storage_adapter, logic_adapters=logic_adapters, database_uri=database_uri)
    elif is_empty(storage_adapter) == False and is_empty(logic_adapters) == False:
        return ChatBot(bot_mode, storage_adapter=storage_adapter, logic_adapters=logic_adapters)
    elif is_empty(storage_adapter) == False:
        return ChatBot(bot_mode, storage_adapter=storage_adapter)
    else:
        return None

def trainer(chats):
    if chats is None or len(chats) <= 0:
        return None

    result = {}
    try:
        trainer = ChatterBotCorpusTrainer(bot)
        trainer.train(chats)
        result['msg'] = 'Data Trainer Completed !!!'
    except Exception as ex:
        print(str(ex))
        result['msg'] = str(ex)
    
    return result

def trainer_databases(bot, language):
    if bot is None or is_empty(language):
        return None

    result = {}
    dir = "chatterbot_corpus.data." + get_data_mode(language)
    try:
        trainer = ChatterBotCorpusTrainer(bot)
        trainer.train(dir)
        result['msg'] = 'Data Trainer Completed !!!'
    except Exception as ex:
        print(str(ex))
        result['msg'] = str(ex)
    
    return result

def get_data_mode(language):
    if is_empty(language):
        return DATA_MODE.ja

    codes = DATA_MODE()
    for key, value in codes.__dict__.items():
        if is_empty(value) or key != language:
            continue
        return value
    return DATA_MODE.ja
