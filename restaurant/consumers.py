# restaurant/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer # type: ignore
import json
from .tasks import procesar_pedido_async  # Tarea Celery

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.group_name = f'order_{self.order_id}'

        # Autenticación con token JWT (opcional)
        token = self.scope['query_string'].decode().split('=')[1]
        if not self.validar_token(token):
            await self.close()
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Ejecutar tarea Celery y notificar al frontend al finalizar
        procesar_pedido_async.delay(self.order_id, self.group_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_status_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'status': event['status']
        }))

    def validar_token(self, token):
        # Lógica de validación JWT (usa tu librería de autenticación)
        return True  # Implementa esto correctamente