from django.contrib import admin
from meeting_diary_docker.meetings.models import *

# Register your models here.
admin.site.register(Department)
admin.site.register(Member)
admin.site.register(Committee)
admin.site.register(Meeting)
