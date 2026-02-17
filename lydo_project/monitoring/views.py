from django.shortcuts import render
from django.http import JsonResponse
from .models import Youth

def youth_api(request):
    # Fetch data from your Youth model
    youths = Youth.objects.all().values('name', 'age', 'gender', 'program', 'barangay__name')
    # Convert the QuerySet to a list and return as JSON
    return JsonResponse(list(youths), safe=False)

# Create your views here.
