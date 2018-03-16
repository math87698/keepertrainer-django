# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Team, Package, UserPackage, Keeper, Session, Attendance


class TeamAdmin(admin.ModelAdmin):
    list_display = ('trainer','name','club','status','created_date','edited_date')


class PackageAdmin(admin.ModelAdmin):
    list_display = ('name','description','created_date','edited_date')


class UserPackageAdmin(admin.ModelAdmin):
    list_display = ('trainer','team','package','active','usage_counter','installed_date','deinstalled_date')


class KeeperAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','birthdate','club','level','trainer',
                    'team','email','phone','street','zipcity','nationality','shirtnumber','foot',
                    'height','weight','occupation','avatar_image','notes','status','created_date','edited_date')


class SessionAdmin(admin.ModelAdmin):
    list_display = ('topic','date','time','duration','goal','coordination',
                    'team','type','technique','tactic','stamina','mental','equipment','intensity',
                    'status','created_date','edited_date')


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('session','keeper','present','absence_reason','created_date','edited_date')


admin.site.register(Team, TeamAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(UserPackage, UserPackageAdmin)
admin.site.register(Keeper, KeeperAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Attendance, AttendanceAdmin)