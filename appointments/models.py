from django.db import models
from users.models import Patient, Kine

class RendezVous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rendez_vous')
    kine = models.ForeignKey(Kine, on_delete=models.CASCADE, related_name='rendez_vous')
    date = models.DateField()
    heure = models.TimeField()
    motif = models.TextField(blank=True)
    statut = models.CharField(
        max_length=20,
        choices=[
            ('PLANIFIE', 'Planifié'),
            ('CONFIRME', 'Confirmé'),
            ('ANNULE', 'Annulé'),
            ('TERMINE', 'Terminé'),
        ],
        default='PLANIFIE'
    )
    notes = models.TextField(blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-heure']
        verbose_name = 'Rendez-vous'
        verbose_name_plural = 'Rendez-vous'

    def __str__(self):
        return f"RDV {self.patient.utilisateur.get_full_name()} - {self.kine.utilisateur.get_full_name()} le {self.date} à {self.heure}"
