import json
from channels.generic.websocket import AsyncWebsocketConsumer
import os
from django import setup
from channels.db import database_sync_to_async
from secrets import token_hex
from typing import Optional

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'remanga_site.settings')
setup()

from remanga.models import User, Comment, Title

class WebsocketConsumer(AsyncWebsocketConsumer):
    connections = dict()

    async def connect(self) -> None:
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        
        self.handlers_websockets = {
            "bookmark": self.handler_websockets_bookmark,
            "comment": self.handler_websockets_comment
        }
        
        await self.accept()
        self.connections[self.session_id] = self
        await self.set_and_send_websockets_csrf_token()

    async def set_and_send_websockets_csrf_token(self) -> None:
        websockets_csrf_token = await self.generate_csrf_token()
        self.scope['websockets_csrf_token'] = websockets_csrf_token

        await self.send(json.dumps({"websockets_csrf_token": websockets_csrf_token}))

    async def generate_csrf_token(self) -> str:
        return token_hex(32)

    async def disconnect(self, close_code) -> None:
        del self.connections[self.session_id]
        
    async def receive(self, text_data) -> None:
        data = json.loads(text_data)
        is_valid_websocket_csrf = await self.is_valid_websocket_csrf(data)
        
        if not is_valid_websocket_csrf: 
            return

        websocket_type = data["type"]
        if websocket_type in self.handlers_websockets:
            await self.handlers_websockets[websocket_type](data)
    
    async def is_valid_websocket_csrf(self, data: dict) -> bool:
        received_websockets_csrf_token = data['websockets_csrf_token']
        stored_websockets_csrf_token = self.scope.get('websockets_csrf_token', 'default_value')

        if received_websockets_csrf_token != stored_websockets_csrf_token:
            await self.close()
            return False 
        
        return True

    async def handler_websockets_bookmark(self, data: dict) -> None:
        """
        Update the title and bookmarks page for the all user sessions
        """                    
        user, title, is_bookmark_added = await self.change_bookmark_in_db(data)
        
        response = {
            "type": data["type"],
            "title_rus_name": title.rus_name,
            "title_dir_name": title.dir_name,
            "title_img_url": title.img_url,
            "is_bookmark_added": not is_bookmark_added,
        }

        await self.one_user_broadcast(response, user.id)

    @database_sync_to_async    
    def change_bookmark_in_db(self, data: dict) -> tuple[Optional[User], Optional[Title], bool]:
        user = User.objects.filter(id=data["user_id"]).first()
        title = Title.objects.filter(id=data["title_id"]).first()        
        is_bookmark_added = user.bookmarks.filter(id=title.id).exists()

        if is_bookmark_added: 
            user.bookmarks.remove(title)
            title.count_bookmarks -= 1
        else: 
            user.bookmarks.add(title)
            title.count_bookmarks += 1

        title.save()

        return user, title, is_bookmark_added

    async def one_user_broadcast(self, response: dict, user_id: int) -> None:
        for session_id in self.connections:
            if session_id.split("-")[0] == str(user_id):
                await self.connections[session_id].send(json.dumps(response))

    async def handler_websockets_comment(self, data: dict) -> None:
        """
        Update title comments for all sessions that are on the title
        """    
        user, title, comment = await self.create_comment_in_db(data)
        user_avatar = "" if not user.avatar else user.avatar.url
        response = {
            "type": data["type"],
            "content": comment.content,
            "user_id": user.id,
            "user_name": user.username,
            "user_avatar": user_avatar,
            "comment_id": comment.id
        }                

        await self.title_broadcast(response, title.id)
    
    @database_sync_to_async    
    def create_comment_in_db(self, data: dict) -> tuple[Optional[User], Optional[Title], Comment]:
        user = User.objects.filter(id=data["user_id"]).first()
        title = Title.objects.filter(id=data["title_id"]).first()

        max_comment_length = 500
        comment_content = data["content"][:max_comment_length]
        comment = Comment.objects.create(author=user, title=title, content=comment_content)

        comment.save()

        return user, title, comment

    async def title_broadcast(self, response: dict, title_id: int) -> None:
        for session_id in self.connections:
            if session_id.split("-")[1] == str(title_id):
                await self.connections[session_id].send(json.dumps(response)) 