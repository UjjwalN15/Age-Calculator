# from django.shortcuts import render, get_object_or_404
# from django.utils import timezone
# from datetime import datetime
# import pytz
# from .models import User

# def home(request):
#     return render(request, 'index.html')

# def calculate_age(request, timezone='Asia/Kathmandu'):
#     if request.method == 'POST':
#         dob = request.POST.get('dob', None)
#         email = request.POST.get('email', None)
#         name = request.POST.get('first_name', None)
        
#         if not dob or not email or not name:
#             return render(request,{'error': 'All fields are required.'})
        
#         try:
#             dob_split = [int(d) for d in dob.split('-')]
#             tz = pytz.timezone(timezone)
#             today = datetime.now(tz)
#             birthdate = datetime(dob_split[0], dob_split[1], dob_split[2])
#             birthdate = tz.localize(birthdate)
#             age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
#         except ValueError:
#             return render(request,{'error': 'Invalid date format.'})
        
#         # Attempt to retrieve the user; if not found, handle gracefully
#         user = User.objects.filter(email=email).first()
#         if user:
#             user.date_of_birth = birthdate.date()  # Save the date of birth
#             user.save()

#             # Call the email function to send the age calculation result
#             send_email_for_agecalculation(email, age, name, dob)

#             # Redirect to the 'successful.html' template after processing
#             return render(request, 'successful.html')
#         else:
#             return render(request,{'error': 'No user found with the provided email.'})
    
#     return render(request, 'index.html')
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
import pytz
from .models import User
from .emails import *
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
    return render(request, 'index.html')
def calculate_age(request, timezone='Asia/Kathmandu'):
    if request.method == 'POST':
        dob = request.POST.get('dob', None)
        email = request.POST.get('email', None)
        fname = request.POST.get('first_name', None)
        lname = request.POST.get('last_name', None)
        gender = request.POST.get('gender', None)
        address = request.POST.get('address', None)
        
        if not dob or not email or not fname or not lname or not gender or not address:
            return render(request, 'error.html', {'error': 'All fields are required.'})
        
        try:
            dob_split = [int(d) for d in dob.split('-')]
            tz = pytz.timezone(timezone)
            today = datetime.now(tz)
            birthdate = datetime(dob_split[0], dob_split[1], dob_split[2])
            birthdate = tz.localize(birthdate)
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            if age <= 0:
                # return render(request, 'error.html', {'error': 'Wrong birthdate input'})
                return HttpResponseRedirect(f"{reverse('error')}")
        except ValueError:
            # return render(request, 'error.html',{'error': 'Invalid date format.'})
            return HttpResponseRedirect(f"{reverse('error')}")
        
        # Check if user already exists; if not, create a new one
        user, created = User.objects.get_or_create(email=email, defaults={
            'first_name': fname,
            'date_of_birth': birthdate.date(),
            'last_name': lname,
            'gender': gender,
            'address': address,
        })
        
        if not created:
            # If user already exists, update the date of birth and name
            user.date_of_birth = birthdate.date()
            user.first_name = fname
            user.last_name= lname
            user.gender= gender
            user.address= address
            user.save()

        # Call the email function to send the age calculation result
        send_email_for_agecalculation(email, age, fname, dob)

        # Redirect to the 'successful.html' template after processing
        return render(request, 'successful.html', {'age': age})
    
    return render(request, 'index.html')

def error_view(request):
    return render(request, 'error.html')