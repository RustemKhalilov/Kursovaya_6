from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import (HomeView, ClientListView, ClientCreateView, ClientDeleteView, ClientUpdateView,
                           ClientDetailView, MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView,
                           MessageDetailView, MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView,
                           MailingDetailView, LogListView)

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('create/', ClientCreateView.as_view(), name='create'),
    path('clients_list/', ClientListView.as_view(), name='clients_list'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='edit'),
    path('view/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='view'),
    path('messages_list/', MessageListView.as_view(), name='messages_list'),
    path('message_create/', MessageCreateView.as_view(), name='create_message'),
    path('message_view/<int:pk>/', cache_page(60)(MessageDetailView.as_view()), name='view_message'),
    path('message_edit/<int:pk>/', MessageUpdateView.as_view(), name='edit_message'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),
    path('mailings_list/', MailingListView.as_view(), name='mailings_list'),
    path('mailing_create/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing_view/<int:pk>/', MailingDetailView.as_view(), name='view_mailing'),
    path('mailing_edit/<int:pk>/', MailingUpdateView.as_view(), name='edit_mailing'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('logs_list/', LogListView.as_view(), name='logs_list'),
]