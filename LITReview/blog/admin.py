from django.contrib import admin
from .models import Ticket, Review

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')
    list_filter = ('time_created', 'user')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-time_created',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'rating', 'ticket', 'user', 'time_created')
    list_filter = ('rating', 'time_created')
    search_fields = ('headline', 'body', 'user__username', 'ticket__title')
    ordering = ('-time_created',)
