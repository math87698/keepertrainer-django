# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class Team(models.Model):
    trainer = models.ForeignKey(User)
    name = models.CharField(max_length=70)
    club = models.CharField(max_length=70)
    status = models.IntegerField(default=1)
    created_date = models.DateTimeField(default=timezone.now)
    edited_date = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "%s" % (self.name)


class Package(models.Model):
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=70)
    created_date = models.DateTimeField(default=timezone.now)
    edited_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "%s" % (self.name)


class UserPackage(models.Model):
    trainer = models.ForeignKey(User)
    team = models.ForeignKey(Team)
    package = models.ForeignKey(Package)
    active = models.BooleanField()
    usage_counter = models.IntegerField(default=0)
    installed_date = models.DateTimeField(default=timezone.now)
    deinstalled_date = models.DateTimeField(default=timezone.now)


# Keeper Model
def keeper_upload_path(instance, filename):
    return '/'.join(['keepers', str(instance.id), filename])

class Keeper(models.Model):
    OCCUPATION_CHOICES = {
        ('school', 'Schüler'),
        ('education', 'Ausbildung'),
        ('Student', 'Student'),
        ('employed', 'Berufstätig'),
        ('pro', 'Profi'),
        ('other', 'Andere'),
    }
    FOOT_CHOICES = {
        ('1', 'rechts'),
        ('2', 'links'),
    }
    trainer = models.ForeignKey(User)
    last_name = models.CharField(max_length=70)
    first_name = models.CharField(max_length=70)
    birthdate = models.DateField(blank=True, null=True)
    club = models.CharField(max_length=70)
    level = models.CharField(max_length=70)
    team = models.ForeignKey(Team)
    email = models.EmailField(max_length=254, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    street = models.CharField(max_length=70, blank=True)
    zipcity = models.CharField(max_length=70, blank=True)
    nationality = CountryField(blank=True)
    shirtnumber = models.IntegerField(blank=True, null=True)
    foot = models.CharField(max_length=5, choices=FOOT_CHOICES, blank=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    occupation = models.CharField(max_length=70, choices=OCCUPATION_CHOICES, blank=True)
    notes = models.TextField(blank=True)
    status = models.IntegerField(default=1)
    created_date = models.DateTimeField(default=timezone.now)
    edited_date = models.DateTimeField(default=timezone.now)
    avatar_image = models.ImageField(upload_to=keeper_upload_path, default='keepers/default-avatar.jpg')
    class Meta:
        ordering = ('last_name','first_name',)

    def __unicode__(self):
        return "%s" % (self.last_name)

    def __unicode__(self):
        return "%s" % (self.first_name)

    @property
    def lifespan(self):
        return '%s - present' % self.birthdate.strftime('%d.m%.%Y')


# Training Session Model
class Session(models.Model):
    COORDINATION_CHOICES = {
        ('orientation', 'Orientierung'),
        ('rhytm', 'Rhytmus'),
        ('balance', 'Gleichgewicht'),
        ('reaction', 'Reaktion'),
        ('differentiation', 'Differenzierung'),
    }
    TYPE_CHOICES = {
        ('special', 'Spezifisch'),
        ('integrated', 'Integriert'),
        ('theory', 'Theorie'),
        ('analysis', 'Videoanalyse'),
        ('match', 'Spiel/Trainingsspiel'),
        ('other', 'Andere')

    }
    INTENSITY_CHOICES = {
        ('high', 'Hoch'),
        ('medium', 'Mittel'),
        ('regenaration', 'Regenerativ'),
    }
    team = models.ForeignKey(Team)
    topic = models.CharField(max_length=70)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    duration = models.DurationField(default=timedelta(minutes=90))
    coordination1 = models.CharField(max_length=70, choices=COORDINATION_CHOICES)
    coordination2 = models.CharField(max_length=70, choices=COORDINATION_CHOICES)
    type = models.CharField(max_length=70, choices=TYPE_CHOICES, blank=True)
    goal = models.TextField(max_length=70, blank=True)
    technique = models.TextField(max_length=500, blank=True)
    tactic = models.TextField(max_length=500, blank=True)
    stamina = models.TextField(max_length=500, blank=True)
    mental = models.TextField(max_length=500, blank=True)
    equipment = models.CharField(max_length=200, blank=True)
    intensity = models.CharField(max_length=25, choices=INTENSITY_CHOICES, blank=True)
    status = models.IntegerField(default=1)
    created_date = models.DateTimeField(default=timezone.now)
    edited_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('date', 'time',)

    def __unicode__(self):
        return "%s" % (self.topic)

    @property
    def lifespan(self):
        return '%s - present' % self.datetime.strftime('%d.m%.%Y %H:%M')


class Attendance(models.Model):
    REASON_CHOICES = {
        ('injured', 'Verletzt'),
        ('sick', 'Krank'),
        ('match', 'Spiel'),
        ('work', 'Beruf'),
        ('education', 'Schule / Ausbildung'),
        ('other', 'Sonstige'),
    }
    session = models.ForeignKey(Session)
    keeper = models.ForeignKey(Keeper)
    team = models.ForeignKey(Team)
    present = models.BooleanField()
    absent = models.BooleanField()
    absence_reason = models.CharField(max_length=70, choices=REASON_CHOICES, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    edited_date = models.DateTimeField(default=timezone.now)