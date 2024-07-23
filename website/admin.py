from django.contrib import admin
from .models import User, Category, Patient

# Register your models here.

class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'appt_date', 'date_added','is_active','is_done', 'user')

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Patient, PatientAdmin)