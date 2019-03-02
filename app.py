from gevent import monkey
monkey.patch_all()
from threading import Thread, Event
from time import sleep
import sqlite3
from random import random
from flask import Flask, render_template, copy_current_request_context, g
from flask_socketio import SocketIO, emit

# ROUTING OF SERVER

# DEFINATIONS
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True


# ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return str(tuple(query_db('select * from example')))

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# SOCKET WORK

socketio = SocketIO(app, async_mode='gevent')

# CONNECTIONS

@socketio.on('connect')
def test_connect():
    print('Client Connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


# DATABASE CONNECTION

# DEFINITIONS

DATABASE = './database.db'

# FUNCTIONS

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# MAIN RUNNER

if __name__ == '__main__':
    socketio.run(app)