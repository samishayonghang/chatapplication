from channels.generic.websocket import WebsocketConsumer
import json
from urllib.parse import parse_qs
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from.models import Codeform

class ChatConsumer(WebsocketConsumer):

    def connect(self):
       
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.group_name = f'room_{self.room_name}' 
        chat_room = Codeform.objects.filter(room_code=self.room_name).first()
        self.username = chat_room.username
        
       
        

        # Add to group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Notify the room that a user has joined
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {
                'type': 'send_status',
                'value': json.dumps({'status': f'{self.username} joined the room'})
            }
        )
        self.accept()

        # Send initial connection confirmation to the client
        self.send(text_data=json.dumps({'message': f'Welcome to room {self.room_name}, {self.username}'}))

    def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message')
            payload = {
                'message': message,
                'sender': self.username,
            }
            print(f"Received: {payload}")

            # Send message to group
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    'type': 'send_message',
                    'value': json.dumps(payload)
                }
            )
        except json.JSONDecodeError:
            self.send(text_data=json.dumps({'error': 'Invalid JSON format'}))
        except Exception as e:
            self.send(text_data=json.dumps({'error': str(e)}))

    def disconnect(self, close_code):
        # Remove from group when the client disconnects
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

        # Notify the room that a user has left
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {
                'type': 'send_status',
                'value': json.dumps({'status': f'{self.username} left the room'})
            }
        )

    def send_message(self, event):
        data = json.loads(event.get('value', '{}'))
        
        # Send message to WebSocket client
        self.send(text_data=json.dumps({
            'message': data['message'],
            'sender': data['sender']
        }))

    def send_status(self, event):
        """Handles status updates like 'online'"""
        self.send(text_data=json.dumps({'payload': event['value']}))
