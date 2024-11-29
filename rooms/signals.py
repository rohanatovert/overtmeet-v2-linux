from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HomieChatUser, CallNotifications, UserProfileModel, CallModel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@receiver(post_save, sender=CallNotifications)
def send_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        # print(CallNotifications.objects.filter(is_seen=False, user=instance.user))
        notification_obj = CallNotifications.objects.filter(is_seen=False, user=instance.user).count()
        user_id = str(instance.user.id)
        data = {
            'count':notification_obj
        }

        async_to_sync(channel_layer.group_send)(
            user_id, {
                'type':'send_notification',
                'value':json.dumps(data)
            }
        )

@receiver(post_save, sender=CallModel)
def chat_message(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        user = instance.sender
        message = instance.message
        user_id = str(instance.user.id)
        data = {
            'username':user,
            'message':message
        }
        async_to_sync(channel_layer.group_send)(
            user_id, {
                'type':'chat_message',
                'value':json.dumps(data)
            }
        )



@receiver(post_save, sender = UserProfileModel)
def send_online_status(sender, instance, created, **kwargs):
     if not created:
        channel_layer = get_channel_layer()
        user = instance.user.username
        user_status = instance.online_status

        data = {
            'username':user,
            'status':user_status
        }
        async_to_sync(channel_layer.group_send)(
            'user', {
                'type':'send_online_status',
                'value':json.dumps(data)
            }
        )

