# Register your models here.
from django.contrib import admin
from .models import Interaction

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ['id', 'hcp', 'summary', 'sentiment', 'created_at']
    search_fields = ['hcp__name', 'summary']
    list_filter = ['sentiment', 'interaction_type']