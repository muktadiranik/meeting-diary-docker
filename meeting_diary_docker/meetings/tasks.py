from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from meeting_diary_docker.meetings.models import Meeting


@shared_task(bind=True)
def send_invitation_mail_to_invited_members(self, email_list, meeting_id):
    title = Meeting.objects.get(id=meeting_id).title
    description = Meeting.objects.get(id=meeting_id).description
    agenda = Meeting.objects.get(id=meeting_id).agenda
    context = {
        "subject": title,
        "message": f"{title} meeting is scheduled",
        "description": description,
        "agenda": agenda,
    }
    html_message = render_to_string(
        "emails/meeting_invitation.html", context)
    for email in email_list.split(" "):
        send_mail(
            subject=title,
            html_message=html_message,
            message=f"{title} meeting is scheduled",
            from_email="admin@meeting-diary.org",
            recipient_list=[email],
            fail_silently=False,
        )
