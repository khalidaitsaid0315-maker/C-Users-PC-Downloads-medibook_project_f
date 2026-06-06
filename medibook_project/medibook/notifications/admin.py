from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('rendez_vous', 'type_notification', 'envoye_le', 'statut_succes')
    list_filter = ('type_notification', 'statut_succes')

# Register your models here.
