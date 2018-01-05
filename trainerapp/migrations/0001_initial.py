# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 23:54
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import trainerapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('present', models.BooleanField()),
                ('absent', models.BooleanField()),
                ('absence_reason', models.CharField(blank=True, choices=[('match', 'Spiel'), ('other', 'Sonstige'), ('sick', 'Krank'), ('work', 'Beruf'), ('education', 'Schule / Ausbildung'), ('injured', 'Verletzt')], max_length=70)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('edited_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Keeper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=70)),
                ('first_name', models.CharField(max_length=70)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('club', models.CharField(max_length=70)),
                ('level', models.CharField(max_length=70)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('street', models.CharField(blank=True, max_length=70)),
                ('zipcity', models.CharField(blank=True, max_length=70)),
                ('nationality', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('shirtnumber', models.IntegerField(blank=True, null=True)),
                ('foot', models.CharField(blank=True, choices=[('1', 'rechts'), ('2', 'links')], max_length=5)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('occupation', models.CharField(blank=True, choices=[('school', 'Sch\xfcler'), ('Student', 'Student'), ('employed', 'Berufst\xe4tig'), ('pro', 'Profi'), ('education', 'Ausbildung'), ('other', 'Andere')], max_length=70)),
                ('notes', models.TextField(blank=True)),
                ('status', models.IntegerField(default=1)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('edited_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('avatar_image', models.ImageField(default='keepers/default-avatar.jpg', upload_to=trainerapp.models.keeper_upload_path)),
            ],
            options={
                'ordering': ('last_name', 'first_name'),
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('description', models.CharField(max_length=70)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('edited_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=70)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('time', models.TimeField(default=django.utils.timezone.now)),
                ('duration', models.DurationField(default=datetime.timedelta(0, 5400))),
                ('coordination1', models.CharField(choices=[('orientation', 'Orientierung'), ('rhytm', 'Rhytmus'), ('balance', 'Gleichgewicht'), ('differentiation', 'Differenzierung'), ('reaction', 'Reaktion')], max_length=70)),
                ('coordination2', models.CharField(choices=[('orientation', 'Orientierung'), ('rhytm', 'Rhytmus'), ('balance', 'Gleichgewicht'), ('differentiation', 'Differenzierung'), ('reaction', 'Reaktion')], max_length=70)),
                ('type', models.CharField(blank=True, choices=[('analysis', 'Videoanalyse'), ('match', 'Spiel/Trainingsspiel'), ('special', 'Spezifisch'), ('theory', 'Theorie'), ('integrated', 'Integriert'), ('other', 'Andere')], max_length=70)),
                ('goal', models.TextField(blank=True, max_length=70)),
                ('technique', models.TextField(blank=True, max_length=500)),
                ('tactic', models.TextField(blank=True, max_length=500)),
                ('stamina', models.TextField(blank=True, max_length=500)),
                ('mental', models.TextField(blank=True, max_length=500)),
                ('equipment', models.CharField(blank=True, max_length=200)),
                ('intensity', models.CharField(blank=True, choices=[('medium', 'Mittel'), ('high', 'Hoch'), ('regenaration', 'Regenerativ')], max_length=25)),
                ('status', models.IntegerField(default=1)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('edited_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ('date', 'time'),
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('club', models.CharField(max_length=70)),
                ('status', models.IntegerField(default=1)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('edited_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='UserPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField()),
                ('usage_counter', models.IntegerField(default=0)),
                ('installed_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('deinstalled_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainerapp.Package')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainerapp.Team')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainerapp.Team'),
        ),
        migrations.AddField(
            model_name='keeper',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainerapp.Team'),
        ),
        migrations.AddField(
            model_name='keeper',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendance',
            name='keeper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainerapp.Keeper'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainerapp.Session'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainerapp.Team'),
        ),
    ]
