from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from .models import Utilisateur, Patient, Kine, Vendeur
from django.views.generic import View
from appointments.models import Appointment
from django.db import models

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            
            if role == 'PATIENT':
                Patient.objects.create(utilisateur=user)
            elif role == 'KINE':
                Kine.objects.create(utilisateur=user)
            elif role == 'VENDEUR':
                Vendeur.objects.create(utilisateur=user)
            
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès !')
            return redirect('home')
    else:
        form = UserRegistrationForm()
        role = request.GET.get('type', '')
        if role:
            form.fields['role'].initial = role.upper()

    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
    }
    
    if hasattr(user, 'patient_profile'):
        context['profile'] = user.patient_profile
    elif hasattr(user, 'kine_profile'):
        context['profile'] = user.kine_profile
    elif hasattr(user, 'vendeur_profile'):
        context['profile'] = user.vendeur_profile
    
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = Utilisateur.objects.count()
    total_appointments = Appointment.objects.count()
    total_kines = Kine.objects.count()
    total_patients = Patient.objects.count()
    recent_appointments = Appointment.objects.order_by('-date_heure')[:10]

    context = {
        'total_users': total_users,
        'total_appointments': total_appointments,
        'total_kines': total_kines,
        'total_patients': total_patients,
        'recent_appointments': recent_appointments,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_users(request):
    users = Utilisateur.objects.all()
    return render(request, 'admin/users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def admin_appointments(request):
    appointments = Appointment.objects.all().order_by('-date_heure')
    return render(request, 'admin/appointments.html', {'appointments': appointments})

@login_required
@user_passes_test(is_admin)
def admin_reports(request):
    # Statistiques pour les rapports
    appointments_by_status = Appointment.objects.values('statut').annotate(count=models.Count('id'))
    appointments_by_month = Appointment.objects.extra(
        select={'month': "strftime('%m', date_heure)"}
    ).values('month').annotate(count=models.Count('id'))
    
    context = {
        'appointments_by_status': appointments_by_status,
        'appointments_by_month': appointments_by_month,
    }
    return render(request, 'admin/reports.html', context)

@login_required
@user_passes_test(is_admin)
def admin_settings(request):
    if request.method == 'POST':
        # Gérer les paramètres ici
        messages.success(request, 'Paramètres mis à jour avec succès')
        return redirect('admin_settings')
    return render(request, 'admin/settings.html')

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(User, pk=pk, role='PATIENT')
    
    # Vérifier si l'utilisateur a le droit de voir ce profil
    if request.user.role != 'KINE' and request.user != patient:
        messages.error(request, "Vous n'avez pas accès à ce profil.")
        return redirect('home')
    
    # Récupérer les rendez-vous du patient avec le kiné actuel
    appointments = Appointment.objects.filter(
        patient=patient,
        kine=request.user
    ).order_by('-date_heure')
    
    context = {
        'patient': patient,
        'appointments': appointments
    }
    return render(request, 'users/patient_detail.html', context)
