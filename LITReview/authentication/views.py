from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout # import des fonctions login et authenticate
from django.views.generic import View
from django.conf import settings

from . import forms

# Vue de déconnexion
def logout_user(request):
    logout(request)
    return redirect('login')

# Vue d'inscription
def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, 'signup.html', context={'form': form})  # formulaire non valide
    # pour les requêtes GET (ou autres)
    return render(request, 'signup.html', context={'form': form})
