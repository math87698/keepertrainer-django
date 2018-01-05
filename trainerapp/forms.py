# -*- coding: utf-8 -*-

from django import forms
from .models import Team, UserPackage, Keeper, Session, Attendance
from django.contrib.admin.widgets import AdminDateWidget


class AddTeam(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name','club')


class DeleteTeam(forms.ModelForm):
    class Meta:
        model = Team
        fields = ()


class AddPackage(forms.ModelForm):
    class Meta:
        model = UserPackage
        fields = ('trainer','team','package','active')


class AddKeeper(forms.ModelForm):
    last_name = forms.CharField(label_suffix="", label="Name", error_messages={'required':'Gib dem Torhüter einen Namen, damit du ihn wieder findest',
                                                                             'max_length':'Der Name kann nicht länger als 70 Zeichen sein',})
    first_name = forms.CharField(label_suffix="", label="Vorname", error_messages={'required':'Gib dem Torhüter einen Vornamen, damit du ihn wieder findest',
                                                                               'max_length':'Der Vorname kann nicht länger als 70 Zeichen sein',})
    club = forms.CharField(label_suffix="", label="Verein", error_messages={'required':'Falls der Torhüter keinen Verein hat, identifiziere ihn als Vereinslos',
                                                                               'max_length':'Der Vereinsname kann nicht länger als 70 Zeichen sein und beinhaltet einen Wert wie FC Olten',})
    level = forms.CharField(label_suffix="", label="Mannschaft", help_text='Erfasse die Mannschaft wie 1. Liga oder Junioren B' ,error_messages={'required':'Falls der Torhüter in keinem Team spielt, identifiziere ihn als Teamlos',
                                                                               'max_length':'Die Mannschaftsbezeichnung kann nicht länger als 70 Zeichen sein, und beinhaltet einen Wert wie z.B. Junioren B',})
    class Meta:
        model = Keeper
        fields = ('avatar_image','last_name','first_name','club', 'level')
        error_messages = {
            'avatar_image' : {
                   'invalid': 'Das Profilbildformat wird nicht unterstützt, lade ein JPEG oder PNG hoch',
                   'invalid_image': 'Das Profilbildformat wird nicht unterstützt, lade ein JPEG oder PNG hoch',
            }
        }


class EditKeeper(forms.ModelForm):
    last_name = forms.CharField(label_suffix="")
    first_name = forms.CharField(label_suffix="")
    club = forms.CharField(label_suffix="")
    level = forms.CharField(label_suffix="")
    birthdate = forms.DateField(input_formats=['%d.%m.%Y', ], widget=AdminDateWidget(format='%d.%m.%Y'), label='Geburtsdatum')
    #foot = forms.ChoiceField(choices=Keeper.FOOT_CHOICES, widget=forms.RadioSelect(attrs={'type' : 'radio'}), label_suffix="", label="Starker Fuss")
    #avatar_image = forms.ImageField(widget=forms.ClearableFileInput())
    avatar_image = forms.ImageField(label_suffix="", label="Profilbild hochladen")
    class Meta:
        model = Keeper
        fields = ('last_name','first_name','birthdate','club', 'level', 'email','phone','street','zipcity',
                  'nationality','shirtnumber','foot','height','weight','occupation','avatar_image')
        error_messages ={
            # 'name': '',
            # 'firstname': '',
            'birthdate': {
                'invalid': 'Bitte gib ein gültiges Datum ein',
            },
            # 'club': 'Bitte gib einen Vereinsnamen ein (z.B. FC Sursee)',
            'level': {
                'required': 'Wähle eine Stufe aus der Liste aus',
            },
        }
        field_classes = {
            'birthdate': forms.DateField,
        }


class DeleteKeeper(forms.ModelForm):
    class Meta:
        model = Keeper
        fields = ()


# Session Forms
class AddSession(forms.ModelForm):
    date = forms.DateField(input_formats=['%d.%m.%Y',], widget=AdminDateWidget(format='%d.%m.%Y'),
                           label='Datum', error_messages={'required':'Wähle ein Datum aus',})
    time = forms.TimeField(widget=forms.widgets.TimeInput(format='%h:%m:%s'),
                           label='Zeit', error_messages= {'required':'Erfasse eine Zeit im Format z.B. 17:30,'})
    duration = forms.DurationField(widget=forms.widgets.TimeInput(format='%H:%i'),
                                   label='Trainingsdauer',
                                   error_messages={'required': 'Erfasse eine Zeit im Format z.B. 17:30,'})
    class Meta:
        model = Session
        fields = ('topic','date','time','duration','coordination1','coordination2','type','goal','equipment','intensity')
        labels = {
            'topic': ('Thema'),
            'duration': ('Trainingsdauer'),
            'coordination1': ('Koordinationsthema 1'),
            'coordination2': ('Koordinationsthema 2'),
        }
        error_messages = {
            'topic': {
                'required': 'Weise dem Training ein Thema deiner Wahl zu',
            },
            'duration': {
                'required': 'Erfasse deine Training im Format z.B. 01:30:00 für 90 min.',
            },
            'coordination1': {
                'required': 'Wähle eine Koordinative Fähigkeit aus'
            },
            'coordination2': {
                'required': 'Wähle eine Koordinative Fähigkeit aus'
            },
        }


class EditSession(forms.ModelForm):
    date = forms.DateField(input_formats=['%d.%m.%Y',], widget=AdminDateWidget(format='%d.%m.%Y'),
                           label='Datum', error_messages={'required':'Wähle ein Datum aus',})
    time = forms.TimeField(widget=forms.widgets.TimeInput(format='%h:%m:%s'),
                           label='Zeit', error_messages= {'required':'Erfasse eine Zeit im Format z.B. 17:30,'})
    duration = forms.DurationField(widget=forms.widgets.TimeInput(format='%H:%i'),
                                   label='Trainingsdauer',
                                   error_messages={'required': 'Erfasse eine Zeit im Format z.B. 17:30,'})
    class Meta:
        model = Session
        fields = ('topic','date','time','duration','coordination1','coordination2','type','goal','equipment','intensity')
        labels = {
            'topic': ('Thema'),
            'duration': ('Trainingsdauer'),
            'coordination1': ('Koordinationsthema 1'),
            'coordination2': ('Koordinationsthema 2'),
        }
        error_messages = {
            'topic': {
                'required': 'Weise dem Training ein Thema deiner Wahl zu',
            },
            'duration': {
                'required': 'Erfasse deine Training im Format z.B. 01:30:00 für 90 min.',
            },
            'coordination1': {
                'required': 'Wähle eine Koordinative Fähigkeit aus'
            },
            'coordination2': {
                'required': 'Wähle eine Koordinative Fähigkeit aus'
            },
        }


class DeleteSession(forms.ModelForm):
    class Meta:
        model = Session
        fields = ()


# Presence Form
class AddAttendance(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('session','keeper','present','absent','absence_reason')


class EditAttendance(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('session','keeper','present','absent','absence_reason')


class DeleteAttendance(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ()