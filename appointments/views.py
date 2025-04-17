from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import RendezVous
from .forms import RendezVousForm

@login_required
def appointment_list(request):
    if request.user.role == 'PATIENT':
        appointments = RendezVous.objects.filter(patient=request.user.patient_profile)
    elif request.user.role == 'KINE':
        appointments = RendezVous.objects.filter(kine=request.user.kine_profile)
    else:
        appointments = RendezVous.objects.none()
    
    return render(request, 'appointments/list.html', {
        'appointments': appointments
    })

@login_required
def kine_appointment_list(request):
    if request.user.role != 'KINE':
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('home')
    
    appointments = RendezVous.objects.filter(kine=request.user.kine_profile)
    
    # Filtrage par statut
    statut = request.GET.get('statut')
    if statut:
        appointments = appointments.filter(statut=statut)
    
    return render(request, 'appointments/kine_list.html', {
        'appointments': appointments,
        'current_statut': statut
    })

@login_required
def appointment_create(request):
    if request.user.role != 'PATIENT':
        messages.error(request, "Seuls les patients peuvent créer des rendez-vous.")
        return redirect('home')
    
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient_profile
            appointment.save()
            messages.success(request, "Le rendez-vous a été créé avec succès.")
            return redirect('appointments:detail', pk=appointment.pk)
    else:
        form = RendezVousForm()
    
    return render(request, 'appointments/create.html', {
        'form': form
    })

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(RendezVous, pk=pk)
    
    # Vérifier que l'utilisateur a le droit de voir ce rendez-vous
    if request.user.role == 'PATIENT' and appointment.patient != request.user.patient_profile:
        messages.error(request, "Vous n'avez pas accès à ce rendez-vous.")
        return redirect('home')
    elif request.user.role == 'KINE' and appointment.kine != request.user.kine_profile:
        messages.error(request, "Vous n'avez pas accès à ce rendez-vous.")
        return redirect('home')
    
    return render(request, 'appointments/detail.html', {
        'appointment': appointment
    })

@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(RendezVous, pk=pk)
    
    # Vérifier que l'utilisateur a le droit de modifier ce rendez-vous
    if request.user.role == 'PATIENT' and appointment.patient != request.user.patient_profile:
        messages.error(request, "Vous n'avez pas le droit de modifier ce rendez-vous.")
        return redirect('home')
    elif request.user.role == 'KINE' and appointment.kine != request.user.kine_profile:
        messages.error(request, "Vous n'avez pas le droit de modifier ce rendez-vous.")
        return redirect('home')
    
    if request.method == 'POST':
        form = RendezVousForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Le rendez-vous a été mis à jour avec succès.")
            return redirect('appointments:detail', pk=appointment.pk)
    else:
        form = RendezVousForm(instance=appointment)
    
    return render(request, 'appointments/update.html', {
        'form': form,
        'appointment': appointment
    })

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(RendezVous, pk=pk)
    
    # Vérifier que l'utilisateur a le droit de supprimer ce rendez-vous
    if request.user.role == 'PATIENT' and appointment.patient != request.user.patient_profile:
        messages.error(request, "Vous n'avez pas le droit de supprimer ce rendez-vous.")
        return redirect('home')
    elif request.user.role == 'KINE' and appointment.kine != request.user.kine_profile:
        messages.error(request, "Vous n'avez pas le droit de supprimer ce rendez-vous.")
        return redirect('home')
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, "Le rendez-vous a été supprimé avec succès.")
        return redirect('appointments:list')
    
    return render(request, 'appointments/delete.html', {
        'appointment': appointment
    })
