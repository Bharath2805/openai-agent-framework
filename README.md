# Agentic AI Examples

Welcome to **Agentic AI Examples**, a collection of Jupyter notebooks showcasing agentic AI workflows using the OpenAI Agents SDK. This repository includes examples for agent collaboration, tool usage, guardrails, and deep search techniques. Future expansions will integrate additional frameworks like CrewAI to demonstrate multi-agent systems.

## Table of Contents

* [Project Overview](#project-overview)
* [Project Structure](#project-structure)
* [Prerequisites](#prerequisites)
* [Setup Instructions](#setup-instructions)

  * [Option 1: Download as ZIP](#option-1-download-as-zip)
  * [Option 2: Clone with Git](#option-2-clone-with-git)
  * [Environment Setup](#environment-setup)
* [Running the Notebooks](#running-the-notebooks)
* [Using Cursor IDE](#using-cursor-ide)
* [Contributing](#contributing)
* [License](#license)

## Project Overview

This repository contains four Jupyter notebooks demonstrating the capabilities of the OpenAI Agents SDK:

1. **Introduction to OpenAI Agents SDK**: Basics of agent creation and usage.
2. **Agent Collaboration and Tool Usage**: Multi-agent workflows with Discord integration.
3. **Implementing Guardrails for AI Agents**: Adding safety checks for agent inputs.
4. **Deepsearch**: Web search and report generation with Discord notifications.

## Prerequisites

* **Python**: Version 3.10 or higher
* **Git**: For cloning the repository (optional)
* **Cursor IDE**: Recommended for development (optional, alternative IDEs or Jupyter Notebook can be used)
* **API Keys**: OpenAI API key (required), Google, DeepSeek, Groq API keys (optional), and Discord webhook URL
* **Dependencies**: Listed in `requirements.txt`

## Setup Instructions

### Option 1: Download as ZIP

1. **Download the Project**:

   * Visit [https://github.com/Bharath2805/openai-agent-framework](https://github.com/Bharath2805/openai-agent-framework).
   * Click the green **Code** button and select **Download ZIP**.

2. **Extract the ZIP file** to a folder on your computer (e.g., `~/agentic-ai-examples`).

3. **Navigate to the Project Folder**:

   ```bash
   cd ~/agentic-ai-examples
   ```

### Option 2: Clone with Git

1. **Clone the Repository**:

   Open a terminal and run:

   ```bash
   git clone https://github.com/Bharath2805/openai-agent-framework.git
   cd agentic-ai-examples
   ```

## Environment Setup

### Create a Virtual Environment:

```bash
python -m venv .venv
```

### Activate the Virtual Environment:

* **For Mac/Linux**:

  ```bash
  source .venv/bin/activate
  ```

* **For Windows**:

  ```bash
  .venv\Scripts\activate
  ```

### Install Dependencies:

Ensure the virtual environment is activated, then run:

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:

* `jupyter==1.1.1`
* `openai==1.51.2`
* `python-dotenv==1.0.1`
* `requests==2.32.3`
* `pydantic==2.9.2`
* `httpx==0.27.2`
* `ipython==8.28.0`

Note: The `openai-agents` library is assumed to be custom. If it's a public package, ensure it's included in `requirements.txt` or provide installation instructions.

### Set Up Environment Variables:

1. Create a `.env` file in the root directory (`agentic-ai-examples/`).
2. Add the following, replacing with your actual credentials:

   ```env
   OPENAI_API_KEY=your-openai-api-key
   GOOGLE_API_KEY=your-google-api-key
   DEEPSEEK_API_KEY=your-deepseek-api-key
   GROQ_API_KEY=your-groq-api-key
   DISCORD_WEBHOOK_URL=your-discord-webhook-url
   ```

   **Note**: Google, DeepSeek, and Groq API keys are optional for some notebooks. The Discord webhook URL is required for notebooks 2, 3, and 4.

## Running the Notebooks

### Start Jupyter Notebook:

With the virtual environment activated, run:

```bash
jupyter notebook
```

This opens a browser window with the Jupyter interface.

### Open a Notebook:

Navigate to `agents/open_ai_sdk/` and select a notebook (e.g., `1Introduction to OpenAI Agents SDK.ipynb`).

Follow the notebook's instructions to run cells interactively. Ensure API keys and the Discord webhook URL are set in `.env` for full functionality.

## Using Cursor IDE

### Install Cursor IDE:

Download and install **Cursor IDE** from [here](https://cursor.sh/).

### Open the Project:

1. Launch **Cursor IDE**.
2. Click **File > Open Folder** and select the `agentic-ai-examples` directory.

### Configure Python Interpreter:

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) to open the command palette.
2. Type **Python: Select Interpreter** and choose the path to your virtual environment (e.g., `.venv/bin/python` or `.venv\Scripts\python.exe`).

### Run Notebooks:

1. Open a `.ipynb` file (e.g., `agents/open_ai_sdk/2Agent Collaboration and Tool Usage.ipynb`).
2. Use **Cursor's built-in Jupyter support** to run cells interactively.
3. Leverage **Cursor's AI features** for code completion, debugging, or generating explanations.

## Obtaining a Discord Webhook URL

Several notebooks (2, 3, and 4) in this project require a Discord webhook URL to send notifications. Follow these steps to create a webhook URL for your Discord server:

### Log in to Discord:

1. Open Discord (desktop, browser, or mobile) and log in to your account.
2. Ensure you have a server where you have **Manage Webhooks** or **Administrator** permissions. If not, create a server or ask an admin for help.

### Select a Channel:

1. Navigate to the text channel where you want webhook messages to appear (e.g., `#notifications`).
2. Optionally, create a new channel: Click the server name, select **Create Channel**, choose **Text Channel**, and name it.

### Access Channel Settings:

1. Right-click the channel and select **Edit Channel**, or click the gear icon next to the channel name.

### Go to Integrations:

In the channel settings, click the **Integrations** tab on the left sidebar.

### Create a Webhook:

1. Click **Create Webhook** in the Webhooks section.
2. If the button is unavailable, confirm you have **Manage Webhooks** permission or request assistance from a server admin.

### Configure the Webhook:

1. Set a **Name** (e.g., `AgenticAI-Webhook`) to identify its purpose.
2. Confirm the **Channel** is correct.
3. Optionally, upload an avatar image.
4. Click **Save Changes**.

### Copy the Webhook URL:

Locate the **Webhook URL** field (e.g., `https://discord.com/api/webhooks/123456789012345678/abcde...`).
Click **Copy Webhook URL** to copy it to your clipboard.

**Important**: Keep the URL confidential, as anyone with it can send messages to your channel.

### Add to Your `.env` File:

1. Open or create the `.env` file in the `agentic-ai-examples` root directory.

2. Add the webhook URL:

   ```env
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook-id/your-webhook-token
   ```

3. Ensure `.env` is listed in `.gitignore` to avoid exposing the URL on GitHub.

### Test the Webhook (Optional):

To verify the webhook, send a test message using a terminal:

```bash
curl -H "Content-Type: application/json" -X POST -d '{"content":"Test message"}' https://discord.com/api/webhooks/your-webhook-id/your-webhook-token
```

Alternatively, run a notebook (e.g., `4Deepsearch.ipynb`) to test integration. Check the Discord channel for the message.

**Note**: If the webhook fails, verify the URL is correct, the channel exists, and your project loads the `.env` file properly. For help, refer to Discord’s documentation or contact the project maintainer.


