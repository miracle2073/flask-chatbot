import json
import eventlet

from flask import Flask, render_template, copy_current_request_context
from flask_socketio import SocketIO, send, emit

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)
socketio = SocketIO(app)

Joe = ChatBot("Joe Bot")
Joe.set_trainer(ChatterBotCorpusTrainer)

pool = eventlet.GreenPool()
pile = eventlet.GreenPile(pool)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('my event')
def handle_my_custom_event(data):
    data = json.loads(str(data).replace("\'", "\""))
    emit('chat', data)

    @copy_current_request_context
    def train_bot():
        Joe.train("chatterbot.corpus.english.conversations")
        print("Training finished...")

    @copy_current_request_context
    def calculate_response(msg):
        print("Calculating response for {}".format(msg))
        response = str(Joe.get_response(msg))
        print("Response is: {}".format(response))
        emit('chat', {"user": "Joe", "msg": response})
        emit('joe', response)

    emit('joe', 'Let me think... It may take a while, so be patient =)')
    pile.spawn(calculate_response, data["msg"])

@socketio.on('disconnect')
def disconnect():
    print("disconnected...")

@socketio.on('connect')
def connect():
    emit('flush', 'You\'ve been successfully connected to server...')
    print("Connected...")

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8000)
