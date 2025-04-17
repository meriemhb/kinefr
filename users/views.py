from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from .models import Utilisateur, Patient, Kine, Vendeur

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
