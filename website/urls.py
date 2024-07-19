from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path('details', views.details, name="details"),
    path('booking', views.booking, name="booking"),
    #path('appointments', views.appointments, name="appointments"),
    path('staffs', views.staffs, name="staffs"),
    path('active_appointments/', views.active_appointments, name='active_appointments'),
    path('manage_appointments/', views.manage_appointments, name='manage_appointments'),
    path('edit_appointment/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('rebook_appointment/<int:appointment_id>/', views.rebook_appointment, name='rebook_appointment'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    
]
