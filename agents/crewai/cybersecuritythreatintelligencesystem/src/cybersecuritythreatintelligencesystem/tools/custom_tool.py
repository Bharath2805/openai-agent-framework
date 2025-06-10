# cybersecuritythreatintelligencesystem/tools/custom_tool.py

import os
import time
from typing import Type, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from crewai.tools import BaseTool
from twilio.rest import Client

load_dotenv()

class WhatsAppMessageInput(BaseModel):
    message: str = Field(..., description="The message content to send to WhatsApp")

class WhatsAppTool(BaseTool):
    name: str = "send_whatsapp_message"
    description: str = "Send a message to WhatsApp. Provide the bulletin content as a string."
    args_schema: Type[BaseModel] = WhatsAppMessageInput

    def _run(self, message: str) -> str:
        # Default WhatsApp number
        to_number = "+4915222350056"
        
        if not message or not message.strip():
            return "❌ Error: Message content cannot be empty."

        account_sid = os.getenv("WHATSAPP_ACCOUNT_SID")
        auth_token = os.getenv("WHATSAPP_AUTH_TOKEN")
        from_number = os.getenv("WHATSAPP_FROM_NUMBER")

        if not all([account_sid, auth_token, from_number]):
            return "❌ Error: WhatsApp credentials not found in environment variables."

        try:
            client = Client(account_sid, auth_token)
            
            # WhatsApp message length limit
            MAX_LENGTH = 4000
            
            if len(message) <= MAX_LENGTH:
                # Send as single message
                twilio_message = client.messages.create(
                    from_=f'whatsapp:{from_number}',
                    body=f"🔔 CrewAI Security Alert:\n\n{message}",
                    to=f'whatsapp:{to_number}'
                )
                return f"✅ WhatsApp message sent successfully! SID: {twilio_message.sid}"
            else:
                # Split into multiple messages
                chunks = [message[i:i + MAX_LENGTH] for i in range(0, len(message), MAX_LENGTH)]
                sids = []
                
                for i, chunk in enumerate(chunks, 1):
                    content = f"🔔 CrewAI Security Alert (Part {i}/{len(chunks)}):\n\n{chunk}"
                    twilio_message = client.messages.create(
                        from_=f'whatsapp:{from_number}',
                        body=content,
                        to=f'whatsapp:{to_number}'
                    )
                    sids.append(twilio_message.sid)
                    
                    # Rate limiting
                    if i < len(chunks):
                        time.sleep(2)
                
                return f"✅ WhatsApp bulletin sent in {len(chunks)} parts! SIDs: {', '.join(sids)}"
                
        except Exception as e:
            return f"❌ Failed to send WhatsApp message: {str(e)}"