from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout # import des fonctions login et authenticate
from django.views.generic import View


# Vue de déconnexion
def logout_user(request):
    logout(request)
    return redirect('login')
