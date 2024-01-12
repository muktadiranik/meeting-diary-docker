from django.db.models.signals import post_save
from django.dispatch import receiver
from meeting_diary_docker.meetings.models import Meeting
from meeting_diary_docker.meetings.tasks import send_invitation_mail_to_invited_members


@receiver(post_save, sender=Meeting)
def send_invitation_mail(sender, **kwargs):
    pass
