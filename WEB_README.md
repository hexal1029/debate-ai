# AI Historical Debate Generator - Web Interface

Web interface for the AI Historical Debate Generator, built with Next.js and FastAPI.

## Architecture

- **Backend**: FastAPI with Server-Sent Events (SSE) for real-time streaming
- **Frontend**: Next.js 14 with App Router, TypeScript, and Tailwind CSS
- **Storage**: In-memory (v1 - debates lost on restart)
- **No Authentication**: Open access for v1

---

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- Anthropic API Key ([get one here](https://console.anthropic.com/))

### 1. Backend Setup

```bash
# Navigate to backend directory
cd /Users/ddhuang/Desktop/CUR/debate-ai/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run the server
cd /Users/ddhuang/Desktop/CUR/debate-ai
PYTHONPATH=. uvicorn backend.main:app --reload --port 8000
```

The backend will be available at **http://localhost:8000**

- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd /Users/ddhuang/Desktop/CUR/debate-ai/frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local if needed (default backend URL is http://localhost:8000)

# Run the development server
npm run dev
```

The frontend will be available at **http://localhost:3000**

---

## Development Workflow

### Run Both Servers

**Terminal 1 - Backend:**
```bash
cd /Users/ddhuang/Desktop/CUR/debate-ai
source backend/venv/bin/activate
PYTHONPATH=. uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd /Users/ddhuang/Desktop/CUR/debate-ai/frontend
npm run dev
```

**Terminal 3 - Original CLI (still works!):**
```bash
cd /Users/ddhuang/Desktop/CUR/debate-ai
python debate.py --p1 "孔子" --p2 "老子" --topic "道" --rounds 3
```

---

## Features

### Backend API

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/debates` | POST | Create new debate |
| `/api/debates` | GET | List all debates (with pagination) |
| `/api/debates/{id}` | GET | Get debate details |
| `/api/debates/{id}/stream` | GET | SSE stream for real-time updates |
| `/api/debates/{id}` | DELETE | Delete debate |
| `/api/styles` | GET | Get available debate styles |
| `/health` | GET | Health check |

### Frontend Pages

- **Home (`/`)**: Debate list gallery
- **Create (`/create`)**: Create new debate form
- **Debate (`/debate/[id]`)**: Real-time debate viewer with SSE streaming

### Real-time Features

- **SSE Streaming**: Server-Sent Events provide real-time progress updates
- **Auto-scroll**: Messages appear with smooth animations
- **Progress Indicator**: Shows current step (e.g., "3/7 - Researching Newton...")
- **Export to Markdown**: Download completed debates

---

## Testing the Web Interface

### 1. Create a Debate

1. Navigate to http://localhost:3000
2. Click "创建辩论" or visit http://localhost:3000/create
3. Fill in:
   - **辩论者 1**: 牛顿
   - **辩论者 2**: 莱布尼茨
   - **辩论话题**: 微积分的发明权
   - **辩论风格**: Academic (or any style)
4. Click "开始辩论"

### 2. Watch Real-time Generation

You'll be redirected to `/debate/[id]` where you can see:
- Progress bar updating in real-time
- Messages appearing as they're generated
- Colored bubbles for each speaker (moderator, character1, character2)

### 3. Export Debate

Once completed, click "导出为 Markdown" to download the debate as a `.md` file.

### 4. View Debate List

Return to the home page to see all debates with status indicators.

---

## API Testing with curl

### Create a debate:
```bash
curl -X POST http://localhost:8000/api/debates \
  -H "Content-Type: application/json" \
  -d '{
    "p1": "孔子",
    "p2": "老子",
    "topic": "道",
    "rounds": 2,
    "style": "casual-chat",
    "language": "zh",
    "language_style": "现代口语"
  }'
```

Response:
```json
{
  "id": "deb_1709876543",
  "status": "pending",
  "created_at": "2026-03-05T10:30:00Z"
}
```

### Connect to SSE stream:
```bash
curl http://localhost:8000/api/debates/deb_1709876543/stream
```

You'll see real-time events:
```
event: connected
data: {"id":"deb_1709876543","status":"pending"}

event: progress
data: {"step":"2/7","message":"正在研究孔子的背景和思想..."}

event: message
data: {"speaker":"主持人","role":"moderator","content":"..."}

event: complete
data: {"id":"deb_1709876543"}
```

---

## Environment Variables

### Backend (`.env`)

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# Optional
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:3000
MAX_CONCURRENT_DEBATES=3
LOG_LEVEL=info
DEBUG=false
```

### Frontend (`.env.local`)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=AI Historical Debate Arena
```

---

## Project Structure

```
debate-ai/
├── backend/                      # FastAPI backend
│   ├── main.py                   # App entry point
│   ├── models.py                 # Pydantic models
│   ├── routes/                   # API endpoints
│   │   ├── debates.py
│   │   ├── stream.py            # SSE streaming
│   │   └── styles.py
│   ├── services/                 # Business logic
│   │   ├── debate_service.py    # Integrates with src/
│   │   └── job_manager.py       # In-memory job queue
│   └── requirements.txt
│
├── frontend/                     # Next.js frontend
│   ├── app/                      # Pages (App Router)
│   │   ├── layout.tsx
│   │   ├── page.tsx             # Home (debate list)
│   │   ├── create/
│   │   │   └── page.tsx         # Create debate
│   │   └── debate/[id]/
│   │       └── page.tsx         # Debate viewer
│   ├── components/               # React components
│   │   ├── DebateForm.tsx
│   │   ├── DebateViewer.tsx
│   │   ├── DebateList.tsx
│   │   ├── MessageBubble.tsx
│   │   └── ProgressIndicator.tsx
│   ├── lib/                      # Utilities
│   │   ├── api.ts               # API client
│   │   ├── types.ts             # TypeScript types
│   │   └── utils.ts             # Helper functions
│   ├── hooks/
│   │   └── useDebateStream.ts   # SSE hook
│   └── package.json
│
├── src/                          # UNCHANGED - Original Python modules
│   ├── ai_client.py
│   ├── character_builder.py
│   ├── debate_engine.py
│   ├── prompter.py
│   ├── formatter.py
│   └── style_config.py
│
└── debate.py                     # UNCHANGED - Original CLI
```

---

## How It Works

### Backend Flow

1. **API Request**: User creates debate via POST `/api/debates`
2. **Job Creation**: `job_manager` creates a `DebateJob` with progress queue
3. **Background Task**: `debate_service.run_debate_job()` runs asynchronously:
   - Imports existing modules from `src/`
   - Calls `CharacterBuilder.build_character()` for each character
   - Calls `DebateEngine.run_debate()` with progress callback
   - Streams progress to `progress_queue`
4. **SSE Stream**: Client connects to GET `/api/debates/{id}/stream`
   - Receives real-time events from `progress_queue`
   - Events: `progress`, `message`, `complete`, `error`

### Frontend Flow

1. **Create Form**: User fills `DebateForm` component
2. **API Call**: Calls `createDebate()` from `lib/api.ts`
3. **Redirect**: Navigates to `/debate/[id]`
4. **SSE Connection**: `useDebateStream` hook connects to SSE endpoint
5. **Real-time Updates**: Messages appear as they're generated
6. **Completion**: Export button appears when debate finishes

---

## Deployment

### Backend (Railway / Render)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy
cd backend
railway login
railway init
railway up

# Set environment variables in Railway dashboard:
# - ANTHROPIC_API_KEY
# - CORS_ORIGINS (add your Vercel URL)
```

### Frontend (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel login
vercel --prod

# Set environment variable:
# NEXT_PUBLIC_API_URL = <your Railway backend URL>
```

---

## Troubleshooting

### Backend won't start

**Problem**: `ModuleNotFoundError: No module named 'backend'`

**Solution**: Run with `PYTHONPATH=.` from the project root:
```bash
cd /Users/ddhuang/Desktop/CUR/debate-ai
PYTHONPATH=. uvicorn backend.main:app --reload --port 8000
```

### Frontend can't connect to backend

**Problem**: CORS errors in browser console

**Solution**: Check `CORS_ORIGINS` in backend `.env`:
```bash
CORS_ORIGINS=http://localhost:3000
```

### SSE stream disconnects

**Problem**: EventSource closes unexpectedly

**Solution**:
1. Check backend logs for errors
2. Verify API key is valid
3. Check network/firewall settings

### Debate creation fails

**Problem**: "ANTHROPIC_API_KEY not configured"

**Solution**: Set the API key in backend `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

---

## Key Technical Decisions

### Why FastAPI over Flask?
- Native async/await support
- Built-in SSE support via `sse-starlette`
- Automatic OpenAPI documentation
- Better performance for concurrent requests

### Why SSE over WebSockets?
- Simpler protocol (one-way server → client)
- Auto-reconnect built into EventSource API
- HTTP/2 friendly
- Sufficient for our use case (server push only)

### Why In-memory Storage?
- Zero setup complexity for v1
- Fast reads/writes
- Sufficient for development/testing
- Easy migration to PostgreSQL/SQLite later

### Why No Authentication?
- Simpler MVP development
- Good for testing and demos
- Use rate limiting to prevent abuse
- Easy to add NextAuth.js later

---

## Next Steps (v2)

- [ ] Add PostgreSQL/SQLite persistence
- [ ] Add user authentication (NextAuth.js)
- [ ] Add debate favorites/bookmarks
- [ ] Add share debate via unique URL
- [ ] Add dark mode toggle
- [ ] Add API rate limiting per IP
- [ ] Add analytics dashboard
- [ ] Deploy to production

---

## Cost Estimates

Each debate costs approximately $0.04-$0.25 depending on:
- Number of rounds
- Debate style (academic is more expensive than casual-chat)
- Character complexity

100 debates ≈ $4-$25 in API costs.

---

## Support

For issues or questions:
1. Check backend logs: Look at terminal where uvicorn is running
2. Check frontend console: Open browser DevTools → Console
3. Check API docs: http://localhost:8000/docs
4. Check health endpoint: http://localhost:8000/health

---

**Built with ❤️ using Claude AI, Next.js, and FastAPI**
