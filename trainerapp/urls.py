from django.conf.urls import url, static
from django.conf import settings
from django.contrib import admin
from . import views


urlpatterns = [
    # url for successful heroku domain (otherwise we get 404)
    url(r'^$', views.heroku, name='heroku'),
    # Account URLs
    url(r'^accounts/settings/$', views.account_settings, name='account_settings'),
    url(r'^accounts/account/edit/$', views.edit_account, name='edit_account'),
    # Team and Dashboard URLs
    url(r'^dashboard/$', views.index, name='index'),
    url(r'^team/new/$', views.new_team, name='new_team'),
    url(r'^team/(?P<team_pk>\d+)/edit/$', views.edit_team, name='edit_team'),
    url(r'^team/(?P<team_pk>\d+)/delete/$', views.delete_team, name='delete_team'),
    # Dashboard Packages link to Keeper, Session
    url(r'^(?P<team_pk>\d+)/(?P<package_pk>\d+)/$', views.select_package, name='select_package'),
    # Keeper URLs
    url(r'^keeper/(?P<keeper_pk>\d+)/(?P<team_pk>\d+)/(?P<package_pk>\d+)/$', views.keeper_detail, name='keeper_detail'),
    url(r'^keeper/new/(?P<team_pk>\d+)/$', views.new_keeper, name='new_keeper'),
    url(r'^keeper/edit/(?P<keeper_pk>\d+)/$', views.edit_keeper, name='edit_keeper'),
    url(r'^keeper/delete/(?P<keeper_pk>\d+)/$', views.delete_keeper, name='delete_keeper'),
    # Session URLs
    url(r'^training/(?P<session_pk>\d+)/(?P<team_pk>\d+)/(?P<package_pk>\d+)/$', views.session_detail, name='session_detail'),
    url(r'^training/new/(?P<team_pk>\d+)/$', views.new_session, name='new_session'),
    url(r'^training/edit/(?P<session_pk>\d+)/$', views.edit_session, name='edit_session'),
    url(r'^training/delete/(?P<session_pk>\d+)/$', views.delete_session, name='delete_session'),
    # Presence URLs
    url(r'^anwesenheiten/(?P<attendance_pk>\d+)/$', views.attendance_detail, name='attendance_detail'),
    url(r'^anwesenheiten/new/(?P<team_pk>\d+)/$', views.new_attendance, name='new_attendance'),
    url(r'^anwesenheiten/edit/(?P<attendance_pk>\d+)/$', views.edit_attendance, name='edit_attendance'),
    url(r'^anwesenheiten/delete/(?P<attendance_pk>\d+)/$', views.delete_attendance, name='delete_attendance'),
]