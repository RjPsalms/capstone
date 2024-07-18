from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path('details', views.details, name="details"),
    path('booking', views.booking, name="booking"),
    path('appointments', views.appointments, name="appointments"),
    path('staffs', views.staffs, name="staffs"),
]
