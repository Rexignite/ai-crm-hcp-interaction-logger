import json
from datetime import datetime, timedelta
from interactions.models import Interaction
from hcp.models import HCP

def log_interaction_tool(user_message, llm):
    try:
        prompt = f"""
        Extract structured information from this interaction note:
        "{user_message}"
        
        Return ONLY JSON with these exact fields:
        - hcp_name: (full name of the doctor/HCP, e.g., "Dr. Sharma")
        - summary: (brief summary in 1-2 lines)
        - sentiment: (positive/neutral/negative)
        - action_items: (list of next steps)
        
        Example:
        Input: "Met Dr. Sharma today, discussed new diabetes medication"
        Output: {{"hcp_name": "Dr. Sharma", "summary": "Discussed new diabetes medication", "sentiment": "positive", "action_items": ["Schedule follow-up"]}}
        
        Only return JSON, no other text.
        """
        
        extracted = llm.invoke(prompt)
        print(f"🔍 LLM Response: {extracted.content}")  # Debug
        
        try:
            data = json.loads(extracted.content)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON Parse Error: {e}")
            # Fallback - manually extract name
            import re
            name_match = re.search(r'(Dr\.?\s+[A-Z][a-z]+)', user_message)
            hcp_name = name_match.group(1) if name_match else "Unknown"
            data = {
                "hcp_name": hcp_name,
                "summary": user_message[:100],
                "sentiment": "neutral",
                "action_items": []
            }
        
        # Ensure hcp_name is not empty
        if not data.get('hcp_name') or data.get('hcp_name').strip() == '':
            data['hcp_name'] = 'Unknown'
        
        # ✅ FIX: Duplicate HCP handle karein
        hcp_name = data.get('hcp_name', 'Unknown')
        try:
            # Pehle exact match dhundho
            hcp = HCP.objects.get(name=hcp_name)
        except HCP.DoesNotExist:
            # Agar nahi mila toh naya create karo
            hcp = HCP.objects.create(
                name=hcp_name,
                specialty='General'
            )
        except HCP.MultipleObjectsReturned:
            # Agar multiple hain toh pehle wala lo
            hcp = HCP.objects.filter(name=hcp_name).first()
            print(f"⚠️ Multiple HCP found, using first: ID {hcp.id}")
        
        # Interaction save
        interaction = Interaction.objects.create(
            hcp=hcp,
            summary=data.get('summary', user_message),
            structured_data=data,
            sentiment=data.get('sentiment', 'neutral'),
            action_items=data.get('action_items', [])
        )
        
        return {
            "status": "success", 
            "interaction_id": interaction.id, 
            "message": f"✅ Logged for {hcp.name}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Baki functions same rahenge
def edit_interaction_tool(interaction_id, updates, llm):
    try:
        interaction = Interaction.objects.get(id=interaction_id)
        if 'summary' in updates:
            interaction.summary = updates['summary']
        interaction.save()
        return {"status": "success", "message": f"✅ Updated interaction {interaction_id}"}
    except Interaction.DoesNotExist:
        return {"status": "error", "message": "Interaction not found"}

def search_hcp_tool(query):
    results = HCP.objects.filter(name__icontains=query)
    hcp_list = [{"id": h.id, "name": h.name, "specialty": h.specialty} for h in results[:10]]
    return {"status": "success", "count": len(hcp_list), "results": hcp_list}

def schedule_followup_tool(interaction_id, days=7):
    try:
        interaction = Interaction.objects.get(id=interaction_id)
        followup_date = interaction.created_at + timedelta(days=days)
        return {"status": "success", "message": f"📅 Follow-up on {followup_date.strftime('%Y-%m-%d')}"}
    except Interaction.DoesNotExist:
        return {"status": "error", "message": "Interaction not found"}

def generate_summary_tool(interaction_id, llm):
    try:
        interaction = Interaction.objects.get(id=interaction_id)
        prompt = f"Generate professional summary for: {interaction.summary}"
        summary = llm.invoke(prompt)
        return {"status": "success", "summary": summary.content}
    except Interaction.DoesNotExist:
        return {"status": "error", "message": "Interaction not found"}