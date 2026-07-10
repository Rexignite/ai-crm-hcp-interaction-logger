from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Interaction
from .serializers import InteractionSerializer
from hcp.models import HCP
from agent.graph import agent, AgentState

# Form mode - Interaction list aur create
class InteractionListCreateView(APIView):
    def get(self, request):
        interactions = Interaction.objects.all().order_by('-created_at')[:20]
        serializer = InteractionSerializer(interactions, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        hcp_id = request.data.get('hcp_id')
        summary = request.data.get('summary')
        
        if not hcp_id or not summary:
            return Response({"error": "hcp_id and summary required"}, status=400)
        
        try:
            hcp = HCP.objects.get(id=hcp_id)
        except HCP.DoesNotExist:
            return Response({"error": "HCP not found"}, status=404)
        
        interaction = Interaction.objects.create(
            hcp=hcp,
            summary=summary,
            structured_data=request.data
        )
        
        serializer = InteractionSerializer(interaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Chat mode - LangGraph agent use karega
class ChatInteractionView(APIView):
    def post(self, request):
        user_message = request.data.get('message', '')
        
        if not user_message:
            return Response({"error": "Message is required"}, status=400)
        
        try:
            # Agent state prepare karein
            state = AgentState(
                messages=[{"role": "user", "content": user_message}],
                intent="",
                tool_output={},
                extracted_data={},
                interaction_id=0
            )
            
            # Agent run karein
            result = agent.invoke(state)
            
            # Response extract karein
            if result.get('tool_output'):
                response_text = result['tool_output'].get('message', str(result['tool_output']))
            else:
                response_text = "I processed your request"
                
            return Response({
                "message": user_message,
                "response": response_text
            })
            
        except Exception as e:
            return Response({
                "message": user_message,
                "response": f"❌ Error: {str(e)}"
            }, status=500)