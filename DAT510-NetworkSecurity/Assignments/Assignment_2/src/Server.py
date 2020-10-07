from flask import Flask,  request, redirect, url_for, render_template,jsonify
from flask_socketio import SocketIO,send,emit,join_room,leave_room
import logging
import os
import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'CiphersForCiphers'
socketio = SocketIO(app,logger=False)

app.config["TEMPLATES_AUTO_RELOAD"] = True
        

connectedUsers = {}

if not os.path.isdir('log'):
    os.mkdir('log')
filename = datetime.datetime.now()
filename = filename.strftime("%Y%m%d%H%M%S")
filename = 'log\\Server_' + filename + '.log'

logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(filename)
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)


@app.route('/')
def index():
     return 'Diffie Hellman Encrypted chat messenger. Index page.'

@app.route('/getusers')
def getusers():
    return connectedUsers

@app.route('/sendusers')
def sendusers():
    session = request.args.get('session')
    message = request.args.get('message')
    sender =  connectedUsers[session]
    data = {'session':session,'message':message,'sender':sender}
    emit('message',data,room=session,namespace='/',broadcast=True)
    return connectedUsers

@socketio.on('chatwith')
def handle_send_msg(data):
    requester = data['requester']
    requester_sid = data['requester_sid']
    user = data['user']
    session_id = data['user_sid']
    logger.info(f'User: {requester} wants to start chat with {user}...')
    emit('beginchat',data,room=session_id,namespace='/')


@socketio.on('onnextkey')
def nextkey(data):
    logger.info(f'Requesting new key creation...')
    user_sid = data['user_sid']
    requester_sid = data['requester_sid']
    if request.sid == requester_sid:
        emit('nextkey',data,room=user_sid,namespace='/')
    

@socketio.on('onhandshake')
def handshake(data):
    requester = data['requester']
    requester_sid = data['requester_sid']
    user = data['user']
    user_sid = data['user_sid']
    logger.info(f'Handshake for : {requester}...')
    emit('handshake',data,room=requester_sid,namespace='/')
    logger.info(f'Handshake for : {user}...')
    emit('handshake',data,room=user_sid,namespace='/')

    
@socketio.on('logout')
def logout(data):
    session = data['session']
    user = data['user']
    del connectedUsers[session]
    logger.info(f'User {user} has loged out: ')
    emit('connectedusers',connectedUsers)

@socketio.on('login')
def login(data):
    session = data['session']
    user = data['user']
    connectedUsers[session] = user
    logger.info(f'User {user} has logged in {request.sid}')
    emit('users',connectedUsers,broadcast=True)

@socketio.on('sendmessage')
def sendmessage(data):
    user_sid = data['user_sid']
    requester_sid = data['requester_sid']
    enc = data['enc']
    logger.info(f'Send Message request, tranmsitting encrypted message: {enc}...')
    emit('sendmessage',data,room=user_sid)
    

@socketio.on('message')
def handle_message(message):
    logger.info('received message: ' + message)

@app.route('/get_users',methods=['GET'])
def get_users():
    return jsonify(connectedUsers)


if __name__ == '__main__':
    # app.run(port=8080)
    socketio.run(app)
    logger.info(f'Connected {socketio.server.get_session()}')
    logger.info('Server has started...')