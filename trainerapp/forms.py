# -*- coding: utf-8 -*-

from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit, ButtonHolder
from crispy_forms.bootstrap import InlineRadios


from .models import Team, UserPackage, Keeper, Session, Attendance


class UserChangeForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')


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
    last_name = forms.CharField(label_suffix="", label="Name",
                                error_messages={'required':'Erfasse den Familienname, damit du ihn später findest',
                                                                             'max_length':'Der Name kann nicht länger als 70 Zeichen sein',})
    first_name = forms.CharField(label_suffix="", label="Vorname",
                                 error_messages={'required':'Der Torhüter hat bestimmt auch einen Vornamen',
                                                                               'max_length':'Der Vorname kann nicht länger als 70 Zeichen sein',})
    level = forms.CharField(label_suffix="", label="Mannschaft",
                            help_text='Erfasse die Mannschaft wie 1. Liga oder Junioren B' ,error_messages={'required':'Falls er noch in keiner Mannschaft ist, ist er Teamlos',
                                                                               'max_length':'Die Mannschaftsbezeichnung kann nicht länger als 70 Zeichen sein',})
    class Meta:
        model = Keeper
        fields = ('avatar_image','last_name','first_name','level')
        error_messages = {
            'avatar_image' : {
                   'invalid': 'Das Profilbildformat wird nicht unterstützt, lade ein JPEG oder PNG hoch',
                   'invalid_image': 'Das Profilbildformat wird nicht unterstützt, lade ein JPEG oder PNG hoch',
            }
        }


class EditKeeper(forms.ModelForm):
    last_name = forms.CharField(label_suffix="", label="Name",
                                error_messages={'required':'Erfasse den Familienname, damit du ihn später findest',
                                                                             'max_length':'Der Name kann nicht länger als 70 Zeichen sein',})
    first_name = forms.CharField(label_suffix="", label="Vorname",
                                 error_messages={'required':'Der Torhüter hat bestimmt auch einen Vornamen',
                                                                               'max_length':'Der Vorname kann nicht länger als 70 Zeichen sein',})
    level = forms.CharField(label_suffix="", label="Mannschaft",
                            help_text='Erfasse die Mannschaft wie 1. Liga oder Junioren B' ,error_messages={'required':'Falls er noch in keiner Mannschaft ist, ist er Teamlos',
                                                                               'max_length':'Die Mannschaftsbezeichnung kann nicht länger als 70 Zeichen sein',})
    birthdate = forms.DateField(input_formats=['%d.%m.%Y', ], widget=AdminDateWidget(format='%d.%m.%Y'), label='Geburtsdatum', required=False)
    email = forms.EmailField(label_suffix="", label="E-Mail", required=False,
                                error_messages={'invalid':'Eine E-Mail Adresse beinhaltet ein @ Zeichen',})
    phone = forms.CharField(label_suffix="", label="Telefonnummer", required=False,
                                error_messages={'max_length':'Akzeptierte Telefonnummern sind 078 405 76 99 oder +41 78 405 76 99',})
    street = forms.CharField(label_suffix="", label="Strasse", required=False,
                                error_messages={'max_length':'Ein Strassenname kann nicht länger als 70 Zeichen sein',})
    zipcity = forms.CharField(label_suffix="", label="PLZ / Ort", required=False,
                                error_messages={'max_length':'PLZ / Ort kann nicht länger als 70 Zeichen sein',})
    shirtnumber = forms.IntegerField(label_suffix="", label="Trikotnummer", required=False,
                                error_messages={'invalid':'Shirts werden nur mit Zahlen bedruckt',})
    foot = forms.ChoiceField(choices=Keeper.FOOT_CHOICES, widget=forms.RadioSelect(attrs={'type' : 'radio'}), label_suffix="", label="Starker Fuss", required=False)
    height = forms.IntegerField(label_suffix="", label="Grösse", required=False, min_value=100, max_value=250,
                                help_text='in cm', error_messages={'invalid':'Wow wie gross ist das in cm?', 'min_value':'Negativzahlen sind beim Gewicht nicht möglich',
                                                                   'max_value':'Wir begrenzen auf 250cm'})
    weight = forms.IntegerField(label_suffix="", label="Gewicht", required=False, min_value=0, max_value=200,
                                help_text='in kg', error_messages={'invalid':'Boah, wie misst man das in kg?', 'min_value':'Negativzahlen sind beim Gewicht nicht möglich',
                                                                   'max_value':'Wir begrenzen auf 200kg'})
    occupation = forms.ChoiceField(choices=Keeper.OCCUPATION_CHOICES, label_suffix="", label="Beschäftigung", required=False)
    #avatar_image = forms.ImageField(widget=forms.ClearableFileInput())
    avatar_image = forms.ImageField(label_suffix="", label="")
    class Meta:
        model = Keeper
        fields = ('avatar_image','last_name','first_name','birthdate','club', 'level', 'email','phone','street','zipcity',
                  'nationality','shirtnumber','foot','height','weight','occupation')
        labels = {
            'nationality': ('Nationalität'),
        }
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
    DURATION_CHOICES = {
        (1, '30'),
        (2, '45'),
        (3, '60'),
        (4, '75'),
        (5, '90'),
        (6, '105'),
        (7, '120+'),
    }
    topic = forms.CharField(label="Thema", error_messages={'required':'Bestimme den Inhalt des Trainings',
                                                           'max_length':'Das Thema kann nicht länger als 70 Zeichen sein',})
    date = forms.DateField(widget=forms.TextInput(attrs={'id': 'datepicker'}), input_formats=['%d.%m.%Y',],
                           label='Datum', error_messages={'required':'Wähle ein Datum aus',})
    time = forms.TimeField(widget=forms.widgets.TextInput(attrs={'id': 'timepicker2'}), input_formats=['%h:%m:%s',],
                           label='Zeit', error_messages= {'required':'Erfasse eine Zeit im Format z.B. 17:30,'})
    duration = forms.ChoiceField(choices=DURATION_CHOICES, widget=forms.widgets.RadioSelect, label_suffix="", label="Trainingsdauer in Minuten",)
    coordination = MultiSelectField(choices=Session.COORDINATION_CHOICES)
    type = forms.ChoiceField(choices=Session.TYPE_CHOICES, widget=forms.widgets.RadioSelect, label_suffix="", label="Trainingsart", initial="special")
    class Meta:
        model = Session
        fields = ('topic','date','time','duration','coordination', 'type')
        label = {
            'coordination': 'Koordinative Schwerpunkte'
        }
        error_messages = {
            'coordination': {
                'required': 'Wähle eine Koordinative Fähigkeit aus'
            },
        }

    def __init__(self, *args, **kwargs):
        super(AddSession, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset('',
                     'topic',
                     'date',
                     Field('time', css_class="input-group-addon bootstrap-timepicker timepicker"),
                     Field(InlineRadios('duration')),
                     Field('coordination'),
                     'type',
                     ),
        ButtonHolder(
            Submit('Training erfassen', 'Training erfassen', css_class="teal-green btn-block")
        ),
        )


class EditSession(forms.ModelForm):
    topic = forms.CharField(label="Thema", error_messages={'required': 'Bestimme den Inhalt des Trainings',
                                                           'max_length': 'Das Thema kann nicht länger als 70 Zeichen sein', })
    date = forms.DateField(input_formats=['%d.%m.%Y', ], widget=AdminDateWidget(format='%d.%m.%Y'),
                           label='Datum', error_messages={'required': 'Wähle ein Datum aus', })
    time = forms.TimeField(widget=forms.widgets.TimeInput(format='%h:%m'),
                           label='Zeit', error_messages={'required': 'Erfasse eine Zeit im Format z.B. 17:30,'})
    duration = forms.DurationField(widget=forms.widgets.TimeInput(format='%H:%i'),
                                   label='Trainingsdauer',
                                   error_messages={'required': 'Erfasse eine Zeit im Format z.B. 17:30,'})
    coordination = MultiSelectField(choices=Session.COORDINATION_CHOICES)
    type = forms.ChoiceField(choices=Session.TYPE_CHOICES, label_suffix="", label="Trainingsart")
    class Meta:
        model = Session
        fields = ('topic','date','time','duration','coordination', 'type','goal','equipment','intensity')
        labels = {
            'coordination': ('Koordinative Schwerpunkte'),
            'goal': ('Beschreibung / Ziel'),
            'equipment': ('Benötigtes Material'),
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
    keeper = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Attendance.objects.values('keeper').filter(team_id=28))

    class Meta:
        model = Attendance
        fields = ('keeper',)


class EditAttendance(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('session','keeper','present','absence_reason')


class DeleteAttendance(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ()