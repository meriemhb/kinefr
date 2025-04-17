from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Appointment
from .forms import AppointmentForm

@login_required
def appointment_list(request):
    if request.user.role == 'PATIENT':
        appointments = Appointment.objects.filter(patient=request.user)
    elif request.user.role == 'KINE':
        appointments = Appointment.objects.filter(kine=request.user)
    else:
        appointments = []
    
    context = {
        'appointments': appointments
    }
    return render(request, 'appointments/list.html', context)

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            if request.user.role == 'PATIENT':
                appointment.patient = request.user
            elif request.user.role == 'KINE':
                appointment.kine = request.user
            appointment.save()
            messages.success(request, 'Rendez-vous créé avec succès.')
            return redirect('appointments:list')
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/form.html', {'form': form})

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.user not in [appointment.patient, appointment.kine]:
        messages.error(request, "Vous n'avez pas accès à ce rendez-vous.")
        return redirect('appointments:list')
    
    return render(request, 'appointments/detail.html', {'appointment': appointment})

@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.user not in [appointment.patient, appointment.kine]:
        messages.error(request, "Vous n'avez pas accès à ce rendez-vous.")
        return redirect('appointments:list')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rendez-vous mis à jour avec succès.')
            return redirect('appointments:detail', pk=pk)
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'appointments/form.html', {'form': form, 'appointment': appointment})

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.user not in [appointment.patient, appointment.kine]:
        messages.error(request, "Vous n'avez pas accès à ce rendez-vous.")
        return redirect('appointments:list')
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Rendez-vous supprimé avec succès.')
        return redirect('appointments:list')
    
    return render(request, 'appointments/delete.html', {'appointment': appointment})

@login_required
def kine_appointment_list(request):
    if request.user.role != 'KINE':
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('home')
    
    statut = request.GET.get('statut')
    appointments = Appointment.objects.filter(kine=request.user)
    
    if statut:
        appointments = appointments.filter(statut=statut)
    
    context = {
        'appointments': appointments,
        'current_status': statut
    }
    return render(request, 'appointments/kine_list.html', context)
