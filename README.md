# Chat Room Application 

### Overview :

In my operating systems course, I was tasked to develop a client-server based communication system (chat room) as part of a university project. The project's main objective is to illustrate the practical application of Inter-Process Communication (IPC) using socket programming. It is implemented in Python using Flask and Socket.IO to handle real-time web socket connections.

### Features: 
- **Random username generation**: when a new client enters, he is assigned a new random user based on a random name from a list of predefined names and a character trait. (ie username = random name + random trait + random number)
- **User List**: a user list of the currently connected users is broadcasted and shown to all users.
- **GUI** : This is all accessible through a simple yet intuitive graphical user interface.

### Dependencies:
- Flask
- Flask_socketio

`pip install Flask flask-socketio`
   
