# In reviews/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Review,UserProfile
from django.contrib.auth.models import User


@receiver(post_save, sender=Review)
def send_review_email_notification(sender, instance, created, **kwargs):
    if created:
        book_title = instance.book.title
       
        recipient_email = 'admin@example.com' 
        
        subject = f'New Review for "{book_title}"'
        message = (
            f'A new review has been posted for the book "{book_title}" by {instance.user.username}.\n\n'
            f'Rating: {instance.rating}/5\n'
            f'Comment: {instance.comment}'
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
        )



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)