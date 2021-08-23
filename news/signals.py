from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Author

@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
    send_mail(
        subject=instance.heading,
        message=instance.content,
        from_email='Sample417@yandex.ru',
        recipient_list=['mugivara18@gmail.com']
    )



