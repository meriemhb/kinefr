from django import forms
from .models import RendezVous
from users.models import Kine
from django.utils import timezone

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['kine', 'date', 'heure', 'motif']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}),
            'heure': forms.TimeInput(attrs={'type': 'time'}),
            'motif': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les kinésithérapeutes actifs
        self.fields['kine'].queryset = Kine.objects.filter(utilisateur__is_active=True)
        # Personnaliser l'affichage des kinésithérapeutes
        self.fields['kine'].label_from_instance = lambda obj: f"{obj.utilisateur.get_full_name()} - {obj.specialites}"
        self.fields['date'].label = "Date du rendez-vous"
        self.fields['heure'].label = "Heure du rendez-vous"
        self.fields['motif'].label = "Motif de la consultation" 