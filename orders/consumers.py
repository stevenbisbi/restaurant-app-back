from channels.generic.websocket import AsyncWebsocketConsumer  # type: ignore
from asgiref.sync import sync_to_async
import json
from django.core.serializers.json import DjangoJSONEncoder
from .serializers import OrderSerializer

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'order_{self.order_id}'

        try:
            await self.get_order(self.order_id)
        except Exception:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        new_status = data.get('status')

        if new_status:
            try:
                await self.update_order_status(self.order_id, new_status)
            except Exception as e:
                await self.send(text_data=json.dumps({
                    'error': str(e)
                }))
                return

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_order_status',
                }
            )

    async def send_order_status(self, event):
        order = await self.get_order(self.order_id)
        status = await sync_to_async(lambda: OrderSerializer(order).data['status'])()

        await self.send(text_data=json.dumps({
            'status': status,
            'message': 'Order status updated!'
        }, cls=DjangoJSONEncoder))

    @sync_to_async
    def get_order(self, order_id):
        from .models import Order
        return Order.objects.get(id=order_id)

    @sync_to_async
    def update_order_status(self, order_id, new_status):
        from .models import Order
        order = Order.objects.get(id=order_id)

        valid_statuses = dict(Order.STATUS_CHOICES).keys()
        if new_status not in valid_statuses:
            raise ValueError(f"Estado inválido: '{new_status}'")

        order.status = new_status
        order.save()
