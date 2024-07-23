from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_appointment_confirmation(appointment):
    subject = 'Appointment Confirmation'
    from_email = settings.EMAIL_HOST_USER
    to = appointment.email

    html_content = render_to_string('website/confirmation_email.html', {
        'first_name': appointment.first_name,
        'last_name': appointment.last_name,
        'service': appointment.service,
        'appt_date': appointment.appt_date,
        'details': appointment.details
    })

    msg = EmailMultiAlternatives(subject, '', from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
