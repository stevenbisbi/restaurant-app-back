# restaurant/tasks.py
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.core.mail import send_mail

import time

import logging
logger = logging.getLogger(__name__)

@shared_task
def procesar_pedido_async(order_id, group_name):
    try:
    
    # Simula un proceso largo (ej: 10 segundos)
        time.sleep(10)

        # Notificar vía WebSocket al finalizar
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_status_update',
                'status': 'Pedido listo'
            }
        )
        logger.info(f"Pedido {order_id} procesado y notificado.")
    except Exception as e:
        logger.error(f"Error procesando pedido {order_id}: {str(e)}")
        raise
    
@shared_task
def enviar_correo_confirmacion(destinatario, asunto, mensaje):
    try:
        send_mail(
            asunto,
            mensaje,
            "noreply@restaurantos.com",
            [destinatario],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Error enviando correo a {destinatario}: {str(e)}")
        raise  # Opcional: Re-lanza la excepción para reintentos