from django.contrib import admin

from .models import HomieChatUser, UserProfileModel, Room, Video, File, Order, CallModel, CallNotifications,TranscriptsAndSummaries

# Register your models here.

admin.site.register(HomieChatUser)
admin.site.register(UserProfileModel)
admin.site.register(Room)
admin.site.register(Video)
admin.site.register(File)
admin.site.register(Order)
admin.site.register(CallModel)
admin.site.register(CallNotifications)
admin.site.register(TranscriptsAndSummaries)