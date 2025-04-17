from django.db import models
from users.models import Utilisateur
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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

class Availability(models.Model):
    kine = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    jour = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    duree_rdv = models.IntegerField(
        default=30,
        validators=[MinValueValidator(15), MaxValueValidator(120)],
        help_text="Durée d'un rendez-vous en minutes"
    )
    est_disponible = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Disponibilité"
        verbose_name_plural = "Disponibilités"
        ordering = ['jour', 'heure_debut']
        unique_together = ['kine', 'jour', 'heure_debut']
    
    def __str__(self):
        return f"{self.kine.get_full_name()} - {self.jour} {self.heure_debut}-{self.heure_fin}"
    
    def get_creneaux_disponibles(self):
        """Retourne la liste des créneaux disponibles pour cette plage horaire"""
        creneaux = []
        current_time = self.heure_debut
        while current_time < self.heure_fin:
            creneaux.append(current_time)
            # Ajouter la durée du rendez-vous
            minutes = current_time.hour * 60 + current_time.minute + self.duree_rdv
            current_time = current_time.replace(
                hour=minutes // 60,
                minute=minutes % 60
            )
        return creneaux
