const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);
const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);

var loc = window.location;
var wsStart = 'ws://';
if (loc.protocol == 'https:') {
    wsStart = 'wss://'
}
var endpoint = wsStart + '20.207.207.133:8001' + '/ws/' + id + '/';


const socket = new WebSocket(
    endpoint
);

socket.onopen = function(e){
    console.log("CONNECTION ESTABLISHED");
}

socket.onclose = function(e){
    console.log("CONNECTION LOST");
}

socket.onerror = function(e){
    console.log("ERROR OCCURED");
}

socket.onmessage = function(e){
    const data = JSON.parse(e.data);
    if(data.username == message_username){
        document.querySelector('#chat-body').innerHTML += `<tr>
                                                                <td>
                                                                <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">${data.message}</p>
                                                                </td>
                                                            </tr>`
    }else{
        document.querySelector('#chat-body').innerHTML += `<tr>
                                                                <td>
                                                                <p class="bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-left rounded">${data.message}</p>
                                                                </td>
                                                            </tr>`
    }
}

document.querySelector('#chat-message-submit').onclick = function(e){
    const message_input = document.querySelector('#message_input');
    const message = message_input.value;

    socket.send(JSON.stringify({
        'message':message,
        'username':message_username,
        'receiver':receiver
    }));

    message_input.value = '';
}

const messageInput = document.getElementById('message_input');

messageInput.addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        
        event.preventDefault();
        
       const message = messageInput.value.trim();

       if(message !== ''){
            socket.send(JSON.stringify({
                'message' : message,
                'username' : message_username,
                'receiver':receiver
            }))

            messageInput.value = '';
       }
    }
});