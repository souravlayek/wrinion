# import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model


from .models import ChatMessage, Thread


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']

        thread_obj = await self.get_thread(me, other_user)
        chat_room = f"thread_{thread_obj.id}"
        self.thread_obj = thread_obj
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )


    async def websocket_receive(self, event):
        # print("receive", event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
        user = self.scope['user']
        username = 'default'
        if user.is_authenticated:
            username = user.username

        myResponse = {
            'message': msg,
            'username': username
        }
        await self.create_chat_message(user, msg)
        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type": "chat_message",
                "text": json.dumps(myResponse)
            }
        )


    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)
        await self.channel_layer.group_discard(
            self.chat_room, 
            self.channel_name
        )


    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def create_chat_message(self, user, msg):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj ,user=user, message=msg)
