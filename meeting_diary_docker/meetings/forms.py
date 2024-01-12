from ckeditor.widgets import CKEditorWidget
from django import forms
from meeting_diary_docker.meetings.models import *


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"
        exclude = ["user"]


class CommitteeForm(forms.ModelForm):
    class Meta:
        model = Committee
        fields = "__all__"
        exclude = ["department"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CommitteeForm, self).__init__(*args, **kwargs)
        self.fields['member'].queryset = Member.objects.filter(
            department=self.initial["department"])


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = "__all__"
        exclude = ["department"]


class MeetingForm(forms.ModelForm):
    meeting_time = forms.fields.DateTimeField(widget=forms.widgets.DateTimeInput(
        attrs={'type': 'datetime-local'}), required=False)

    class Meta:
        model = Meeting
        fields = "__all__"
        exclude = ["department", "committee", "acknowledged_member",
                   "attended_member"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MeetingForm, self).__init__(*args, **kwargs)
        self.fields['invited_member'].queryset = Member.objects.filter(
            id__in=self.initial["committee"].member.all())
