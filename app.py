from gevent import monkey
monkey.patch_all()
from time import sleep
import sqlite3
from random import random
from flask import Flask, render_template, copy_current_request_context, g, request, jsonify,redirect
from flask_socketio import SocketIO, emit

# ROUTING OF SERVER

# DEFINATIONS
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

PERSON = '"C"'

def scoreUpdate(person,value):
    score = query_db('select Marks from Driver where PersonID={};'.format(person))[0][0]
    score = (score - value)%100
    query = "update Driver SET Marks="+str(score)+" where PersonID='C';"
    query_db(query)

# DATABASE CONNECTION

# DEFINITIONS

DATABASE = './database.db'

# FUNCTIONS

def args_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = args_db().execute(query, args)
    rv = cur.fetchall()
    args_db().commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulation/')
def simulation():
    return render_template('sim.html')

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

# INFERENCES

# CONDITIONAL

@app.route('/acc/')
def acc():
    if 'var' in request.args:
        limit = 11 
        var = int(request.args['var'])
        if var > limit:
            socketio.emit('data', {"msg":"Harsh Acceleration"})
            scoreUpdate(PERSON,.5)
            return redirect('/simulation/')
        elif -1 * var > limit:
            socketio.emit('data', {"msg":"Harsh Brakeing"})
            scoreUpdate(PERSON,.5)
            return redirect('/simulation/')
        else:
            scoreUpdate(PERSON,-.005)
            return jsonify({"msg":"Harsh Retardation"})
    else:
        return jsonify({'err':'var not in provided'})

@app.route('/speed/')
def speed():
    if 'var' in request.args:
        limit = 110
        var = int(request.args['var'])
        if var > limit:
            socketio.emit('data', {"msg":"Harsh Speeding"})
            scoreUpdate(PERSON,.5)
            return redirect('/simulation/')
        else:
            return jsonify({'err':'var in limit'})
    else:
        return jsonify({'err':'var not in provided'})

@app.route('/engine/load/')
def engineLoad():
    if 'var' in request.args:
        high = 50
        low = 20
        var = int(request.args['var'])
        if var < low or var >= high:
            socketio.emit('data', {"msg":"Engine load inappropriate.","map":"mechanic"})
            return redirect('/simulation/')
        else:
            return jsonify({'err':'var in limit'})            
    else:
        return jsonify({'err':'var not in scope'})

@app.route('/engine/vehicle/')
def engineVehicle():
    if 'var' in request.args:
        high = 1.3
        low = 0.9
        var = int(request.args['var'])
        if var <= low:
            socketio.emit('data', {"msg":"Slow down."})
            scoreUpdate(PERSON,.5)
            return redirect('/simulation/')
        elif var > high:
            return jsonify({"msg":"Speed Up"})
    else:
        return jsonify({'err':'var not in scope'})

@app.route('/stopping/')
def stopping():
    if 'var' in request.args:
        limit = 12
        var = int(request.args['var'])
        if var > limit:
            socketio.emit('data', {"msg":"Turn off engine."})
            scoreUpdate(PERSON,.5)
            return redirect('/simulation/')
        else:
            return jsonify({'err':'var in limit'})
    else:
        return jsonify({'err':'var not in scope'})

# BOOLEAN INFERENCE

@app.route('/coolant/')
def coolant():
    socketio.emit('data', {"msg":"Engine Coolant Circuit Error.","map":"mechanic"})
    return redirect('/simulation/')

@app.route('/misfire/')
def misfire():
    socketio.emit('data', {"msg":"Engine might have an issue.","map":"mechanic"})
    return redirect('/simulation/')

@app.route('/ocircuit/')
def ocircuit():
    socketio.emit('data', {"msg":"Error with O2 circuit","map":"mechanic"})
    return redirect('/simulation/')

# MAIN RUNNER

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0",port=9000)

