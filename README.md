# FactCheckit 🇮🇳

Multi-agent AI system for real-time crisis news and claim verification, powered by trusted Indian fact-checkers.

## The Problem

During crises in India—natural disasters, health emergencies, or civil unrest—misinformation spreads rapidly through WhatsApp and social media. False claims about relief operations, medical treatments, or safety measures create panic and endanger lives. While India has excellent fact-checking organizations (PIB, Alt News, BOOM Live, Factly, Vishvas News), manually verifying every viral claim at scale is impossible.

**Key Challenges:**
- Misinformation spreads faster than fact-checkers can respond
- People lack tools to instantly verify suspicious claims
- Manual fact-checking doesn't scale during crisis information overload
- Critical time lost between claim circulation and verification

## The Solution

FactCheckit is an AI-powered multi-agent system that instantly verifies claims by:

1. **Extracting** claims from user input
2. **Cross-referencing** with trusted Indian fact-checkers (PIB, Alt News, BOOM Live, Factly, Vishvas News)
3. **Researching** web sources for evidence
4. **Determining** verdict with confidence scoring
5. **Explaining** results in clear, human-readable format

**Result:** Users get verified information in seconds instead of hours.

## Architecture

### Multi-Agent System

```
User Input → Extractor Agent → Verification Agent → Research Agent → Verdict Agent → Explanation Agent → User Output
```

**Agent Pipeline:**

1. **Extractor Agent**
   - Parses user input
   - Identifies verifiable claims
   - Extracts key entities and assertions

2. **Verification Agent** (Orchestrator)
   - Coordinates workflow
   - Routes to fact-checker sources
   - Manages multi-source checking

3. **Research Agent**
   - Searches web sources
   - Queries Indian fact-checker databases
   - Retrieves supporting evidence

4. **Verdict Agent**
   - Synthesizes evidence
   - Applies confidence scoring
   - Determines classification (True/False/Misleading/Unverified)

5. **Explanation Agent**
   - Generates human-readable summary
   - Provides context and sources
   - Formats shareable report

### Technology Stack

**Frontend:**
- Next.js 14 (React)
- Tailwind CSS
- Responsive design

**Backend:**
- FastAPI (Python)
- Async request handling
- REST API

**AI & Sources:**
- Google Gemini AI
- PIB (Press Information Bureau)
- Alt News
- BOOM Live
- Factly
- Vishvas News

### System Architecture Diagram

```
┌─────────────────┐
│   Web Interface │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Backend│
└────────┬────────┘
         │
    ┌────┴─────┬──────────┬──────────┬──────────┐
    ▼          ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Extract │→│Verify  │→│Research│→│Verdict │→│Explain │
│ Agent  │ │ Agent  │ │ Agent  │ │ Agent  │ │ Agent  │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │ Indian Fact-Checkers  │
              ├───────────────────────┤
              │ • PIB                 │
              │ • Alt News            │
              │ • BOOM Live           │
              │ • Factly              │
              │ • Vishvas News        │
              └───────────────────────┘
```

## Setup Instructions

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Git

## 🚀 QUICK START (5 Minutes)

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run development server**
```bash
npm run dev
```

4. **Access application at** `http://localhost:3000`

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
Create `.env` file:
```env
GOOGLE_API_KEY=your_gemini_api_key
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
```

5. **Run backend server**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **API available at**
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

### Full Stack Development

Run both services simultaneously:

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

## Usage

1. **Open web interface** at `http://localhost:3000`
2. **Enter a claim** you want to verify
3. **Click "Verify Claim"**
4. **Wait for AI agents** to process (loading animation shows progress)
5. **Receive verdict** with:
   - Classification (True/False/Misleading/Unverified)
   - Confidence score
   - Evidence sources
   - Detailed explanation

## Project Structure

```
FactCheckit/
├── frontend/
│   ├── app/
│   │   ├── page.js              # Main landing page
│   │   ├── layout.js            # App layout
│   │   └── globals.css          # Global styles
│   ├── components/
│   │   ├── VerificationForm.js  # Claim input form
│   │   └── Loader.js            # Loading animation
│   ├── package.json
│   └── next.config.mjs
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── agents/              # Agent implementations
│   │   └── bots/                # Telegram bot
│   └── requirements.txt
└── README.md
```

## Features

✅ **Real-time Verification** - Get results in seconds  
✅ **Multi-Source Checking** - Cross-references 5+ Indian fact-checkers  
✅ **AI-Powered Analysis** - Google Gemini AI agents  
✅ **Sequential Agent Pipeline** - Coordinated multi-agent workflow  
✅ **Clean UI** - Responsive, accessible interface  
✅ **Crisis-Optimized** - Designed for emergency information needs  
✅ **Indian Context** - Specialized for Indian fact-checking ecosystem  

## (Optional) Telegram Bot Setup

Want to verify claims via Telegram chat?

#### Create Telegram Bot

1. **Open Telegram** and search for `@BotFather`
2. **Send `/newbot`** command and follow prompts
3. **Copy the API token** you receive
4. **Add to `.env` file:**
```env
TELEGRAM_BOT_TOKEN=your_token_here
```

5. **Run the bot:**
```bash
cd backend
python -m app.bots.telegram_bot
```

6. **Test:** Find your bot on Telegram and send a claim!

## License

MIT License

## Contact

For questions or support, please open an issue on GitHub.

---

**Built for crisis verification • Powered by AI agents • Trusted Indian sources**