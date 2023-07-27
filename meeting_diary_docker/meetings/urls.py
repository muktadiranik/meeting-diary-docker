from django.urls import path
from django.contrib.auth.decorators import login_required
from meeting_diary_docker.meetings.views import *


app_name = "meetings"
urlpatterns = [
    path("", login_required(DepartmentListView.as_view()), name="home"),
    path("delete-department/<int:pk>/",
         login_required(DeleteDepartmentView.as_view()), name="delete_department"),
    path("update-department/<int:pk>/",
         login_required(UpdateDepartmentView.as_view()), name="update_department"),
    path("department-detail/<int:pk>/",
         login_required(DepartmentDetailView.as_view()), name="department_detail"),
    path("committee-detail/<int:committee_pk>/",
         login_required(CommitteeDetailView.as_view()), name="committee_detail"),
    path("delete-committee/<int:committee_pk>/",
         login_required(DeleteCommitteeView.as_view()), name="delete_committee"),
    path("update-committee/<int:committee_pk>/",
         login_required(UpdateCommitteeView.as_view()), name="update_committee"),
    path("committee-detail/<int:committee_pk>/add-meeting/",
         login_required(AddMeetingView.as_view()), name="add_meeting"),
    path("committee-detail/<int:committee_pk>/delete-meeting/<int:meeting_pk>/",
         login_required(DeleteMeetingView.as_view()), name="delete_meeting"),
    path("committee-detail/<int:committee_pk>/update-meeting/<int:meeting_pk>/",
         login_required(UpdateMeetingView.as_view()), name="update_meeting"),
    path("meeting-detail/<int:meeting_pk>/",
         login_required(MeetingDetailView.as_view()), name="meeting_detail"),
    path("add-member/",
         login_required(AddMemberView.as_view()), name="add_member"),
    path("delete-member/<int:member_pk>/",
         login_required(DeleteMemberView.as_view()), name="delete_member"),
    path("update-member/<int:member_pk>/",
         login_required(UpdateMemberView.as_view()), name="update_member"),
]
