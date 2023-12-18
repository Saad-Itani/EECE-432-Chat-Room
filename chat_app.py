import random
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room,  disconnect
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jad_Saad'
socketio = SocketIO(app)

connected_users = {}  # Dictionary to store connected users and keep track of currently connected users

@app.route('/')  ## this just the root URL of the web app 
def index():
    return render_template('index.html')

def random_username(): # creating random username based on character trait + name + random number 
    adjectives = ["Clever", "Cute", "Brave", "Happy", "Funny", "Mysterious"]
    nouns = ["Jad", "Saad", "Lynn", "Jana", "Khalil", "Samer"]
    return random.choice(adjectives) + random.choice(nouns) + str(random.randint(1, 99))

## Handling a new client connection :
## We are listening here for the "connect" event which is triggered when a new client establishes a connection with the server. 
## It then assigns a random username to the new user and stores it in the session dictionary used by the flask framework. We then assign 
## username to its SID, which is the session id, in the connected users dictionary which we initialized beforehand. Finally we emit the 
## event "update_user_list" which sends the list of current connected users the list of the currently connected users to update it 
## on each users interface. Finally, we call handle_new_connection() broadcasts a new message to all users to notify them that a 
## new user has entered the chat along with the timestamp. We emit a broadcast_message to the server to broadcast the message 

@socketio.on('connect') 
def handle_connect():
    username = random_username()
    session['username'] = username
    connected_users[request.sid] = username
    emit('update_user_list', list(connected_users.values()), broadcast=True) ## This specifies that message should be sent to all 
    ## connected users
    handle_new_connection(username)

def handle_new_connection(username):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    emit('broadcast_message', {'message': f'{username} has joined the chat', 'timestamp': timestamp}, broadcast=True)

## Handling when a user disconnects:  
## It listens for the event "disconnect" which is triggered when a user disconnects or when we close the tab of the user basically. 
## We start by popping the name of that users from the list of currently connected users and alert all connected users to update their 
## list and then emit "broadcast_message" event to send a message on the chat that this current user has left and alongside it 
## the timestamp 

@socketio.on('disconnect')
def handle_disconnect():
    username = connected_users.pop(request.sid, 'Anonymous')
    emit('update_user_list', list(connected_users.values()), broadcast=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    emit('broadcast_message', {'message': f'{username} has left the chat', 'timestamp': timestamp}, broadcast=True)

## Handling when sending a message: 
## First we get the username of the session that is currently sending a message. We then emit a broadcast event 
## that broadcasts the message along with the user who sent the message to all users 
@socketio.on('send_message')
def handle_send_message(message):
    username = session.get('username', 'Anonymous')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    emit('broadcast_message', {'message': f'{username}: {message}', 'timestamp': timestamp}, broadcast=True)

## Runs the flask application 
if __name__ == '__main__':
    socketio.run(app, debug=True)
