from django.db import models
from hcp.models import HCP

class Interaction(models.Model):
    INTERACTION_TYPES = [
        ('meeting', 'Meeting'),
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('other', 'Other'),
    ]
    
    hcp = models.ForeignKey(HCP, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES, default='meeting')
    summary = models.TextField()
    structured_data = models.JSONField(default=dict)
    sentiment = models.CharField(max_length=50, blank=True)
    action_items = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.hcp.name} - {self.created_at}"