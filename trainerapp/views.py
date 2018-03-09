# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
import datetime

from .models import Team, UserPackage, Keeper, Session, Attendance

from .forms import UserChangeForm, AddTeam, DeleteTeam, AddPackage, AddKeeper, EditKeeper, DeleteKeeper
from .forms import AddSession, EditSession, DeleteSession, AddAttendance, EditAttendance, DeleteAttendance


def heroku(request):
    return HttpResponse('Successful Heroku deploy')


def index(request):
    teams = Team.objects.filter(trainer=request.user, status=1)
    packages = UserPackage.objects.all()
    context = {
        'teams': teams,
        'packages': packages,
    }
    return render(request, 'base.html', context)


def account_settings(request):
    model = get_user_model()
    return render(request, 'account/account_detail.html', {'model': model})


def edit_account(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deine Kontoeinstellungen wurden erfolgreich gespeichert!')
            return redirect('index')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'account/edit_account.html', {'form': form})


def new_team(request):
    if request.method == "POST":
        team_form = AddTeam(request.POST)
        if team_form.is_valid():
            team = team_form.save(commit=False)
            team.trainer = request.user
            team.edited_date = timezone.now()
            team.save()
            for package_id in range (1,4):
                package = UserPackage(trainer=request.user,team_id=team.pk,package_id=package_id,active=True)
                package.save()
            messages.success(request, 'Bravo, das Team wurde erstellt, nun kannst du Torhüter hinzufügen!')
            return redirect('index')
    else:
        team_form = AddTeam()
    return render(request, 'team/new_team.html', {'team_form': team_form})


def edit_team(request, team_pk):
    team = get_object_or_404(Team, pk=team_pk)
    if request.method == "POST":
        form = AddTeam(request.POST, instance=team)
        if form.is_valid():
            team = form.save(commit=False)
            team.trainer = request.user
            team.edited_date = timezone.now()
            team.save()
            messages.success(request, 'Das Team wurde erfolgreich geändert!')
            return redirect('index')
    else:
        form = AddTeam(instance=team)
    return render(request, 'team/edit_team.html', {'form': form})


def delete_team(request, team_pk):
    team = get_object_or_404(Team, pk=team_pk)
    if request.method == 'POST':
        form = DeleteTeam(request.POST, instance=team)
        if form.is_valid():
            team = form.save(commit=False)
            team.status = 0
            team.save()
            messages.success(request, 'Das Team wurde erfolgreich gelöscht!')
            return redirect('index')
    else:
        form = DeleteTeam(instance=team)
    return render(request, 'team/delete_team.html', {'form': form})


# Here are all Keeper Views, Overview, Detail, Add Form, Edit Form, Delete Form

def select_package(request, team_pk, package_pk):
    package = get_object_or_404(UserPackage, package_id=package_pk, team_id=team_pk)
    team = get_object_or_404(Team, id=team_pk)
    if package.package.pk == 1:
        keepers = Keeper.objects.filter(team=team, status=1)
        context = {
            'team': team,
            'package': package,
            'keepers': keepers,
        }
        return render(request, 'keeper/keeper_overview.html', context)
    elif package.package.pk == 2:
        today = datetime.datetime.today()
        sessions = Session.objects.filter(team=team, status=1, date__month=today.month)
        context = {
            'team': team,
            'package': package,
            'sessions': sessions,
            'today': today,
        }
        return render(request, 'session/session_overview.html', context)
    elif package.package.pk == 3:
        attendance = Attendance.objects.filter(team=team)
        context = {
            'team': team,
            'package': package,
            'attendance': attendance,
        }
        return render(request, 'attendance/attendance_overview.html', context)


def keeper_detail(request, keeper_pk, team_pk, package_pk):
    keeper = get_object_or_404(Keeper, pk=keeper_pk)
    team = get_object_or_404(Team, pk=team_pk)
    package = UserPackage(pk=package_pk)
    context = {
        'keeper': keeper,
        'team': team,
        'package': package,
    }
    return render(request, 'keeper/keeper_detail.html', context)


def new_keeper(request, team_pk, package_pk):
    if request.method == "POST":
        form = AddKeeper(request.POST, request.FILES)
        if form.is_valid():
            keeper = form.save(commit=False)
            keeper.trainer = request.user
            keeper.team = get_object_or_404(Team, pk=team_pk)
            keeper.created_date = timezone.now()
            keeper.save()
            messages.success(request, 'Klasse, dein Torhüter wurde erfolgreich erfasst!')
            return redirect(reverse('keeper_detail', args=[package_pk, team_pk, keeper.pk]))
    else:
        form = AddKeeper()
    return render(request, 'keeper/new_keeper.html', {'form': form})


def upload_avatar(request):
    if request.method == "POST" and request.FILES('avatar_image'):
        avatar_image = request.FILES['avatar_image']
        fs = FileSystemStorage()
        filename = fs.save(avatar_image.name, avatar_image)
        uploaded_file_url = fs.url(filename)
        if 'new_keeper' in request.POST:
            return render(request, 'keeper/new_keeper.html',{'uploaded_file_url': uploaded_file_url})
        elif 'edit_keeper' in request.POST:
            return render(request, 'keeper/edit_keeper.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'keeper/new_keeper.html')


def edit_keeper(request, keeper_pk, team_pk, package_pk):
    keeper = get_object_or_404(Keeper, pk=keeper_pk)
    if request.method == "POST":
        form = EditKeeper(request.POST, request.FILES, instance=keeper)
        if form.is_valid():
            keeper = form.save(commit=False)
            keeper.edited_date = timezone.now()
            keeper.save()
            messages.success(request, 'Die Änderungen am Torhüter wurden gespeichert!')
            return redirect(reverse('keeper_detail', args=[package_pk, team_pk, keeper_pk]))
    else:
        form = EditKeeper(instance=keeper)
    context = {
        'keeper': keeper,
        'form': form,
    }
    return render(request, 'keeper/edit_keeper.html', context)


def delete_keeper(request, keeper_pk, team_pk, package_pk):
    keeper = get_object_or_404(Keeper, pk=keeper_pk)
    if request.method == "POST":
        form = DeleteKeeper(request.POST, instance=keeper)
        if form.is_valid():
            keeper = form.save(commit=False)
            keeper.edited_date = timezone.now()
            keeper.status = 0
            keeper.save()
            messages.success(request, 'Der Torhüter wurde erfolgreich gelöscht!')
            return redirect(reverse('select_package', args=[package_pk, team_pk]))
    else:
        form = DeleteKeeper(instance=keeper)
    context = {
        'keeper': keeper,
        'form': form,
    }
    return render(request, 'keeper/delete_keeper.html', context)


# Session Views
def session_detail(request, session_pk, team_pk, package_pk):
    session = get_object_or_404(Session, pk=session_pk)
    team = get_object_or_404(Team, pk=team_pk)
    package = UserPackage(pk=package_pk)
    context = {
        'session' : session,
        'team': team,
        'package': package,
    }
    return render(request, 'session/session_detail.html', context)


def filter_session(request, team_pk, package_pk, month):
    package = get_object_or_404(UserPackage, package_id=package_pk, team_id=team_pk)
    team = get_object_or_404(Team, pk=team_pk)
    today = datetime.datetime.now()
    sessions = Session.objects.filter(team=team, status=1, date__month=month)
    context = {
        'team': team,
        'package': package,
        'sessions': sessions,
        'today': today,
    }
    return render(request, 'session/session_overview.html', context)


def new_session(request, team_pk, package_pk):
    if request.method == "POST":
        form = AddSession(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.team = get_object_or_404(Team, pk=team_pk)
            session.created_date = timezone.now()
            session.save()
            messages.success(request, 'Los gehts, dein Training wurde erfolgreich erstellt!')
            return redirect(reverse('session_detail', args=[package_pk, team_pk, session.pk]))
    else:
        form = AddSession()
    return render(request, 'session/new_session.html', {'form': form})


def edit_session(request, session_pk, team_pk, package_pk):
    session = get_object_or_404(Session, pk=session_pk)
    if request.method == "POST":
        form = EditSession(request.POST, instance=session)
        if form.is_valid():
            session = form.save(commit=False)
            session.edited_date = timezone.now()
            session.save()
            messages.success(request, 'Die Trainigsinformationen wurden aktualisiert')
            return redirect(reverse('session_detail', args=[package_pk, team_pk, session_pk]))
    else:
        form = EditSession(instance=session)
    return render(request, 'session/edit_session.html', {'form': form})


def copy_session(request, session_pk, team_pk, package_pk):
    session = get_object_or_404(Session, pk=session_pk)
    team = get_object_or_404(Team, pk=team_pk)
    topic = 'Kopie von ' + session.topic
    session_copy = Session(team_id=team.pk, topic=topic, date=session.date, time=session.time, coordination1=session.coordination1, coordination2=session.coordination2)
    session_copy.save()
    messages.success(request, 'Erledigt, das Training wurde kopiert und kann nun bearbeitet werden!')
    return redirect(reverse('edit_session', args=[package_pk, team_pk, session_copy.pk]))


def delete_session(request, session_pk, team_pk, package_pk):
    session = get_object_or_404(Session, pk=session_pk)
    if request.method == "POST":
        form = DeleteSession(request.POST, instance=session)
        if form.is_valid():
            session = form.save(commit=False)
            session.edited_date = timezone.now()
            session.status = 0
            session.save()
            messages.success(request, 'Das Training wurde erfolgreich gelöscht')
            return redirect(reverse('select_package', args=[package_pk, team_pk]))
    else:
        form = DeleteSession(instance=session)
    return render(request, 'session/delete_session.html', {'form': form})


# Presence Views
def attendance_detail(request, attendance_pk):
    attendance = get_object_or_404(Attendance, attendance_pk)
    context = {
        'attendance': attendance,
    }
    return render(request, 'attendance/attendance_detail.html', context)


def new_attendance(request, team_pk):
    if request.method == "POST":
        form = AddAttendance(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.team = get_object_or_404(Team, pk=team_pk)
            attendance.created_date = timezone.now()
            attendance.save()
            messages.success(request, 'Das war ein Erfolg, die Abwesenheiten sind gespeichert!')
            return redirect(reverse('session_detail', args=[attendance.pk]))
    else:
        form = AddAttendance()
    return render(request, 'attendance/new_attendance.html', {'form': form})


def edit_attendance(request, attendance_pk):
    attendance = get_object_or_404(Attendance, pk=attendance_pk)
    if request.method == "POST":
        form = EditAttendance(request.POST, instance=attendance)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.edited_date = timezone.now()
            attendance.save()
            messages.success(request, 'Die Abwesenheiten wurden aktualisiert')
            return redirect(reverse('session_detail', args=[attendance]))
    else:
        form = EditAttendance(instance=attendance)
    return render(request, 'attendance/edit_attendance.html', {'form': form})


def delete_attendance(request, attendance_pk):
    attendance = get_object_or_404(Attendance, pk=attendance_pk)
    if request.method == "POST":
        form = DeleteAttendance(request.POST, instance=attendance)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.edited_date = timezone.now()
            attendance.status = 0
            attendance.save()
            messages.success(request, 'Die Abwesenheiten wurden gelöscht')
            return redirect(reverse('session_detail', args=[attendance]))
    else:
        form = DeleteAttendance(instance=attendance)
    return render(request, 'attendance/delete_attendance.html', {'form': form})