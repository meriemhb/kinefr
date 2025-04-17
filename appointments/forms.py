from django import forms
from .models import RendezVous
from users.models import Kine

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['kine', 'date', 'heure', 'motif', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'heure': forms.TimeInput(attrs={'type': 'time'}),
            'motif': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les kinésithérapeutes disponibles
        self.fields['kine'].queryset = Kine.objects.all()
        self.fields['kine'].label = "Kinésithérapeute"
        self.fields['date'].label = "Date du rendez-vous"
        self.fields['heure'].label = "Heure du rendez-vous"
        self.fields['motif'].label = "Motif de la consultation"
        self.fields['notes'].label = "Notes supplémentaires" 