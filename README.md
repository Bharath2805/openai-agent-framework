# AI Agents with WhatsApp Integration 🤖📱

This project demonstrates two powerful AI agent frameworks:
1. **OpenAI Agents SDK** - For simple agent workflows
2. **CrewAI** - For multi-agent cybersecurity intelligence system

Both can send results directly to your WhatsApp!

## 🚀 Quick Setup

### 1. Download the Project
1. Go to your GitHub repository
2. Click the green **"Code"** button
3. Select **"Download ZIP"**
4. Extract the ZIP file to your computer

### 2. Install Cursor IDE
1. Visit [cursor.sh](https://cursor.sh)
2. Download and install Cursor IDE
3. Open Cursor and select **"Open Folder"**
4. Choose your extracted project folder

### 3. Set Up Python Environment
Open Cursor's terminal and run these commands:

```bash
# Create virtual environment
python -m venv .venv

# Activate it (Windows)
.venv\Scripts\activate

# Activate it (Mac/Linux)
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

## 🔧 Configuration

### 1. Create Environment File
1. In your project folder, create a file called `.env`
2. Copy this template and fill in your details:

```env
# OpenAI API Key
OPENAI_API_KEY=sk-proj-your-openai-key-here

# WhatsApp via Twilio
WHATSAPP_ACCOUNT_SID=your-twilio-account-sid
WHATSAPP_AUTH_TOKEN=your-twilio-auth-token
WHATSAPP_FROM_NUMBER=+14155238886

# Optional: Other AI providers
GOOGLE_API_KEY=your-google-api-key
DEEPSEEK_API_KEY=your-deepseek-key
GROQ_API_KEY=your-groq-key
```

### 2. Get OpenAI API Key
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Go to **API Keys** section
4. Click **"Create new secret key"**
5. Copy the key to your `.env` file

### 3. Set Up WhatsApp with Twilio

#### Step 1: Create Twilio Account
1. Go to [twilio.com](https://www.twilio.com)
2. Click **"Sign up"** and create a free account
3. Verify your email and phone number

#### Step 2: Get Your Account Details
1. Go to your [Twilio Console](https://console.twilio.com)
2. Find your **Account SID** and **Auth Token**
3. Copy these to your `.env` file

#### Step 3: Set Up WhatsApp Sandbox
1. In Twilio Console, go to **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Follow the instructions to join the WhatsApp Sandbox
3. Send the activation message from your phone to the Twilio number
4. Copy the **From** number (usually starts with +1415) to your `.env` file

#### Step 4: Test Your Setup
- The sandbox number should be: `+14155238886`
- You need to send a message like `join <code>` to activate it
- Your phone number will be whitelisted for testing

## 📚 What's Included

### OpenAI Agents SDK Examples
- **Notebook 1**: Basic agent creation and conversation
- **Notebook 2**: Multi-agent customer support system
- **Notebook 3**: Guardrails and content filtering
- **Notebook 4**: Deep research with web search

### CrewAI Cybersecurity System
- **5 Specialized Agents**: Threat researcher, malware analyst, phishing watcher, news monitor, report compiler
- **Automated Intelligence**: Daily security bulletins sent to WhatsApp
- **Multi-Model Support**: Uses different AI models for different tasks

## 🎯 How to Run

### OpenAI Agents (Jupyter Notebooks)
1. Open Cursor terminal
2. Start Jupyter: `jupyter notebook`
3. Open any `.ipynb` file
4. Run cells one by one
5. Watch agents work and send results to WhatsApp!

### CrewAI Cybersecurity System
1. Open Cursor terminal
2. Navigate to the CrewAI folder
3. Run: `python main.py`
4. Wait for the crew to research and compile a security report
5. Check your WhatsApp for the daily bulletin!

## 🔍 Key Features

### OpenAI Agents SDK
- ✅ Simple agent creation
- ✅ Tool integration (web search, WhatsApp)
- ✅ Agent collaboration and handoffs
- ✅ Input/output guardrails
- ✅ Multi-model support

### CrewAI System
- ✅ Multi-agent cybersecurity intelligence
- ✅ Real-time threat monitoring
- ✅ Automated research and reporting
- ✅ WhatsApp bulletins
- ✅ Configurable agent roles and tasks

## 📱 WhatsApp Integration

Both systems can send messages to WhatsApp:
- **Research reports** from deep web searches
- **Customer support** responses
- **Security bulletins** with latest threats
- **Social media posts** for marketing

Messages are automatically formatted for mobile reading with emojis and proper spacing.

## 🛠️ Customization

### Change WhatsApp Number
Edit the phone number in your code files:
```python
whatsapp_number = "+1234567890"  # Your number here
```

### Add New Agents
1. **OpenAI Agents**: Create new `Agent()` instances with custom instructions
2. **CrewAI**: Add new agents in `agents.yaml` and tasks in `tasks.yaml`

### Modify AI Models
- OpenAI: `gpt-4o-mini`, `gpt-4o`
- Google: `gemini-2.0-flash`
- DeepSeek: `deepseek-chat`
- Groq: `llama3-8b-8192`

## 🚨 Troubleshooting

### Common Issues

**"API Key not found"**
- Check your `.env` file exists
- Verify the key format is correct
- Make sure no extra spaces

**"WhatsApp not working"**
- Verify you joined the Twilio sandbox
- Check your phone number is whitelisted
- Confirm all Twilio credentials are correct

**"Module not found"**
- Activate your virtual environment
- Run `pip install -r requirements.txt`
- Restart your terminal

### Need Help?
1. Check the error messages carefully
2. Verify your `.env` file has all required keys
3. Make sure your virtual environment is activated
4. Try running simpler examples first

## 🎉 What's Next?

Once everything works:
1. Experiment with different prompts
2. Create your own agent personalities
3. Add new tools and integrations
4. Build custom workflows for your needs

Happy coding with AI agents! 🚀