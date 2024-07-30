import smtplib
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from mailing.models import Mailing, Log
from datetime import datetime
import pytz


class Command(BaseCommand):

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status='Запущена')
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)
        for mailing in mailings:
            clients = mailing.clients.all()
            if mailing.next_send_time and current_datetime >= mailing.next_send_time:
                try:
                    server_response = send_mail(
                        subject=mailing.message.title,
                        message=mailing.message.message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email for client in clients],
                        fail_silently=False,
                    )
                    Log.objects.create(status=Log.SUCCESS,
                                       server_response=server_response,
                                       mailing=mailing, )
                except smtplib.SMTPException as e:
                    Log.objects.create(status=Log.FAIL,
                                       server_response=str(e),
                                       mailing=mailing, )
