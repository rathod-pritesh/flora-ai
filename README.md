# Zentriom

Live app: https://zentriom-ai.vercel.app/

I built Zentriom because I kept doing the same thing every week: fix grammar in one app, write a LinkedIn post in another tab, paste confusing code into a third tool just to understand what it was doing. None of these tools know about each other. Switching between them breaks your focus more than people admit. Zentriom puts the tools I actually use, grammar correction, LinkedIn post writing, and code explanation, behind one dashboard, plus a general chat option for anything that doesn't fit those three.

## What actually works right now

The LinkedIn Generator takes a topic, a project, or something you're proud of, and turns it into a post that reads like you'd actually publish it, not something generic. You pick the tone and length, and it works from there.

The Grammar Assistant fixes sentence structure and grammar without rewriting your voice into something else. It shows you what it's changing and why, so you're not just trusting a black box.

The Code Explainer walks through a snippet line by line. I built this one first because it's the tool I personally needed most while learning new codebases.

There's also a Chat option for general questions that don't belong in any of the three tools above, closer to a normal AI conversation than a task-specific workflow.

On the account side, you get email signup with OTP verification, Google login, and password reset, all backed by JWT sessions. History keeps a searchable log of what you've done so far, and Settings shows you which AI model is actually running behind the scenes along with a theme toggle.

A few things are visible on the dashboard but not built yet: a Resume Review tool, a Job Match assistant, a Bug Fix helper, and session-based grouping for chat history instead of one long list. They're marked under development so you can see where this is headed.

## How a request actually gets handled

Each tool sits on its own page, so by the time a request reaches the backend, the system already knows what it is, the user picked LinkedIn Generator or Grammar Assistant by clicking a specific card, not by typing something the AI has to interpret. That choice travels with the request as a task field.

On the backend, a router function checks that field and sends the request straight to the matching node in a LangGraph graph, one node each for grammar, LinkedIn, code explanation, and chat. If the task field doesn't match any of the three specific tools, it falls back to chat by default. Each node builds its own prompt and calls its own service function, then the result comes back through the graph, gets saved to history, and heads back to the frontend.

I want to be clear about what this is and isn't. It's not an AI reading your message and figuring out your intent. It's a router checking one field and picking a node, the same pattern you'd use for any backend routing, just running through LangGraph instead of a plain if/else chain. That's a deliberate choice, not a limitation I'm hiding. Adding a new tool later means writing one more node and one more entry in the router, nothing else has to change.

## Stack

Frontend runs on SvelteKit with Tailwind and Shadcn Svelte for the interface. Backend is Python through FastAPI, with SQLAlchemy for the database layer and UV instead of pip for dependency management, mostly because it's faster and I got tired of waiting. Auth is JWT plus Google OAuth. The database is PostgreSQL, hosted on Neon. The AI layer runs on IBM Granite models through IBM watsonx.ai, with LangGraph handling the routing and LangChain filling in where needed. Everything deploys on Vercel.

## Getting it running locally

Backend needs Python 3.12 and UV installed:

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

You'll need a `.env` file in the backend folder with your database connection string, a JWT secret, Google OAuth credentials, and your IBM watsonx.ai API key.

Frontend is a standard SvelteKit setup:

```bash
cd frontend
npm install
npm run dev
```

Point its `.env` file at wherever your backend is running.

## A note on what was hard to build

Google OAuth alone ate a day and a half of my time, mostly on configuration details that don't show up in tutorials. SMTP was its own mess: I tried Resend first, then hit a wall because Resend wants a verified custom domain and all I had was a `.vercel.app` address, so I moved back to plain SMTP. JWT wasn't much easier, the frontend needs to know whether someone's logged in before it decides what to render, landing page versus the actual app, and getting Bearer token headers to actually authenticate correctly on protected routes took a few rounds of debugging before it held together.

## Where this is going

Resume Review and Job Match are the two features I'd call genuinely "career" tools, and they're next in line. Bug Fix is meant to catch and suggest fixes for errors in code, similar territory to the Code Explainer but more targeted. Session-based chat tracking would group conversations instead of dumping everything into one long list, which is honestly overdue given how the History page works right now.

## Author

Pritesh Rathod
rathodpritesh0712@gmail.com