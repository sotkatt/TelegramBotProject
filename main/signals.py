from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import TelegramAnswers
from main.bot import support_answer_message


@receiver(post_save, sender=TelegramAnswers)
def send_support_answer_message(sender, instance, created, **kwargs):
    if created:
        support_answer_message(
            instance.questions.user, 
            instance.questions.message, 
            instance.answer
        )
        