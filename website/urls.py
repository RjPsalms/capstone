from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path('details', views.details, name="details"),
    path('booking', views.booking, name="booking"),
    path('staffs', views.staffs, name="staffs"),
    path('active_appointments/', views.active_appointments, name='active_appointments'),
    path('done_appt/<int:appointment_id>/', views.done_appt, name='done_appt'),
    path('confirm_appt/<int:appointment_id>/', views.confirm_appt, name='confirm_appt'),
    path('undone_appt/<int:appointment_id>/', views.undone_appt, name='undone_appt'),
    path('appt_details/<int:appointment_id>/', views.appt_details, name='appt_details'),
    path('manage_appointments/', views.manage_appointments, name='manage_appointments'),
    path('edit_appointment/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'), 
]
