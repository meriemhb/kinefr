from django.db import models
from users.models import Utilisateur

class Appointment(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('CONFIRME', 'Confirmé'),
        ('ANNULE', 'Annulé'),
        ('TERMINE', 'Terminé'),
    ]

    patient = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='patient_appointments')
    kine = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='kine_appointments')
    date_heure = models.DateTimeField()
    duree = models.IntegerField(help_text="Durée en minutes")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rendez-vous {self.id} - {self.patient} avec {self.kine} le {self.date_heure}"

    def get_status_color(self):
        colors = {
            'EN_ATTENTE': 'warning',
            'CONFIRME': 'success',
            'ANNULE': 'danger',
            'TERMINE': 'info',
        }
        return colors.get(self.statut, 'secondary')
