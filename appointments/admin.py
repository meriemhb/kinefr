from django.contrib import admin
from .models import RendezVous

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('get_patient', 'get_kine', 'date', 'heure', 'statut')
    list_filter = ('statut', 'date')
    search_fields = (
        'patient__utilisateur__first_name', 
        'patient__utilisateur__last_name',
        'kine__utilisateur__first_name', 
        'kine__utilisateur__last_name'
    )
    date_hierarchy = 'date'

    def get_patient(self, obj):
        return obj.patient.utilisateur.get_full_name()
    get_patient.short_description = 'Patient'

    def get_kine(self, obj):
        return obj.kine.utilisateur.get_full_name()
    get_kine.short_description = 'Kinésithérapeute'
