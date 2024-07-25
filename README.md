# Clinic Appointment Management System
## Overview
  This project is for my final submission to Harvard's CS50 Web Programming with Python and Javascript. 
  
  This a Django-based web application created for a fake clinic called Radiant, designed to manage the clinic's appointments efficiently. It provides features for booking appointments, managing appointment statuses, and sending confirmation emails to patients.
 And being a website, it also contain all of the clinic's services, offers, staff, etc,. Informations and images contained in this project are AI generated just to populate the pages.

### Distinctiveness and Complexity:
>  This is my first formal web application, and I'm so happy that it's working! It's functional, easy to navigate, simple and clean, I think I can sell this. Hopefully, soon I can generate some income building websites like this.

>  The website is live! It is hosted on [Render's](https://dashboard.render.com/) Free tier plan, and as it's database, also the 1-month free Postgres from Render, an amazing site! I spent many hours looking for a working free web hosting servers. And honestly, web hosting 
> is hell, I didn't expect it to be so hard and complicated. I can even say building the website is easier than hosting it! There in lies the complexity of this project I think, and what makes it distinct; 
> that it's production ready ! You can check it through this [link](https://radian-web-test.onrender.com/), however, given the nature of free tier, it has a downtime of 50 seconds with inactivity, meaning it will load for less than a minute on your first visit.
> I wanted to break free from localhost and test the project in real world context, and so this is an accomplishment for me! 

>  With regards to the functionality of the website, any user can book an appointment, regardless of being logged in or not. Being signed in doesn't bring any better features either, it's just that the username of the user will be registered as the booker.
> Additional functionality can only be accessed when the user is a ***staff***, or the ***superuser***, that can be added via Django's admin page. A staff who registered via the website will remain an ordinary user unless registered as a staff in the admin page.
> So the website functions as an all-in website and appointment management for the clinic, reducing the learning curve (or even none at all) for the staff.


## Features
  1. **Home Page:** A welcoming landing page for the clinic's website.
  2. **Appointment Booking:** Users can book appointments using a simple form, no need to sign-in
  3. **Staffs and Admins have the ability to:**
     - **Active Appointments:** View all active appointments with pagination support.
     - **Manage Appointments:** Manage appointments by marking them as done, canceled, or deleting them.
     - **Edit Appointment:** Edit the details of any appointment.
     - **Appointment Details:** View detailed information about a specific appointment.
     - **Email Confirmation:** Clicking a Confirmed button automatically sends an email template containing all the appointment details
     
  4. **Procedure Details page:** More informtion about the procedure is available for the user to read.
  5. **Staff Page:** Information about the clinic's staff.
  6. **Google Review:** User can read google reviews left by users
  7. **User Authentication:** Users can register, log in, and log out.


## Installation
Clone the repository:

```
git clone https://github.com/RjPsalms/capstone.git
```

Create and activate a virtual environment:
```
python -m venv env
```

Activate virtual environment\
```
env\Scripts\activate
```

## Install dependencies:
Run this in your terminal
```
pip install -r requirements.txt
```

Set up the database:

```
python manage.py migrate
```

Create a superuser:

```
python manage.py createsuperuser
```


Collect static files:

```
python manage.py collectstatic
```


Run the development server:
```
python manage.py runserver
```


Configuration

>! [!NOTE]
> This is an important step to ensure the static files will be rendered in production.

In your settings.py file, configure static files:

```
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'website/static'),
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```


## Acknowledgement
I would like to express my deepest gratitude to the incredible staff and teachers at Harvard University for this unbelievably amazing free courses!
Special thanks to Prof. Brian Yu and Prof. David Malan. Both have been amazing teachers, and I am deeply grateful for all the knowledge and skills you have imparted to me. Your influence has been crucial in the development of this project and my growth in the field of computer science.
