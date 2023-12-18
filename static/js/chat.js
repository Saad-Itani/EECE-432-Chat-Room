$(document).ready(function(){
    
    // establishing a connection  
    var socket = io.connect('http://' + document.domain + ':' + location.port); 
    // document.domain here returns the domain name of the server that server that served the webpage, and the port 
    // is used for the server to determine which port the server is running on, this is important for the SOCKeTIO connection 
    // is made to the correct port. 

    // socket.on(....) these are event listeners, so basically for events like connect, broadcast message, and update user list 
    
    // First, we listen for the event 'update_user_list' emitted by the server. This event is emitted by the function handle_connect() 
    // on the server side and is emitted with the current list of users to ammend to it or update it. we initialize an empty variable
    // string, and then for loop on the users array and then append a list item (<li>) to the userlistHTML containing the usernames. 
    // Finally we update the  user interface to display the current list of connected users.

    socket.on('update_user_list', function(users) {
                var userListHtml = '';
                users.forEach(function(user) {
                    userListHtml += '<li>' + user + '</li>';
                });
                $('#user-list').html(userListHtml);
            });

    // event listener to the element "sendbutton", ie when the button is clicked, it call/runs the sendMessage() function 
    $('#sendbutton').on('click', sendMessage);


    // This is the send message function which is triggered by the when we press the send button, 
    // first it creates a variable for the message written in the input box, and then it triggers the 
    // "send_message" event listener onto the server, sending alongside it the message text. This event listener is
    // then received by handle_send_message(message) function on the server side. Finally we clear the myMessage 
    function sendMessage() {
        var message = $('#myMessage').val();
        socket.emit('send_message', message);
        $('#myMessage').val('');
    }

    // This key press event listener is mainly for improving usability in order to send a message by pressing the enter 
    // key instead of constantly needing to press the send button. Basically it checks if the pressed key is "Enter" which has 
    // key code 13 and then it calls the function sendMessage()
    $('#myMessage').on('keypress', function(e) {
        if(e.which === 13) {
            e.preventDefault(); // Prevent the default form submission on Enter key, without it lead to double messages and error 
            // of sending an empty message along with the original message. 
            sendMessage();
        }
    });

    //This function is used to scroll automically when the chat window is full. It works by selecting the messages and then it 
    // sets the "scrollTop" property of the messages. By setting this scrollTop to scrollHeigjt it scrolls to the buttom of the messages 
    // element.  
    function scrollToEnd() {
        var messages = document.getElementById("messages");
        messages.scrollTop = messages.scrollHeight;
    }

    // We are listening for the event 'broadcast_message'; When the server emits this event, we first retrieve the message content 
    // from the data object by the server. We then convert the timestamp from the date of the data into a string in order to 
    // print it next to the message.
    socket.on('broadcast_message', function(data) {
        var message = data.message;
        var timestamp = new Date(data.timestamp).toLocaleTimeString();
        var messageElement = $('<li>' + message + ' - ' + timestamp + '</li>');
        $("#messages").append(messageElement);
        scrollToEnd();
    });


});
