import os
import requests
from langchain.agents import Tool
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_experimental.tools import PythonREPLTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from playwright.async_api import async_playwright
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables from root .env file
load_dotenv("../.env", override=True)

# WhatsApp/Twilio configuration - NOW USING ENVIRONMENT VARIABLES
WHATSAPP_ACCOUNT_SID = os.getenv("WHATSAPP_ACCOUNT_SID")
WHATSAPP_AUTH_TOKEN = os.getenv("WHATSAPP_AUTH_TOKEN") 
WHATSAPP_FROM_NUMBER = os.getenv("WHATSAPP_FROM_NUMBER")
WHATSAPP_TO_NUMBER = os.getenv("WHATSAPP_TO_NUMBER", "+4915222350056")

# Initialize services with error handling
try:
    from langchain_community.utilities import GoogleSerperAPIWrapper
    serper = GoogleSerperAPIWrapper()
except:
    serper = None
    print("Google Serper not configured, using basic search")

try:
    from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
    wikipedia_available = True
except:
    wikipedia_available = False
    print("Wikipedia not available")

# Only initialize Twilio if credentials are available
if WHATSAPP_ACCOUNT_SID and WHATSAPP_AUTH_TOKEN:
    twilio_client = Client(WHATSAPP_ACCOUNT_SID, WHATSAPP_AUTH_TOKEN)
else:
    twilio_client = None
    print("Twilio credentials not found in environment variables")

async def playwright_tools():
    """Set up Playwright browser tools for web automation"""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright

def send_whatsapp_notification(message: str):
    """Send a WhatsApp notification to the user when research is complete"""
    try:
        if not twilio_client:
            return "⚠️ WhatsApp not configured. Add WHATSAPP credentials to .env file"
            
        formatted_message = f"🔬 Research Assistant Update:\n\n{message}"
        
        # Try to send WhatsApp message
        message = twilio_client.messages.create(
            from_=f"whatsapp:{WHATSAPP_FROM_NUMBER}",
            body=formatted_message,
            to=f"whatsapp:{WHATSAPP_TO_NUMBER}"
        )
        return f"✅ WhatsApp notification sent successfully! Message SID: {message.sid}"
    except Exception as e:
        # If WhatsApp fails, just log it and continue
        error_msg = f"⚠️ WhatsApp notification failed: {str(e)}"
        print(error_msg)
        return f"📝 Research completed! (WhatsApp notification skipped - {error_msg})"

def get_file_tools():
    """Get file management tools for saving research outputs"""
    os.makedirs("research_outputs", exist_ok=True)
    toolkit = FileManagementToolkit(root_dir="research_outputs")
    return toolkit.get_tools()

def advanced_web_search(query: str):
    """Enhanced web search specifically for research purposes"""
    try:
        if serper:
            results = serper.run(query)
            return f"Research search results for '{query}':\n{results}"
        else:
            return f"Search functionality not available. Please configure SERPER_API_KEY in your .env file"
    except Exception as e:
        return f"Search failed: {str(e)}"

async def get_research_tools():
    """Compile all tools needed for research assistance"""
    
    # WhatsApp notification tool
    whatsapp_tool = Tool(
        name="send_whatsapp_notification",
        func=send_whatsapp_notification,
        description="Send a WhatsApp notification to the user when research is completed or important updates are available"
    )
    
    # Enhanced search tool
    search_tool = Tool(
        name="research_web_search", 
        func=advanced_web_search,
        description="Search the web for academic and research information on any topic"
    )
    
    # File management tools
    file_tools = get_file_tools()
    
    # Wikipedia for academic references (if available)
    wiki_tool = None
    if wikipedia_available:
        try:
            from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
            wikipedia = WikipediaAPIWrapper()
            wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia)
        except Exception as e:
            print(f"Wikipedia tool creation failed: {e}")
    
    # Python for data analysis
    try:
        from langchain_experimental.tools import PythonREPLTool
        python_repl = PythonREPLTool()
    except Exception as e:
        print(f"Python REPL tool not available: {e}")
        python_repl = None
    
    # Browser tools for web research
    browser_tools, browser, playwright = await playwright_tools()
    
    # Compile all available tools
    all_tools = file_tools + browser_tools + [whatsapp_tool, search_tool]
    
    if wiki_tool:
        all_tools.append(wiki_tool)
    if python_repl:
        all_tools.append(python_repl)
    
    return all_tools, browser, playwright
