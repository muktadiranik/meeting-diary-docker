from django.db import models
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField

User = get_user_model()

# Create your models here.


class Department(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = HTMLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Member(models.Model):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    primary_phone = models.CharField(max_length=255, blank=True, null=True)
    secondary_phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Committee(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = HTMLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    member = models.ManyToManyField(Member, blank=True)

    def __str__(self):
        return str(self.id)


class Meeting(models.Model):
    committee = models.ForeignKey(
        Committee, on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = HTMLField(blank=True, null=True)
    content = HTMLField(blank=True, null=True)
    meeting_time = models.DateTimeField(blank=True, null=True)
    invited_member = models.ManyToManyField(
        Member, related_name='invited_member', blank=True)
    acknowledged_member = models.ManyToManyField(
        Member, related_name='acknowledged_member', blank=True)
    attended_member = models.ManyToManyField(
        Member, related_name='attended_member', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
