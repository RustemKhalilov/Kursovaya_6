from django.contrib import admin
from .models import Client, Mailing, Message, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'comment')
    search_fields = ('name', 'email',)
    list_filter = ('name', 'email',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'periodicity', 'start_date', 'owner', )
    search_fields = ('name',)
    list_filter = ('status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'message')
    search_fields = ('title',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('time', 'status', 'server_response', 'mailing')
    search_fields = ('client',)
    list_filter = ('status',)