# 🛡️ Cybersecurity Threat Intelligence System

A multi-agent threat intelligence pipeline built with **CrewAI**. It collects real-time cybersecurity data, processes it through multiple specialized agents, and sends a final daily bulletin to a **Discord channel** via webhook.

## ✅ Features

- **Agent-based system** with 5 roles:
  - `Threat Researcher`: Finds active threats using **Serper.dev** search
  - `Malware Analyst`: Extracts details about malware, exploits, CVEs
  - `Phishing Watcher`: Tracks phishing campaigns and scam tactics
  - `News Monitor`: Summarizes latest cybersecurity news (via Serper)
  - `Security Report Compiler`: Merges all insights into a final bulletin and sends it to Discord

- Uses **Serper.dev API** for search-based intelligence gathering  
- Final report is:
  - Saved as a Markdown file
  - Automatically posted to Discord using a webhook

## 🛠️ Tools Used

- `CrewAI`: Agent framework
- `SerperDevTool`: Google-like real-time search
- `DiscordWebhookTool`: Sends alerts and reports to a Discord channel

## 🔐 .env Configuration

Create a `.env` file with:


