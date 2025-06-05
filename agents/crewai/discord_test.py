#!/usr/bin/env python3
"""
Test script to verify Discord webhook functionality
Run this separately to test your Discord integration
"""

import os
import requests
from dotenv import load_dotenv

def test_discord_webhook():
    """Test the Discord webhook configuration"""
    
    print("🧪 Testing Discord Webhook...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if webhook URL exists
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not webhook_url:
        print("❌ DISCORD_WEBHOOK_URL not found in environment")
        print("💡 Make sure you have a .env file with:")
        print("   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN")
        return False
    
    print(f"✅ Webhook URL found: {webhook_url[:50]}...")
    
    # Validate URL format
    if not webhook_url.startswith("https://discord.com/api/webhooks/"):
        print("❌ Invalid webhook URL format")
        return False
    
    print("✅ Webhook URL format is valid")
    
    # Test message
    test_message = {
        "content": "🧪 **Test Message from CrewAI System**\n\nIf you see this message, your Discord webhook is working correctly! ✅"
    }
    
    print("📤 Sending test message...")
    
    try:
        response = requests.post(webhook_url, json=test_message, timeout=10)
        
        if response.status_code in [200, 204]:
            print("✅ Test message sent successfully!")
            print("🔍 Check your Discord channel for the test message")
            return True
        else:
            print(f"❌ Failed to send test message. HTTP {response.status_code}")
            print(f"📝 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_discord_tool():
    """Test the actual Discord tool"""
    
    print("\n🔧 Testing Discord Tool Class...")
    
    try:
        from cybersecuritythreatintelligencesystem.tools.custom_tool import DiscordWebhookTool
        
        tool = DiscordWebhookTool()
        result = tool._run("🔧 **Tool Test**\n\nThis is a test from the DiscordWebhookTool class!")
        
        print(f"📊 Tool result: {result}")
        
        if "Successfully sent" in result:
            print("✅ Discord tool is working correctly!")
            return True
        else:
            print("❌ Discord tool test failed")
            return False
            
    except ImportError as e:
        print(f"❌ Could not import Discord tool: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing Discord tool: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Discord Integration Test Suite\n")
    
    # Test 1: Basic webhook
    webhook_success = test_discord_webhook()
    
    # Test 2: Discord tool class
    tool_success = test_discord_tool()
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS:")
    print(f"   Webhook Test: {'✅ PASS' if webhook_success else '❌ FAIL'}")
    print(f"   Tool Test:    {'✅ PASS' if tool_success else '❌ FAIL'}")
    
    if webhook_success and tool_success:
        print("\n🎉 All tests passed! Your Discord integration should work.")
    else:
        print("\n🔍 Some tests failed. Check the errors above.")
        print("\n💡 Common fixes:")
        print("   1. Verify your .env file has the correct DISCORD_WEBHOOK_URL")
        print("   2. Make sure the webhook URL is from a Discord channel you can access")
        print("   3. Check that the webhook hasn't been deleted from Discord")
        print("   4. Ensure your internet connection is working")