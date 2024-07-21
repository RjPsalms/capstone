from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Patient

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class PatientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('first_name', css_class='form-control mb-3', wrapper_class='col-md-5 col-lg-4'),
            Field('last_name', css_class='form-control mb-3', wrapper_class='col-md-5 col-lg-4'),
            Field('email', css_class='form-control mb-3', wrapper_class='col-md-5 col-lg-4'),
            Field('phone_number', css_class='form-control mb-3', wrapper_class='col-md-5 col-lg-4'),
            Field('service', css_class='form-select mb-3', wrapper_class='col-md-5 col-lg-4'),
            Field('appt_date', css_class='form-control mb-3', wrapper_class='col-md-5 col-lg-'),
            Field('details', css_class='form-control mb-3', wrapper_class='col-md-10 col-lg-8', attrs={'rows': '1'}),
        )
        
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'service', 'appt_date', 'details']
        widgets = {
            'appt_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'details': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
        }

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user is not None:
            instance.user = user
        if commit:
            instance.save()
        return instance
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email is required.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise ValidationError("Phone number is required.")
        if not phone_number.isdigit() or len(phone_number) < 10:
            raise ValidationError("Enter a valid 10-digit and above phone number.")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        appt_date = cleaned_data.get('appt_date')
        email = cleaned_data.get('email')

        if not service or not appt_date:
            raise ValidationError("Service and appointment date are required.")
        
         # Check for past date
        if appt_date and appt_date < timezone.now():
            raise ValidationError("The appointment date cannot be in the past.")

        # Check for duplicate booking, excluding the current instance
        if self.instance.pk:
            if Patient.objects.filter(service=service, appt_date=appt_date, email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A booking already exists for this service at the specified time.")
        else:
            if Patient.objects.filter(service=service, appt_date=appt_date, email=email).exists():
                raise ValidationError("A booking already exists for this service at the specified time.")
        
        return cleaned_data
