# Generated by Django 4.2.2 on 2024-01-12 10:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("meetings", "0004_content_remove_meeting_content_meeting_content"),
    ]

    operations = [
        migrations.RenameField(
            model_name="meeting",
            old_name="content",
            new_name="agenda",
        ),
    ]