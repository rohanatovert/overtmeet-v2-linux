const my_username = JSON.parse(document.getElementById('json-message-username').textContent);
const call_receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);
const callid = JSON.parse(document.getElementById('json-username').textContent);

var loc = window.location;
var wsStart = 'ws://';
if (loc.protocol == 'https:') {
    wsStart = 'wss://'
}
var endpoint = wsStart + '20.207.207.133:8001' + '/ws/' + callid + '/call/';

// JavaScript for making a call and handling WebSocket connection

// Function to initiate a call

const call_socket = new WebSocket(
    endpoint
);

call_socket.onopen = function () {
    console.log("CALL CONNECTION ESTABLISHED");
    // WebSocket connection is open, you can now send a call request
    
    
};

call_socket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data.action === 'incoming_call') {
        // Handle incoming call notification, e.g., display a notification to the user
        const fromUser = data.from_user;
        // Implement your notification logic here
        
        showCallNotification(fromUser);
        
        
    };
    if (data.action === 'call_accepted') {
        window.location.href = `https://0.0.0.0:8000/meeting/${data.from_user}-${data.to_user}`;
    }
    if (data.action === 'call_rejected') {
        window.location.reload();
    }
    
};

// Implement other event handlers and logic for accepting and rejecting calls

call_socket.onclose = function () {
    console.log("CALL CONNECTION LOST");
    // WebSocket connection is closed, handle this event if needed
};

call_socket.onerror = function(e){
    console.log("CALL ERROR OCCURED");
};




// Assuming you have an HTML button with the id "call-message-submit"
const callButton = document.querySelector('#call-button-submit');

callButton.onclick = function() {
    // Replace 'toUser' with the username of the user you want to call
    
    call_socket.send(JSON.stringify({
        action: 'call',
        to_user: call_receiver,
    }));
    // Call the makeCall function when the button is clicked
    
};



// JavaScript code for handling the notification
const callNotificationReceiver = document.getElementById('call-notification-receiver');
const callNotificationCaller = document.getElementById('call-notification-caller');
const callerUsername = document.getElementById('caller-username');
const acceptButton = document.getElementById('accept-call');
const rejectButton = document.getElementById('reject-call');
const cancelButton = document.getElementById('cancel-call');
const callMessage = document.getElementById('call-message');

// Function to show the notification with the caller's username
function showCallNotification(username) {
    console.log(my_username, "calling", username);
    if (username===my_username){
        callerUsername.textContent = `Calling ${username}`;
        callNotificationCaller.style.display = 'block';
        console.log(callerUsername);
    }
    else{
        console.log("Incoming");
        callerUsername.textContent = `Incoming Call from ${username}`;
        callNotificationReceiver.style.display = 'block';
    }
};

// Event listener for the accept button
acceptButton.addEventListener('click', function() {
    // Send a socket message to accept the call
    call_socket.send(JSON.stringify({
        action: 'accept_call',
        to_user: callerUsername.textContent,
    }));
    // Hide the notification
    callNotificationReceiver.style.display = 'none';
});

// Event listener for the reject button
rejectButton.addEventListener('click', function() {
    // Send a socket message to reject the call
    call_socket.send(JSON.stringify({
        action: 'reject_call',
        to_user: callerUsername.textContent,
    }));
    // Hide the notification
    callNotificationReceiver.style.display = 'none';
});

// Event listener for the reject button
cancelButton.addEventListener('click', function() {
    // Send a socket message to reject the call
    // Hide the notification
    callNotificationReceiver.style.display = 'none';
    callNotificationCaller.style.display = 'none';
    call_socket.send(JSON.stringify({
        action: 'reject_call',
        to_user: callerUsername.textContent,
    }));
    
});






