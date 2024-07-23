from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Patient, User, Category
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .forms import PatientForm


# from django.utils.dateparse import parse_datetime
# from django.core.mail import send_mail
# from django.utils.html import strip_tags
# from django.template.loader import render_to_string


def index(request):
    return render(request, "website/index.html")

def details(request):
    return render(request, 'website/details.html')

def booking(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user if request.user.is_authenticated else None
            patient.save()

            if request.user.is_superuser or request.user.is_staff:
                messages.success(request, 'Appointment booked successfully!')
                form = PatientForm()
                return render(request, 'website/booking.html', {'form': form})
            else:
                messages.success(request, 'Appointment booked successfully! Thank you for your trust!')
                return render(request, 'website/index.html')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PatientForm()
        return render(request, 'website/booking.html', {'form': form})


def active_appointments(request):
    patients = Patient.objects.all().order_by('-date_added')
    paginator = Paginator(patients ,10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'website/active_appointments.html', {
        'page_obj': page_obj
        })

def manage_appointments(request):
    if request.method == 'POST':
        selected_appointments = request.POST.getlist('selected_appointments')
        if not selected_appointments:
            messages.success(request, 'Choose atleast one entry.')
        else:
            action = request.POST.get('action')
            if action == 'delete':
                Patient.objects.filter(id__in=selected_appointments).delete()
                messages.success(request, 'Selected appointments DELETED.')
            elif action == 'cancel':
                Patient.objects.filter(id__in=selected_appointments).update(is_active=False)
                messages.success(request, 'Selected appointments CANCELLED.') 
            elif action == 'done':
                Patient.objects.filter(id__in=selected_appointments).update(is_done=True)
                messages.success(request, 'Selected appointments marked DONE.')          
    return redirect('active_appointments')


def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Patient, id=appointment_id)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully.')
            return redirect('active_appointments')
    else:
        form = PatientForm(instance=appointment)
    
    return render(request, 'website/edit_appointment.html', {'form': form, 'appointment_id': appointment_id})


def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Patient, id=appointment_id)
    if not appointment:
        messages.success(request, 'Choose atleast one entry.')
    else: 
        appointment.is_active = False
        appointment.save()
        messages.success(request, 'Appointment has been CANCELLED.')
    return redirect('active_appointments')


def done_appt(request, appointment_id):
    appointment = get_object_or_404(Patient, id=appointment_id)
    if not appointment:
        messages.success(request, 'Choose atleast one entry.')
    else: 
        appointment.is_done = True
        appointment.save()
    return redirect('active_appointments')

def undone_appt(request, appointment_id):
    appointment = get_object_or_404(Patient, id=appointment_id)
    if not appointment:
        messages.success(request, 'Choose atleast one entry.')
    else: 
        appointment.is_done = False
        appointment.save()
    return redirect('active_appointments')

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Patient, id=appointment_id)
    if not appointment:
        messages.success(request, 'Choose atleast one entry.')
    else:    
        appointment.delete()
        messages.success(request, 'Appointment has been DELETED.')
    return redirect('active_appointments')


def appt_details(request, appointment_id):
    appointment = get_object_or_404(Patient, id=appointment_id)

    return render(request, 'website/appt_details.html', {'appointment': appointment})
     

def confirm_appt(request, appointment_id):
    appointment = get_object_or_404(Patient, id=appointment_id) 
    appointment.is_confirmed = True
    appointment.save()

    #Now write the send email logic here
    # send_mail(
    #     "Radiant Aes. appointment success",
    #     "We have successfully received your appointment application. A confirmation SMS will be sent to you in a few minutes. Thank you for your trust!",
    #     settings.DEFAULT_FROM_EMAIL,
    #     [patient.email],
    #     fail_silently=False,
    # )

    messages.success(request, 'Appointment has been CONFIRMED, a confirmation email has been sent to the client.')
    return redirect('active_appointments')



def staffs(request):
    return render(request, 'website/staffs.html')


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "registration/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "registration/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "registration/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "registration/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "registration/register.html")
