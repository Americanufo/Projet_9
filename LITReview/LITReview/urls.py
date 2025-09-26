"""
URL configuration for LITReview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
import authentication.views
import blog.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Interface d'administration Django
    path("admin/", admin.site.urls),

    # Page de connexion (login) avec vue officielle Django, template personnalisé
    path(
        '',
        LoginView.as_view(
            template_name='login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),

    # Déconnexion de l’utilisateur
    path('logout/', authentication.views.logout_user, name='logout'),

    # Page d’accueil de l’application affichée après connexion (fil d’actualité / blog)
    path('home/', blog.views.home, name='home'),

    # Page d’inscription
    path('signup/', authentication.views.signup_page, name='signup'),

    #  URL principales pour les billets (tickets) 
    path('tickets/', blog.views.ticket_list, name='ticket_list'),
    path('tickets/new/', blog.views.ticket_create, name='ticket_create'),
    path('tickets/<int:pk>/', blog.views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:pk>/edit/', blog.views.ticket_update, name='ticket_update'),
    path('tickets/<int:pk>/delete/', blog.views.ticket_delete, name='ticket_delete'),
    

    #  URLs pour la gestion des commentaires (reviews) 
    path('tickets/<int:ticket_pk>/reviews/new/', blog.views.review_create, name='review_create'),
    path('reviews/<int:pk>/edit/', blog.views.review_update, name='review_update'),
    path('reviews/<int:pk>/delete/', blog.views.review_delete, name='review_delete'),
    path('create-review/', blog.views.create_review, name='review_create'),

    # URL d'abonnement
    path('abonnements/', include('authentication.urls', namespace='authentication')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)