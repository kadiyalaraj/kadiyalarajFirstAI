# LeanIX Agent Setup Guide

This folder contains a simple LeanIX MCP server scaffold and a Copilot prompt file so you can start using a LeanIX-enabled agent in VS Code.

## Files
- `leanix_mcp_server.py` - local MCP server script
- `README.md` - this guide

## Prerequisites
- Python 3.10+ installed
- A valid LeanIX instance URL
- A LeanIX API token or authentication method

## 1. Update your LeanIX credentials
Open the MCP config file at:
`C:\Users\31805\.copilot\mcp-config.json`

Make sure the `leanix-local` entry has your real values:
- `LEANIX_BASE_URL`
- `LEANIX_API_TOKEN`

## 2. Run the local MCP server
From the workspace folder, run:
```powershell
python "C:/Users/31805/OneDrive - ams OSRAM/Raj_work/Personel/AI workouts/LeanIX Agent/leanix_mcp_server.py"
```

## 3. Use the agent in Copilot Chat
Open Copilot Chat and use the prompt file:
`C:\Users\31805\AppData\Roaming\Code\User\prompts\leanix-agent.prompt.md`

Example prompts:
- "Search LeanIX for an application"
- "Find a factsheet for a service"
- "Retrieve metadata for a LeanIX record"

## 4. Replace the placeholder logic
The current server is a scaffold. It returns sample responses until you connect it to your real LeanIX API endpoints.

To make it fully live, update the functions in `leanix_mcp_server.py` to call your real LeanIX REST API.

## Troubleshooting
- If the server does not start, verify Python is installed.
- If the agent cannot use the tool, verify the MCP config path and the server command.
- If LeanIX requests fail, check your token, URL, and permissions.
