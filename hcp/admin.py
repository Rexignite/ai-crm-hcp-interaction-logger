from django.contrib import admin
from .models import HCP

@admin.register(HCP)
class HCPAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'specialty', 'email', 'phone', 'organization', 'created_at']
    search_fields = ['name', 'specialty', 'email']
    list_filter = ['specialty', 'created_at']
