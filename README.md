# TechJourneyJosh Planner

A CLI planner connected to Google Calendar via **MCP (Model Context Protocol)** — an open standard by Anthropic that lets AI models securely connect to external tools like Google Calendar.

---

## Pick Your Setup Path

| Path | What you need |
|------|--------------|
| [GitHub Codespaces](#option-a-github-codespaces) | GitHub account (free tier works) |
| [Replit](#option-b-replit) | Replit account (free tier works) |
| [Local machine](#option-c-local-machine) | Python 3.10+ installed |

---

## Step 1 — Get Google OAuth Credentials (do this first, on any device)

1. Open [console.cloud.google.com](https://console.cloud.google.com/) in your phone browser
2. Tap the **project dropdown** at the top → **New Project** → name it `Planner` → **Create**
3. Tap the hamburger menu (☰) → **APIs & Services** → **Library**
4. Search **Google Calendar API** → tap it → **Enable**
5. Tap **APIs & Services** → **Credentials** → **+ Create Credentials** → **OAuth client ID**
6. If prompted, tap **Configure Consent Screen** → choose **External** → fill in App name (anything) → **Save and Continue** through all steps
7. Back on Create OAuth client ID → Application type: **Desktop app** → Name it anything → **Create**
8. A popup shows your **Client ID** and **Client Secret** — copy both somewhere safe (Notes app is fine)

---

## Option A — GitHub Codespaces

> Works entirely in your phone browser. No installs.

1. Open this repo on GitHub → tap the green **Code** button → **Codespaces** tab → **Create codespace on main**
2. Wait ~60 seconds for the environment to load
3. In the terminal at the bottom, run:

```bash
cp .env.example .env
```

4. Open `.env` in the file explorer and paste in your Client ID and Secret:

```
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run the OAuth setup (this opens a browser tab via Codespaces port forwarding):

```bash
python auth/google_oauth.py
```

7. A **popup or port-forwarding notification** will appear — tap **Open in Browser**, sign in with Google, allow access
8. Copy the `GOOGLE_REFRESH_TOKEN` printed in the terminal and paste it into `.env`
9. Test it:

```bash
python planner.py list
```

---

## Option B — Replit

> Also works in your phone browser.

1. Go to [replit.com](https://replit.com) → **+ Create Repl** → **Import from GitHub** → paste this repo URL
2. In the Replit Shell tab, run:

```bash
cp .env.example .env
```

3. Open `.env` from the file tree and fill in your Client ID and Secret
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the OAuth setup:

```bash
python auth/google_oauth.py
```

6. Replit will show a **webview URL** for the OAuth callback — tap it, sign in, allow access
7. Paste the printed `GOOGLE_REFRESH_TOKEN` into `.env`
8. Test it:

```bash
python planner.py list
```

---

## Option C — Local Machine

1. Clone the repo and `cd` into it
2. `cp .env.example .env` and fill in your Client ID and Secret
3. `pip install -r requirements.txt`
4. `python auth/google_oauth.py` — a browser window opens automatically
5. Sign in, allow access, copy `GOOGLE_REFRESH_TOKEN` into `.env`
6. `python planner.py list`

---

## Using the Planner

```bash
# List upcoming events (default: next 10)
python planner.py list

# List more events
python planner.py list --max 20

# Add an event (times in UTC)
python planner.py add "Team standup" 2026-05-10T09:00:00Z 2026-05-10T09:30:00Z

# Add with a description
python planner.py add "Deploy v2" 2026-05-15T14:00:00Z 2026-05-15T15:00:00Z --desc "Production release"

# Delete an event by ID
python planner.py delete <event_id>
```

---

## How the MCP Connection Works

`.mcp.json` tells Claude Code to launch the Google Calendar MCP server when you open this project. That means Claude can read and write your calendar events directly during your sessions — no manual API calls needed.

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
