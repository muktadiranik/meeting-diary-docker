from django.apps import AppConfig


class MeetingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "meeting_diary_docker.meetings"

    def ready(self):
        import meeting_diary_docker.meetings.signals
