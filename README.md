# TechJourneyJosh Planner

A CLI planner connected to Google Calendar via the **Model Context Protocol (MCP)**.

## What is MCP?

**MCP (Model Context Protocol)** is an open standard by Anthropic that lets AI models (like Claude) securely connect to external tools and data sources — including Google Calendar, databases, file systems, and more.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Google OAuth credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the **Google Calendar API**
4. Create **OAuth 2.0 Client ID** credentials (type: Desktop app)
5. Download the client secret

### 3. Configure environment variables

```bash
cp .env.example .env
# Fill in GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
```

### 4. Generate your refresh token

```bash
python auth/google_oauth.py
```

This opens a browser for OAuth consent. Paste the printed `GOOGLE_REFRESH_TOKEN` into `.env`.

### 5. Connect MCP to Claude Code

The `.mcp.json` file is already configured. Claude Code will auto-load the Google Calendar MCP server when you open this project. Make sure your `.env` values are set.

## Usage

```bash
# List upcoming events
python planner.py list

# Add an event
python planner.py add "Team standup" 2026-05-10T09:00:00Z 2026-05-10T09:30:00Z

# Add with description
python planner.py add "Deploy v2" 2026-05-15T14:00:00Z 2026-05-15T15:00:00Z --desc "Production release"

# Delete an event
python planner.py delete <event_id>
```

## MCP Configuration

`.mcp.json` wires up the Google Calendar MCP server so Claude Code can read and write calendar events directly during your sessions:

```json
{
  "mcpServers": {
    "google-calendar": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-calendar"],
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}",
        "GOOGLE_REFRESH_TOKEN": "${GOOGLE_REFRESH_TOKEN}"
      }
    }
  }
}
```
