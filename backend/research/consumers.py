import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ResearchProgressConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.brief_id = self.scope["url_route"]["kwargs"]["brief_id"]
        self.group_name = f"research-{self.brief_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def progress_update(self, event):
        await self.send(text_data=json.dumps({
            "brief_id": self.brief_id,
            "status": event["status"],
            "progress": event["progress"],
            "message": event.get("message", ""),
        }))
