Agentic AI Examples
Welcome to Agentic AI Examples, a collection of Jupyter notebooks showcasing agentic AI workflows using the OpenAI Agents SDK. This repository includes examples for agent collaboration, tool usage, guardrails, and deep search techniques. Future expansions will integrate additional frameworks like CrewAI to demonstrate multi-agent systems.
Table of Contents

Project Overview
Project Structure
Prerequisites
Setup Instructions
Option 1: Download as ZIP
Option 2: Clone with Git
Environment Setup


Running the Notebooks
Using Cursor IDE
Contributing
License

Project Overview
This repository contains four Jupyter notebooks demonstrating the capabilities of the OpenAI Agents SDK:

Introduction to OpenAI Agents SDK: Basics of agent creation and usage.
Agent Collaboration and Tool Usage: Multi-agent workflows with Discord integration.
Implementing Guardrails for AI Agents: Adding safety checks for agent inputs.
Deepsearch: Web search and report generation with Discord notifications.




Prerequisites

Python: Version 3.10 or higher
Git: For cloning the repository (optional)
Cursor IDE: Recommended for development (optional, alternative IDEs or Jupyter Notebook can be used)
API Keys: OpenAI API key (required), Google, DeepSeek, Groq API keys (optional), and Discord webhook URL
Dependencies: Listed in requirements.txt

Setup Instructions
Option 1: Download as ZIP

Download the Project:

Visit https://github.com/your-username/agentic-ai-examples.
Click the green Code button and select Download ZIP.
Extract the ZIP file to a folder on your computer (e.g., ~/agentic-ai-examples).


Navigate to the Project Folder:
cd ~/agentic-ai-examples



Option 2: Clone with Git

Clone the Repository:
Open a terminal and run:git clone https://github.com/your-username/agentic-ai-examples.git
cd agentic-ai-examples





Environment Setup

Create a Virtual Environment:
python -m venv .venv


Activate the Virtual Environment:

Mac/Linux:source .venv/bin/activate


Windows:.venv\Scripts\activate




Install Dependencies:

Ensure the virtual environment is activated, then run:pip install -r requirements.txt


The requirements.txt includes:jupyter==1.1.1
openai==1.51.2
python-dotenv==1.0.1
requests==2.32.3
pydantic==2.9.2
httpx==0.27.2
ipython==8.28.0

Note: The openai-agents library is assumed to be custom. If it's a public package, ensure it's included in requirements.txt or provide installation instructions.


Set Up Environment Variables:

Create a .env file in the root directory (agentic-ai-examples/).
Add the following, replacing with your actual credentials:OPENAI_API_KEY=your-openai-api-key
GOOGLE_API_KEY=your-google-api-key
DEEPSEEK_API_KEY=your-deepseek-api-key
GROQ_API_KEY=your-groq-api-key
DISCORD_WEBHOOK_URL=your-discord-webhook-url


Note: Google, DeepSeek, and Groq API keys are optional for some notebooks. The Discord webhook URL is required for notebooks 2, 3, and 4.



Running the Notebooks

Start Jupyter Notebook:

With the virtual environment activated, run:jupyter notebook


This opens a browser window with the Jupyter interface.


Open a Notebook:

Navigate to agents/open_ai_sdk/ and select a notebook (e.g., 1Introduction to OpenAI Agents SDK.ipynb).
Follow the notebook's instructions to run cells interactively.
Ensure API keys and the Discord webhook URL are set in .env for full functionality.



Using Cursor IDE

Install Cursor IDE:

Download and install Cursor from https://cursor.sh/.


Open the Project:

Launch Cursor IDE.
Click File > Open Folder and select the agentic-ai-examples directory.


Configure Python Interpreter:

Press Ctrl+Shift+P (or Cmd+Shift+P on Mac) to open the command palette.
Type Python: Select Interpreter and choose the path to your virtual environment (e.g., .venv/bin/python or .venv\Scripts\python.exe).


Run Notebooks:

Open a .ipynb file (e.g., agents/open_ai_sdk/2Agent Collaboration and Tool Usage.ipynb).
Use Cursor's built-in Jupyter support to run cells interactively.
Leverage Cursor's AI features for code completion, debugging, or generating explanations.




