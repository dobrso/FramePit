import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class RoomConsumer(WebsocketConsumer):
    room_states = {}

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'room_{self.room_id}'

        if self.room_id not in self.room_states:
            self.room_states[self.room_id] = {
                'video_id': None,
                'is_playing': False,
                'current_time': 0,
                'last_update': None
            }

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.send_current_state()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def send_current_state(self):
        state = self.room_states.get(self.room_id, {})
        if state.get('video_id'):
            self.send(text_data=json.dumps({
                'type': 'video_state',
                'video_id': state['video_id'],
                'is_playing': state['is_playing'],
                'current_time': state['current_time']
            }))

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message_type = data.get('type')
        user = self.scope['user']

        if not user.is_authenticated:
            return

        if message_type == 'video_load':
            video_id = data.get('video_id')
            state = self.room_states.get(self.room_id, {})
            state['video_id'] = video_id
            state['is_playing'] = False
            state['current_time'] = 0
            self.room_states[self.room_id] = state

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'video_action',
                    'action': 'load',
                    'video_id': video_id,
                    'username': user.username
                }
            )

        elif message_type == 'video_play':
            current_time = data.get('current_time')
            state = self.room_states.get(self.room_id, {})
            state['is_playing'] = True
            state['current_time'] = current_time
            self.room_states[self.room_id] = state

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'video_action',
                    'action': 'play',
                    'current_time': current_time,
                    'username': user.username
                }
            )

        elif message_type == 'video_pause':
            current_time = data.get('current_time')
            state = self.room_states.get(self.room_id, {})
            state['is_playing'] = False
            state['current_time'] = current_time
            self.room_states[self.room_id] = state

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'video_action',
                    'action': 'pause',
                    'current_time': current_time,
                    'username': user.username
                }
            )

        elif message_type == 'video_seek':
            current_time = data.get('current_time')
            state = self.room_states.get(self.room_id, {})
            state['current_time'] = current_time
            self.room_states[self.room_id] = state

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'video_action',
                    'action': 'seek',
                    'current_time': current_time,
                    'username': user.username
                }
            )

        elif message_type == 'chat_message':
            message = data.get('message').strip()
            if message:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': f'{user.username}: {message}',
                        'username': user.username
                    }
                )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event.get('username', '')
        }))

    def video_action(self, event):
        self.send(text_data=json.dumps({
            'type': 'video_action',
            'action': event['action'],
            'video_id': event.get('video_id'),
            'current_time': event.get('current_time'),
            'username': event.get('username', '')
        }))