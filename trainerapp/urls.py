from django.conf.urls import url, static
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
    url(r'^(?P<package_pk>\d+)/(?P<team_pk>\d+)/$', views.select_package, name='select_package'),
    # Keeper URLs
    url(r'^keeper/(?P<package_pk>\d+)/(?P<team_pk>\d+)/(?P<keeper_pk>\d+)/$', views.keeper_detail, name='keeper_detail'),
    url(r'^keeper/new/(?P<package_pk>\d+)/(?P<team_pk>\d+)/$', views.new_keeper, name='new_keeper'),
    url(r'^keeper/edit/(?P<package_pk>\d+)/(?P<team_pk>\d+)/(?P<keeper_pk>\d+)/$', views.edit_keeper, name='edit_keeper'),
    url(r'^keeper/delete/(?P<package_pk>\d+)/(?P<team_pk>\d+)/(?P<keeper_pk>\d+)/$', views.delete_keeper, name='delete_keeper'),
    # Session URLs
    url(r'^(?P<package_pk>\d+)/(?P<team_pk>\d+)/monat=(?P<month>\d+)/$', views.filter_session, name='filter_session'),
    url(r'^training/archive/(?P<package_pk>\d+)/(?P<team_pk>\d+)/$', views.session_archive, name='session_archive'),
    url(r'^training/(?P<package_pk>\d+)/(?P<team_pk>\d+)/(?P<session_pk>\d+)/$', views.session_detail, name='session_detail'),
    url(r'^training/new/(?P<package_pk>\d+)/(?P<team_pk>\d+)/$', views.new_session, name='new_session'),
    url(r'^training/edit/(?P<package_pk>\d+)/(?P<team_pk>\d+)/(?P<session_pk>\d+)/$', views.edit_session, name='edit_session'),
    url(r'^training/duplicate/(?P<package_pk>\d+)/(?P<team_pk>\d+)/(?P<session_pk>\d+)/$', views.copy_session, name='copy_session'),
    url(r'^training/delete/(?P<package_pk>\d+)/(?P<team_pk>\d+)/(?P<session_pk>\d+)/$', views.delete_session, name='delete_session'),
    # Presence URLs
    url(r'^anwesenheiten/(?P<package_pk>\d+)/(?P<team_pk>\d+)/(?P<keeper_pk>\d+)/$', views.attendance_detail, name='attendance_detail'),
    url(r'^anwesenheiten/new/(?P<package_pk>\d+)/(?P<team_pk>\d+)/$', views.new_attendance, name='new_attendance'),
    url(r'^anwesenheiten/edit/(?P<package_pk>\d+)/(?P<team_pk>\d+)/(?P<attendance_pk>\d+)/$', views.edit_attendance, name='edit_attendance'),
    url(r'^anwesenheiten/delete/(?P<package_pk>\d+)/(?P<attendance_pk>\d+)/$', views.delete_attendance, name='delete_attendance'),
    # Print and Export URLs
    url(r'^training/pdf/$', views.session_pdf, name='session_pdf')
]