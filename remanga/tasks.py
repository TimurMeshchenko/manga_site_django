from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_async_email(subject: str, message: str, from_email: str, recipient_list: list) -> None:
    send_mail(subject, message, from_email, recipient_list, html_message=message)