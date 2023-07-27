from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from django.db.models import Q, F, Value, Func
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from meeting_diary_docker.meetings.models import *
from meeting_diary_docker.meetings.forms import *
from meeting_diary_docker.meetings.serializers import *
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


class DepartmentListView(View):
    def get(self, request):
        if request.GET.get('search_department'):
            departments = Department.objects.filter(user=self.request.user.id).\
                filter(Q(description__icontains=request.GET.get('search_department'))
                       |
                       Q(title__icontains=request.GET.get('search_department'))).\
                prefetch_related('committee_set').\
                prefetch_related("member_set").\
                prefetch_related("meeting_set").\
                order_by('-created_at')
        else:
            departments = Department.objects.filter(user=self.request.user.id).\
                prefetch_related('committee_set').\
                prefetch_related("member_set").\
                prefetch_related("meeting_set").\
                order_by('-created_at')
        add_department_form = DepartmentForm()
        return render(request, 'meetings/home.html', {
            'departments': departments,
            'add_department_form': add_department_form
        })

    def post(self, request):
        add_department_form = DepartmentForm(request.POST)
        if add_department_form.is_valid():
            department = add_department_form.save(commit=False)
            department.user = self.request.user
            department.save()
        return redirect('meetings:home')


class UpdateDepartmentView(View):
    def get(self, request, pk):
        department = Department.objects.get(pk=pk)
        update_department_form = DepartmentForm(instance=department)
        return render(request, 'meetings/update_department.html', {
            'department': department,
            'update_department_form': update_department_form
        })

    def post(self, request, pk):
        department = Department.objects.get(pk=pk)
        update_department_form = DepartmentForm(
            request.POST, instance=department)
        if update_department_form.is_valid():
            update_department_form.save()
        return redirect('meetings:home')


class DeleteDepartmentView(View):
    def get(self, request, pk):
        department = Department.objects.get(pk=pk)
        department.delete()
        return redirect('meetings:home')


class DepartmentDetailView(View):
    def get(self, request, pk):
        department = Department.objects.get(pk=pk)
        if self.request.GET.get('search_committee'):
            committes = Committee.objects.filter(department=department).\
                filter(Q(title__icontains=self.request.GET.get('search_committee'))
                       |
                       Q(description__icontains=self.request.GET.get('search_committee'))).\
                prefetch_related("meeting_set")
        else:
            committes = Committee.objects.filter(
                department=department).prefetch_related("meeting_set")
        if self.request.GET.get('search_member'):
            members = Member.objects.filter(department=department).annotate(full_name=Func(F("first_name"), Value(
                " "), F("last_name"), function="CONCAT")).\
                filter(Q(first_name__icontains=self.request.GET.get('search_member'))
                       |
                       Q(last_name__icontains=self.request.GET.get('search_member'))
                       |
                       Q(email__icontains=self.request.GET.get('search_member'))
                       |
                       Q(primary_phone__icontains=self.request.GET.get('search_member'))
                       |
                       Q(secondary_phone__icontains=self.request.GET.get(
                           'search_member'))
                       |
                       Q(designation__icontains=self.request.GET.get('search_member'))
                       |
                       Q(address__icontains=self.request.GET.get('search_member'))
                       |
                       Q(full_name__icontains=self.request.GET.get('search_member')))
        else:
            members = Member.objects.filter(department=department)
        add_member_form = MemberForm()
        add_committee_form = CommitteeForm(request=self.request, initial={
                                           'department': department})
        return render(request, 'meetings/department_detail.html', {
            'department': department,
            "committees": committes,
            "members": members,
            "add_member_form": add_member_form,
            'add_committee_form': add_committee_form,
        })

    def post(self, request, pk):
        department = Department.objects.get(pk=pk)
        add_committee_form = CommitteeForm(
            request.POST, request=self.request, initial={'department': department})
        if add_committee_form.is_valid():
            committee = add_committee_form.save(commit=False)
            committee.department = department
            committee.save()
        return redirect('meetings:department_detail', pk=department.pk)


class UpdateCommitteeView(View):
    def get(self, request, committee_pk):
        committee = Committee.objects.get(pk=committee_pk)
        update_committee_form = CommitteeForm(instance=committee, initial={
                                              'department': committee.department})
        return render(request, 'meetings/update_committee.html', {
            'committee': committee,
            'update_committee_form': update_committee_form
        })

    def post(self, request, committee_pk):
        committee = Committee.objects.get(pk=committee_pk)
        update_committee_form = CommitteeForm(request.POST, instance=committee, initial={
            'department': committee.department})
        if update_committee_form.is_valid():
            update_committee_form.save()
        return redirect('meetings:department_detail', pk=committee.department.pk)


class DeleteCommitteeView(View):
    def get(self, request, committee_pk):
        committee = Committee.objects.get(pk=committee_pk)
        pk = committee.department.pk
        committee.delete()
        return redirect('meetings:department_detail', pk=pk)


class CommitteeDetailView(View):
    def get(self, request, committee_pk):
        committee = Committee.objects.get(pk=committee_pk)
        if self.request.GET.get('search_meeting'):
            meetings = Meeting.objects.filter(committee=committee).\
                filter(Q(title__icontains=self.request.GET.get('search_meeting'))
                       |
                       Q(description__icontains=self.request.GET.get('search_meeting'))
                       |
                       Q(content__icontains=self.request.GET.get('search_meeting'))
                       |
                       Q(status__icontains=self.request.GET.get('search_meeting'))
                       |
                       Q(meeting_type__title__icontains=self.request.GET.get('search_meeting')))
        else:
            meetings = Meeting.objects.filter(committee=committee)
        return render(request, 'meetings/committee_detail.html', {
            'committee': committee,
            'meetings': meetings,
        })


class AddMeetingView(View):
    def get(self, request, committee_pk):
        committee = Committee.objects.get(pk=committee_pk)
        add_meeting_form = MeetingForm(request=self.request, initial={
                                       'committee': committee})
        add_member_form = MemberForm()
        return render(request, 'meetings/add_meeting.html', {
            'committee': committee,
            'add_meeting_form': add_meeting_form,
            'add_member_form': add_member_form,
        })

    def post(self, request, committee_pk):
        committee = Committee.objects.get(pk=committee_pk)
        add_meeting_form = MeetingForm(request.POST, request=self.request, initial={
                                       'committee': committee})
        if add_meeting_form.is_valid():
            meeting = add_meeting_form.save(commit=False)
            meeting.committee = committee
            meeting.department = committee.department
            meeting.save()
            meeting.invited_member.set(
                add_meeting_form.cleaned_data['invited_member'])
            send_mail(
                meeting.title,
                meeting.content,
                'from@example.com',
                [i.email for i in meeting.invited_member.all()],
                fail_silently=False,
            )
        return redirect('meetings:committee_detail', committee_pk=committee.pk)


class UpdateMeetingView(View):
    def get(self, request, committee_pk, meeting_pk):
        committee = Committee.objects.get(pk=committee_pk)
        meeting = Meeting.objects.get(pk=meeting_pk)
        add_member_form = MemberForm()
        update_meeting_form = MeetingForm(
            instance=meeting, request=self.request, initial={'committee': committee})
        return render(request, 'meetings/update_meeting.html', {
            'committee': committee,
            'meeting': meeting,
            'add_member_form': add_member_form,
            'update_meeting_form': update_meeting_form
        })

    def post(self, request, committee_pk, meeting_pk):
        committee = Committee.objects.get(pk=committee_pk)
        meeting = Meeting.objects.get(pk=meeting_pk)
        update_meeting_form = MeetingForm(request.POST, instance=meeting,
                                          request=self.request, initial={'committee': committee})
        if update_meeting_form.is_valid():
            update_meeting_form.save()
        return redirect('meetings:committee_detail', committee_pk=meeting.committee.pk)


class DeleteMeetingView(View):
    def get(self, request, committee_pk, meeting_pk):
        meeting = Meeting.objects.get(pk=meeting_pk)
        meeting.delete()
        return redirect('meetings:committee_detail', committee_pk=committee_pk)


class MeetingDetailView(View):
    def get(self, request,  meeting_pk):
        meeting = Meeting.objects.get(pk=meeting_pk)
        return render(request, 'meetings/meeting_detail.html', {
            'meeting': meeting,
            "committee": meeting.committee,
        })


class AddMemberView(View):
    def get(self, request):
        add_member_form = MemberForm()
        return render(request, 'meetings/add_member.html', {
            'add_member_form': add_member_form
        })

    def post(self, request):
        add_member_form = MemberForm(request.POST)
        if add_member_form.is_valid():
            member = add_member_form.save(commit=False)
            if "department" in request.META.get('HTTP_REFERER'):
                member.department = Department.objects.get(
                    pk=request.META.get('HTTP_REFERER').split('/')[-2])
            if "committee" in request.META.get('HTTP_REFERER'):
                member.department = Committee.objects.get(
                    pk=request.META.get('HTTP_REFERER').split('/')[-3]).department
            member.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class UpdateMemberView(View):
    def get(self, request,  member_pk):
        member = Member.objects.get(pk=member_pk)
        update_member_form = MemberForm(instance=member)
        return render(request, 'meetings/update_member.html', {
            'member': member,
            'update_member_form': update_member_form
        })

    def post(self, request, member_pk):
        member = Member.objects.get(pk=member_pk)
        update_member_form = MemberForm(request.POST, instance=member)
        if update_member_form.is_valid():
            update_member_form.save()

        return redirect('meetings:department_detail', pk=member.department.id)


class DeleteMemberView(View):
    def get(self, request,  member_pk):
        member = Member.objects.get(pk=member_pk)
        member.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# API Views
class SearchAPIView(APIView):
    def get(self, request):
        if request.GET.get("search"):
            search = request.GET.get("search")
            if request.user.is_superuser:
                departments = Department.objects.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(user__first_name__icontains=search) |
                    Q(user__last_name__icontains=search) |
                    Q(user__email__icontains=search) |
                    Q(user__username__icontains=search)
                ).order_by("-id")
                committees = Committee.objects.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(department__title__icontains=search) |
                    Q(department__description__icontains=search) |
                    Q(department__user__first_name__icontains=search) |
                    Q(department__user__last_name__icontains=search) |
                    Q(department__user__email__icontains=search) |
                    Q(department__user__username__icontains=search)
                ).order_by("-id")
                members = Member.objects.filter(
                    Q(full_name__icontains=search) |
                    Q(primary_phone__icontains=search) |
                    Q(secondary_phone__icontains=search) |
                    Q(email__icontains=search) |
                    Q(address__icontains=search) |
                    Q(designation__icontains=search) |
                    Q(department__title__icontains=search) |
                    Q(department__description__icontains=search) |
                    Q(department__user__first_name__icontains=search) |
                    Q(department__user__last_name__icontains=search) |
                    Q(department__user__email__icontains=search) |
                    Q(department__user__username__icontains=search)
                ).order_by("-id")
                meetings = Meeting.objects.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(content__icontains=search) |
                    Q(department__title__icontains=search) |
                    Q(department__description__icontains=search) |
                    Q(department__user__first_name__icontains=search) |
                    Q(department__user__last_name__icontains=search) |
                    Q(department__user__email__icontains=search) |
                    Q(department__user__username__icontains=search)
                ).order_by("-id")
                return Response({
                    "departments": SimpleDepartmentSerializer(departments, many=True).data,
                    "committees": SimpleCommitteeSerializer(committees, many=True).data,
                    "members": SimpleMemberSerializer(members, many=True).data,
                    "meetings": SimpleMeetingSerializer(meetings, many=True).data,
                })
            departments = Department.objects.filter(user=request.user.id).filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(user__username__icontains=search)
            ).order_by("-id")
            committees = Committee.objects.filter(department__user_id=request.user.id).ffilter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(department__title__icontains=search) |
                Q(department__description__icontains=search) |
                Q(department__user__first_name__icontains=search) |
                Q(department__user__last_name__icontains=search) |
                Q(department__user__email__icontains=search) |
                Q(department__user__username__icontains=search)
            ).order_by("-id")
            members = Member.objects.filter(department__user_id=request.user.id).filter(
                Q(full_name__icontains=search) |
                Q(primary_phone__icontains=search) |
                Q(secondary_phone__icontains=search) |
                Q(email__icontains=search) |
                Q(address__icontains=search) |
                Q(designation__icontains=search) |
                Q(department__title__icontains=search) |
                Q(department__description__icontains=search) |
                Q(department__user__first_name__icontains=search) |
                Q(department__user__last_name__icontains=search) |
                Q(department__user__email__icontains=search) |
                Q(department__user__username__icontains=search)
            ).order_by("-id")
            meetings = Meeting.objects.filter(department__user_id=request.user.id).filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(content__icontains=search) |
                Q(department__title__icontains=search) |
                Q(department__description__icontains=search) |
                Q(department__user__first_name__icontains=search) |
                Q(department__user__last_name__icontains=search) |
                Q(department__user__email__icontains=search) |
                Q(department__user__username__icontains=search)
            ).order_by("-id")
            return Response({
                "departments": SimpleDepartmentSerializer(departments, many=True).data,
                "committees": SimpleCommitteeSerializer(committees, many=True).data,
                "members": SimpleMemberSerializer(members, many=True).data,
                "meetings": SimpleMeetingSerializer(meetings, many=True).data,
            })
        if request.user.is_superuser:
            departments = Department.objects.all().order_by("-id")
            committees = Committee.objects.all().order_by("-id")
            members = Member.objects.all().order_by("-id")
            meetings = Meeting.objects.all().order_by("-id")
            return Response({
                "departments": SimpleDepartmentSerializer(departments, many=True).data,
                "committees": SimpleCommitteeSerializer(committees, many=True).data,
                "members": SimpleMemberSerializer(members, many=True).data,
                "meetings": SimpleMeetingSerializer(meetings, many=True).data,
            })
        departments = Department.objects.filter(
            user=request.user.id).order_by("-id")
        committees = Committee.objects.filter(
            department__user_id=request.user.id).order_by("-id")
        members = Member.objects.filter(
            department__user_id=request.user.id).order_by("-id")
        meetings = Meeting.objects.filter(
            department__user_id=request.user.id).order_by("-id")
        return Response({
            "departments": SimpleDepartmentSerializer(departments, many=True).data,
            "committees": SimpleCommitteeSerializer(committees, many=True).data,
            "members": SimpleMemberSerializer(members, many=True).data,
            "meetings": SimpleMeetingSerializer(meetings, many=True).data,
        })


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title", "description"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Department.objects.all().prefetch_related("committee_set").prefetch_related("member_set").order_by("-id")
        return Department.objects.filter(user=self.request.user.id).prefetch_related("committee_set").order_by("-id")


class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_backends = [SearchFilter]
    search_fields = ["full_name", "primary_phone",
                     "secondary_phone", "email",
                     "address", "designation"]

    def get_queryset(self):
        return Member.objects.filter(department=self.kwargs["department_pk"]).order_by("-id")

    def get_serializer_context(self):
        return {"department_pk": self.kwargs["department_pk"]}


class CommitteeViewSet(ModelViewSet):
    serializer_class = CommitteeSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Committee.objects.filter(department=self.kwargs["department_pk"]).order_by("-id")

    def get_serializer_context(self):
        return {"department_pk": self.kwargs["department_pk"]}


class MeetingViewSet(ModelViewSet):
    serializer_class = MeetingSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title", "description",
                     "content", "meeting_time"]

    def get_queryset(self):
        return Meeting.objects.filter(department=self.kwargs["department_pk"], committee=self.kwargs["committee_pk"]).order_by("-id")

    def get_serializer_context(self):
        return {"department_pk": self.kwargs["department_pk"], "committee_pk": self.kwargs["committee_pk"]}
