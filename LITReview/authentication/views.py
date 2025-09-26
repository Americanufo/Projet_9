from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout  # import des fonctions login et authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import get_user_model

from . import forms
from .models import UserFollows

User = get_user_model()


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


# Gestion des abonnements 
@login_required
def subscriptions(request):
    """
    Affiche la liste des utilisateurs suivis (abonnements) et des abonnés.
    Permet aussi de suivre un nouvel utilisateur via formulaire.
    """
    abonnements = UserFollows.objects.filter(user=request.user)
    abonnes = UserFollows.objects.filter(followed_user=request.user)
    follow_error = None

    if request.method == "POST":
        form = forms.FollowUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user_to_follow = User.objects.get(username=username)
                if user_to_follow == request.user:
                    follow_error = "Vous ne pouvez pas vous abonner à vous-même."
                elif UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists():
                    follow_error = "Vous suivez déjà cet utilisateur."
                else:
                    UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
                    return redirect('authentication:subscriptions')
            except User.DoesNotExist:
                follow_error = "Utilisateur inexistant."
    else:
        form = forms.FollowUserForm()

    return render(request, 'subscriptions.html', {
        'form': form,
        'abonnements': abonnements,
        'abonnes': abonnes,
        'follow_error': follow_error,
    })


# Désabonnement (suppression d'un abonnement)
@login_required
def unfollow(request, followed_id):
    """
    Supprime un abonnement (désabonnement) pour l'utilisateur connecté.
    """
    follow = get_object_or_404(UserFollows, user=request.user, followed_user__id=followed_id)
    follow.delete()
    return redirect('authentication:subscriptions')
