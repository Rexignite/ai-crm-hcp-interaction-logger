from rest_framework import serializers
from .models import Interaction
from hcp.models import HCP

class HCPSerializer(serializers.ModelSerializer):
    class Meta:
        model = HCP
        fields = ['id', 'name', 'specialty', 'email', 'phone', 'organization']

class InteractionSerializer(serializers.ModelSerializer):
    hcp = HCPSerializer(read_only=True)
    hcp_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Interaction
        fields = ['id', 'hcp', 'hcp_id', 'summary', 'structured_data', 'sentiment', 'action_items', 'created_at']