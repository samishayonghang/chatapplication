from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.group_name = f'room_{self.room_name}'
        
        # Add to group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

        # Notify the room that a user has joined
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {
                'type': 'send_status',
                'value': json.dumps({'status': 'online'})
            }
        )

        # Send initial connection confirmation to the client
        self.send(text_data=json.dumps({'payload': 'connected'}))

    def receive(self, text_data):
        try:
            data = json.loads(text_data)
            payload = {
                'message': data.get('message'),
                'sender': data.get('sender')
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

    def disconnect(self, close_code):
        # Remove from group when the client disconnects
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def send_message(self, event):
        data = json.loads(event.get('value', '{}'))
        
        # Send message to WebSocket client
        self.send(text_data=json.dumps({'payload': data}))

    def send_status(self, event):
        """Handles status updates like 'online'"""
        self.send(text_data=json.dumps({'payload': event['value']}))
