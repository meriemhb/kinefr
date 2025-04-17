from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Utilisateur(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrateur')
        PATIENT = 'PATIENT', _('Patient')
        KINE = 'KINE', _('Kinésithérapeute')
        VENDEUR = 'VENDEUR', _('Vendeur')

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.PATIENT,
    )
    date_naissance = models.DateField(null=True, blank=True)
    telephone = models.CharField(max_length=15, blank=True)

class Patient(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='patient_profile')
    numero_securite_sociale = models.CharField(max_length=15, blank=True)

class Kine(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='kine_profile')
    numero_adeli = models.CharField(max_length=9, blank=True)
    specialites = models.CharField(max_length=200, blank=True)

class Vendeur(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='vendeur_profile')
    entreprise = models.CharField(max_length=100, blank=True)

class Admin(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='admin_profile')
    niveau_acces = models.IntegerField(default=1)
