from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from itertools import chain
from operator import attrgetter
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm

# --- Liste des billets (tickets) ---
@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'ticket_list.html', {'tickets': tickets})

# --- Détail d’un billet et ses commentaires ---
@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    reviews = Review.objects.filter(ticket=ticket).order_by('-time_created')
    return render(request, 'ticket_detail.html', {'ticket': ticket, 'reviews': reviews})

# --- Création d’un billet ---
@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm()
    return render(request, 'ticket_form.html', {'form': form})

# --- Modification d’un billet (seulement par son auteur) ---
@login_required
def ticket_update(request, pk):
    print(f"ticket_update : user={request.user}, pk={pk}")
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.user != request.user:
        print("Accès refusé : utilisateur non propriétaire")
        return HttpResponseForbidden("Vous ne pouvez pas modifier ce billet.")
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            print(f"Ticket modifié: {ticket.pk}")
            return redirect('ticket_detail', pk=ticket.pk)
        else:
            print("Formulaire invalide:", form.errors)
    else:
        print("Méthode GET : affichage formulaire")
        form = TicketForm(instance=ticket)
    return render(request, 'ticket_form.html', {'form': form, 'ticket': ticket})

# --- Suppression d’un billet (POST uniquement, auteur unique) ---
@login_required
@require_POST
def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.user != request.user:
        return HttpResponseForbidden("Vous ne pouvez pas supprimer ce billet.")
    ticket.delete()
    return redirect('ticket_list')

# --- Création d’un commentaire sur un billet ---
@login_required
def review_create(request, ticket_pk):
    ticket = get_object_or_404(Ticket, pk=ticket_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = ReviewForm()
    return render(request, 'review_form.html', {'form': form, 'ticket': ticket})

# --- Modification d’un commentaire (seulement par son auteur) ---
@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        return HttpResponseForbidden("Vous ne pouvez pas modifier ce commentaire.")
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('ticket_detail', pk=review.ticket.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'review_form.html', {'form': form, 'review': review})

# --- Suppression d’un commentaire (POST uniquement, auteur unique) ---
@login_required
@require_POST
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        return HttpResponseForbidden("Vous ne pouvez pas supprimer ce commentaire.")
    ticket_pk = review.ticket.pk
    review.delete()
    return redirect('ticket_detail', pk=ticket_pk)

# On récupère les critiques ordonnées de la plus récente à la plus ancienne sur la page des flux
@login_required
def home(request):
    tickets = Ticket.objects.select_related('user').all()
    reviews = Review.objects.select_related('user', 'ticket').all()

    posts = list(chain(tickets, reviews))

    # Ajout d'une propriété temporaire 'post_type' pour chaque élément
    for p in posts:
        p.post_type = 'ticket' if isinstance(p, Ticket) else 'review'

    posts.sort(key=attrgetter('time_created'), reverse=True)

    return render(request, 'home.html', {'posts': posts})

# Création d'un article 
@login_required
def create_review(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            new_ticket = ticket_form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect('home')  # ou autre page de destination
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request, 'review_create.html', {
        'ticket_form': ticket_form,
        'review_form': review_form,
        'ticket' : ticket,
    })

    