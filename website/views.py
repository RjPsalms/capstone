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


from django.utils.dateparse import parse_datetime
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


import logging

logger = logging.getLogger(__name__)

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
            
            # send_mail(
            #     "Radiant Aes. appointment success",
            #     "We have successfully received your appointment application. A confirmation SMS will be sent to you in a few minutes. Thank you for your trust!",
            #     settings.DEFAULT_FROM_EMAIL,
            #     [patient.email],
            #     fail_silently=False,
            # )
            
            messages.success(request, 'Appointment booked successfully!')
            return render(request, 'website/index.html', {
                'created_message': 'Appointment place successfully! A SMS confirmation will be sent to you shortly. Thank you for your trust!',
            })
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PatientForm()

    return render(request, 'website/booking.html', {'form': form})

# def booking(request):
#     services = Category.objects.all()
    
#     if request.method == "POST":
#         firstName = request.POST.get('first_name')
#         lastName = request.POST.get('last_name')
#         email_address = request.POST.get('email')
#         phone = request.POST.get('phone_number')
#         service_id = request.POST.get('service')
#         appt_date_str = request.POST.get('appt_date')
#         remarks = request.POST.get('details')
#         user = request.user if request.user.is_authenticated else None

#         logger.debug(f"POST data: {request.POST}")

#         # Validate required fields
#         if not all([firstName, lastName, email_address, phone, service_id, appt_date_str]):
#             return render(request, "website/booking.html", {
#                 "error_message": "Please fill up required fields.",
#                 'services': services,
#             })
        
#         # Validate email address
#         try:
#             validate_email(email_address)
#         except ValidationError:
#             return render(request, "website/booking.html", {
#                 "error_message": "Invalid email address.",
#                 'services': services,
#             })

#         # Validate phone number (simple example, adjust regex as needed)
#         if not phone.isdigit():
#             return render(request, "website/booking.html", {
#                 "error_message": "Invalid phone number.",
#                 'services': services,
#             })

#         selected_service = get_object_or_404(Category, type=service_id)
        
        
#         appt_date = timezone.datetime.strptime(appt_date_str, '%Y-%m-%d %H:%M:%S')
#         appt_date = timezone.make_aware(appt_date, timezone.get_current_timezone())


#         # Check if an identical booking already exists
#         existing_patient = Patient.objects.filter(
#             first_name=firstName,
#             last_name=lastName,
#             service=selected_service,
#             appt_date=appt_date,
#             email=email_address,
#             phone_number=phone,
#         ).exists()

#         if existing_patient:
#             # If the booking already exists, show an error message
#             return render(request, "website/booking.html", {
#                 "error_message": "Booking already exists.",
#                 'services': services,
#             })
#         else:
#             # If the booking doesn't exist, create a new one
#             patient = Patient(
#                 first_name=firstName,
#                 last_name=lastName,
#                 service=selected_service,
#                 email=email_address,
#                 phone_number=phone,
#                 appt_date=appt_date,
#                 details=remarks,
#                 user=user,
#             )
            
#             try:
#                 patient.save()
#                 logger.debug("Patient saved successfully.")
#             except Exception as e:
#                 logger.error(f"Error saving patient: {e}")
#                 return render(request, "website/booking.html", {
#                     "error_message": f"An error occurred while saving the booking: {e}",
#                     'services': services,
#                 })
            
            

#             # Try sending an email
#             # email_address = 'email_address'  
#             # subject = 'Radiant Aes. Appointment Success'
#             # message = 'We have successfully received your appointment application. A confirmation SMS will be sent to you in a few minutes.<br> Thank you for your trust!'
#             # auth_user = '13rj.garcia10@gmail.com'
#             # auth_password = 'Jun_Bots1216'
            
#             # try:
#             #     send_mail(subject, message, "" ,[email_address], auth_user, auth_password )
#             # except Exception as e:
               
#             #     print(f"Error sending email: {e}")
        
#         return render(request, 'website/index.html', {
#             "created_message": "Request for appointment submitted! Please check your email for confirmation.",
#             "new_booking": "New booking has been submitted. Please check the Booked Appointments tab."
#         })  
    
#     else:
#         return render(request, 'website/booking.html', {'services': services})


def appointments(request):
    patient_list = Patient.objects.all().order_by('-date_added')
    paginator = Paginator(patient_list, 10)  # Show 10 patients per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'website/appointments.html', {'page_obj': page_obj})
    

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
