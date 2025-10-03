from django.contrib import admin
from .models import UserFollows
from django.contrib.auth import get_user_model

@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')       
    search_fields = ('user__username', 'followed_user__username')  # Recherche par noms d’utilisateur
    ordering = ('user',)

User = get_user_model()
admin.site.register(User)