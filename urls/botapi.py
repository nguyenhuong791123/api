# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, request, jsonify
from utils.cm.agent import parse_http_accept_language
from utils.bot.bot import get_bot, trainer_databases, trainer, STORAGE_ADAPTER

app = Blueprint('botapi', __name__)
bot = None

@app.route("/bot")
def index():
    global bot
    bot = get_bot("scapp", STORAGE_ADAPTER.SQLLITE, None, None)
    return render_template("bot.html")

@app.route("/trainer")
def bot_trainer():
    chats = [
        'How are you?',
        'I am good.',
        'That is good to hear.',
        'Thank you',
        'You are welcome.',
    ]
    bot = get_bot("scapp", STORAGE_ADAPTER.SQLLITE, None, None)
    result = trainer(chats)
    return jsonify(result), 200

@app.route("/trainer_all")
def bot_trainer_databases():
    l = parse_http_accept_language(request.headers.get('Accept-Language', ''))
    if l is None:
        l = 'ja'
    # l = 'en'

    logic_adapters = [
        "chatterbot.logic.MathematicalEvaluation"
        ,"chatterbot.logic.TimeLogicAdapter"
        ,"chatterbot.logic.BestMatch"
    ]
    bot = get_bot("scapp", STORAGE_ADAPTER.SQLLITE, logic_adapters, None)
    result = trainer_databases(bot, l)
    return jsonify(result), 200

@app.route("/botget")
def get_bot_response():
    msg = request.args.get('msg')
    if bot is None:
        return 'Not Setting ChatBot!!!'

    result = None
    try:
        result = str(bot.get_response(msg))
    except EOFError as e:
        result = str(e)

    return result

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=8084)
