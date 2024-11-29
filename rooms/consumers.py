# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# import asyncio

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):

#         self.room_group_name = self.scope['url_route']['kwargs']['room_code']

#         print('self.room_group_name: ', self.room_group_name)

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
        
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#         print('Disconnected!')
        

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         receive_dict = json.loads(text_data)
#         peer_username = receive_dict['peer']
#         action = receive_dict['action']
#         message = receive_dict['message']

#         # print('unanswered_offers: ', self.unanswered_offers)

#         print('Message received: ', message)

#         print('peer_username: ', peer_username)
#         print('action: ', action)
#         print('self.channel_name: ', self.channel_name)

#         if(action == 'new-offer') or (action =='new-answer'):
#             # in case its a new offer or answer
#             # send it to the new peer or initial offerer respectively

#             receiver_channel_name = receive_dict['message']['receiver_channel_name']

#             print('Sending to ', receiver_channel_name)

#             # set new receiver as the current sender
#             receive_dict['message']['receiver_channel_name'] = self.channel_name

#             await self.channel_layer.send(
#                 receiver_channel_name,
#                 {
#                     'type': 'send.sdp',
#                     'receive_dict': receive_dict,
#                 }
#             )

#             return

#         # set new receiver as the current sender
#         # so that some messages can be sent
#         # to this channel specifically
#         receive_dict['message']['receiver_channel_name'] = self.channel_name

#         # send to all peers
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'send.sdp',
#                 'receive_dict': receive_dict,
#             }
#         )

#     async def send_sdp(self, event):
#         receive_dict = event['receive_dict']

#         this_peer = receive_dict['peer']
#         action = receive_dict['action']
#         message = receive_dict['message']

#         await self.send(text_data=json.dumps({
#             'peer': this_peer,
#             'action': action,
#             'message': message,
#         }))


# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.db import database_sync_to_async
from .models import CallModel, HomieChatUser, UserProfileModel, CallNotifications
from asgiref.sync import async_to_sync 

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # async_to_sync(self.channel_layer.group_add){
        #     self.room_name, self.room_group_name
        # }

        await self.accept()
        await self.send(text_data=json.dumps({"status":"connected"}))
        

    

    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        print("Personal Chat Data Received:",data)
        message = data['message']
        username = data['username']
        receiver = data['receiver']

        await self.save_message(username, self.room_group_name, message, receiver)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        print("Chat Handler")
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))


    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, username, thread_name, message, receiver):
        chat_obj = CallModel.objects.create(
            sender=username, message=message, thread_name=thread_name)
        other_user_id = self.scope['url_route']['kwargs']['id']
        get_user = HomieChatUser.objects.get(id=other_user_id)
        if receiver == get_user.username:
            CallNotifications.objects.create(chat=chat_obj, user=get_user)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        
        # print("Starting websocket!!")
        my_id = self.scope['user'].id
        self.room_group_name = f'{my_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
            )
        
        await self.accept()
        self.send(text_data = json.dumps({
            'type':'connection_established',
            'message':'You are now connected!'
        }))

    async def disconnect(self, close_code):
        # Disconnect the WebSocket
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.disconnect()

    async def send_notification(self, event):
        data = json.loads(event.get('value'))
        count = data['count']
        await self.send(text_data=json.dumps({
            'count':count
        }))



class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Accepting!")
        self.room_group_name = 'user'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'tester_message',
                'tester': 'hello world',
            }
        )

    async def receive(self, text_data = None, bytes_data = None):
        print("DATA RECEIVED:")
        data = json.loads(text_data)
        username = data['username']
        connection_type = data['type']
        print("Username:", username, "Connection Type:", connection_type)
        await self.change_online_status(username, connection_type)
    
    async def send_online_status(self, event):
        data = json.loads(event.get('value'))
        username = data['username']
        online_status = data['status']
        await self.send(text_data = json.dumps(
            {
                'username':username,
                'online_status':online_status
            }
        ))
    
    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # await self.disconnect()
    
    @database_sync_to_async
    def change_online_status(self, username, c_type):
        user = HomieChatUser.objects.get(username=username)
        userprofile = UserProfileModel.objects.get(user=user)
        if c_type == 'open':
            userprofile.online_status = True
            userprofile.save()
        else:
            userprofile.online_status = False
            userprofile.save()
            


class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Handle WebSocket connection here
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
       

    async def disconnect(self, close_code):
        # Handle WebSocket disconnection here
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']
        print("CALLING DATA:",data)
        from_user = self.scope['user'].username  # Assuming user is authenticated
        to_user = data['to_user']
        if action == 'call':
            # Handle a call request, notify the other user
            

            # You can implement logic to determine if the call is accepted or rejected
            # For this example, we'll assume it's always accepted
            response_data = {
                'action': 'incoming_call',
                'from_user': from_user,
                'to_user': to_user,
            }
            

        # Implement similar methods for accepting and rejecting calls
        elif action == 'accept_call':
            # Handle accepting the call
            
            # Implement your logic for accepting the call
            # You can send a response to the caller that the call has been accepted
            response_data = {
                'action': 'call_accepted',
                'from_user': from_user,
                'to_user': to_user,
            }

        elif action == 'reject_call':
            # Handle rejecting the call
            
            # Implement your logic for rejecting the call
            # You can send a response to the caller that the call has been rejected
            response_data = {
                'action': 'call_rejected',
                'from_user': from_user,
                'to_user': to_user,
            }

        # await self.send(text_data=json.dumps(response_data))
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_notification_message',
                'message': response_data
            }
        )

    async def call_notification_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
        


class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.room_group_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status':'connected'}))