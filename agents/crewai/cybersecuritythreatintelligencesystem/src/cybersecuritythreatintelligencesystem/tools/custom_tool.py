# cybersecuritythreatintelligencesystem/tools/custom_tool.py

import os
import time
import requests
from typing import Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from crewai.tools import BaseTool

load_dotenv()

class DiscordMessageInput(BaseModel):
    content: str = Field(..., description="The text content you want to send to Discord.")

class DiscordWebhookTool(BaseTool):
    name: str = "Send to Discord"
    description: str = "Sends a message to a Discord channel using a webhook URL from the environment."
    args_schema: Type[BaseModel] = DiscordMessageInput

    def _run(self, content: str) -> str:
        if not content or not content.strip():
            return "❌ Error: Content cannot be empty."

        webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        if not webhook_url:
            return "❌ Error: DISCORD_WEBHOOK_URL is not set in the environment."

        if not webhook_url.startswith("https://discord.com/api/webhooks/"):
            return "❌ Error: Invalid Discord webhook URL format."

        MAX_LENGTH = 1900
        chunks = [content[i:i + MAX_LENGTH] for i in range(0, len(content), MAX_LENGTH)]

        success_count = 0

        for i, chunk in enumerate(chunks, start=1):
            payload = {
                "content": f"🔔 CrewAI Alert (Part {i}/{len(chunks)}):\n{chunk}"
            }

            try:
                print(f"\n📡 Sending to Discord:\n{payload['content']}")
                response = requests.post(webhook_url, json=payload, timeout=10)
                print(f"📬 Discord Response: {response.status_code} - {response.text}")

                if response.status_code in [200, 204]:
                    success_count += 1
                else:
                    return f"❌ Failed at part {i}. HTTP {response.status_code}. Response: {response.text}"

                if i < len(chunks):
                    time.sleep(1)

            except Exception as e:
                return f"❌ Exception occurred: {str(e)}"

        return f"✅ Successfully sent {success_count} part(s) to Discord."
