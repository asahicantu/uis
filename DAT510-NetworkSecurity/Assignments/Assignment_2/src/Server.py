from flask import Flask,  request, redirect, url_for, render_template,jsonify
from flask_socketio import SocketIO,send,emit,join_room,leave_room
app = Flask(__name__)
app.config['SECRET_KEY'] = 'CiphersForCiphers'
socketio = SocketIO(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True
        

connectedUsers = {}


@app.route('/')
def index():
     return render_template('index.html')

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
    print(f'User: {requester} wants to start chat with {user}...')
    emit('beginchat',data,room=session_id,namespace='/')


@socketio.on('handshake')
def handshake(data):
    requester = data['requester']
    requester_sid = data['requester_sid']
    user = data['user']
    user_sid = data['user_sid']
    print(f'Handshake for : {requester}...')
    emit('handshake',data,room=requester_sid,namespace='/')
    print(f'Handshake for : {user}...')
    emit('handshake',data,room=user_sid,namespace='/')

    


@socketio.on('logout')
def logout(data):
    session = data['session']
    user = data['user']
    del connectedUsers[session]
    print(f'User {user} loged out: ')
    emit('connectedusers',connectedUsers)


@socketio.on('login')
def login(data):
    session = data['session']
    user = data['user']
    connectedUsers[session] = user
    print(f'User {user} logged in {request.sid}')
    emit('users',connectedUsers,broadcast=True)

@socketio.on('sendmessage')
def sendmessage(data):
    s_id = data['s_id']
    enc = data['enc']
    print(f'Send Message request, transitting encrypted message: {enc}...')
    emit('sendmessage',data,room=s_id)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)





@app.route('/getpub',methods=['GET'])
def getpub():
    text = request.args.get('plainText')
    text_list = __sdes.split_string(text,1)
    text_bin = [ __sdes.int2bin(ord(x),8) for x in text_list ]
    cipher = ''
    for t_b in text_bin:
        cipher += __sdes.encrypt3SDES(t_b,__k1,__k2)
    return cipher

@app.route('/getmsg',methods=['GET'])
def getmsg():
    cipher = request.args.get('cipherText')
    cipher = __sdes.split_string(cipher,8)
    text =''
    for c in cipher:
        t_b = __sdes.decrypt3SDES(c,__k1,__k2)
        text += chr(int(t_b,2))
    return text

@app.route('/sendmsg',methods=['POST'])
def sendmsg():
    enc = request.args.get('enc')
    sender = request.args.get('sender')
    recipient = request.args.get('recipient')

@app.route('/login',methods=['GET'])
def login():
    username = request.args.get('username')
    if username not in  connectedUsers:
        connectedUsers.append(username)
        print(f'User {username} loged in')
        #send(username + ' has logged in', room=room)
        return jsonify(connectedUsers)
    else:
         raise Exception(f'Could not connect to server, username {username} already chosen', status_code=400)

@app.route('/logout',methods=['GET'])
def logout():
    username = request.args.get('username')
    if username in  connectedUsers:
        connectedUsers.remove(username)
        print(f'User {username} loged out')
        return jsonify(connectedUsers)
    else:
         raise Exception(f'Could not logout user {username} since it does not exist', status_code=500)


@app.route('/get_users',methods=['GET'])
def get_users():
    return jsonify(connectedUsers)


if __name__ == '__main__':
    # app.run(port=8080)
    socketio.run(app)
    print(f'Connected {socketio.server.get_session()}')