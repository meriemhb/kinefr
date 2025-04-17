from django import forms
from .models import Appointment
from users.models import Utilisateur

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['kine', 'date_heure', 'duree', 'notes']
        widgets = {
            'date_heure': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duree': forms.NumberInput(attrs={'min': '15', 'max': '120', 'step': '15'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kine'].queryset = Utilisateur.objects.filter(role='KINE')
        self.fields['kine'].label = 'Kinésithérapeute'
        self.fields['date_heure'].label = 'Date et heure'
        self.fields['duree'].label = 'Durée (minutes)'
        self.fields['notes'].label = 'Notes' 