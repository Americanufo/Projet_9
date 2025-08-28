from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Vue de la page d'accueil
@login_required
def home(request):
    return render(request, 'home.html')