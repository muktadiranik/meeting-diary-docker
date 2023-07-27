from django.urls import path, include
from rest_framework_nested import routers
from meeting_diary_docker.meetings.views import *

"""
departments/{department_id}/committee/{committee_id}/meetings/{meeting_id}/
departments/{department_id}/members/{member_id}/
"""

"""
/departments/
/departments/{department_id}/
"""
router = routers.DefaultRouter()
router.register('departments', DepartmentViewSet, basename='departments')

"""
/departments/{department_id}/committees/
/departments/{department_id}/committees/{committee_id}/
"""
departments_router = routers.NestedSimpleRouter(
    router, "departments", lookup='department')
departments_router.register(
    'committees', CommitteeViewSet, basename='department-committees')
departments_router.register(
    'members', MemberViewSet, basename='department-members')

"""
/departments/{department_id}/committees/{committee_id}/meetings/
/departments/{department_id}/committees/{committee_id}/meetings/{meeting_id}/
"""
committee_router = routers.NestedSimpleRouter(
    departments_router, "committees", lookup='committee')
committee_router.register('meetings', MeetingViewSet,
                          basename='committee-meetings')


app_name = "api"
urlpatterns = [
    path('', include(router.urls)),
    path('', include(departments_router.urls)),
    path('', include(committee_router.urls)),
]
