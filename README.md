# AI Historical Debate Generator

A dynamic debate generation system that simulates intellectual discourse between historical figures using Claude AI. The system performs real-time research on any two individuals, constructs authentic character models based on their documented philosophies and rhetorical styles, then generates multi-turn debates that reflect their actual intellectual positions.

## Overview

This project addresses a fundamental challenge in AI-assisted historical analysis: how to generate historically plausible dialogues without hardcoding biographical information. Unlike traditional chatbots that rely on pre-programmed personas, this system dynamically researches each historical figure at runtime, building character models from scratch based on available knowledge.

The implementation uses a two-phase approach. First, the character builder performs deep research on each participant, analyzing their historical context, core philosophical positions, argumentative patterns, and documented communication styles. Second, the debate engine orchestrates a structured multi-turn exchange, maintaining separate conversational contexts for each participant to ensure consistent characterization throughout the debate.

## Architecture

The system consists of three main components:

**Character Builder**: Generates dynamic character profiles through AI-driven historical research. Each profile includes biographical context, ideological framework, rhetorical patterns, and topic-specific stance analysis. The builder adapts to different levels of historical documentation, handling everyone from well-documented philosophers to more obscure figures.

**Debate Engine**: Manages the debate flow and maintains conversational coherence. The engine uses separate message histories for each character, allowing them to build upon their own arguments while responding to their opponent. This context isolation ensures that characters remain consistent in their reasoning across multiple turns.

**Prompt System**: Provides style-aware templates that adapt to different debate formats. The system supports four distinct modes: academic discourse (detailed, evidence-based arguments), casual conversation (concise exchanges), heated debate (confrontational rhetoric), and collaborative performance (comedic dialogue rather than adversarial debate).

## Technical Implementation

### CLI Usage

The command-line interface provides direct access to debate generation:

```bash
python debate.py --p1 "Confucius" --p2 "Socrates" --topic "virtue" --style academic --rounds 5
```

Available parameters include debate style (academic, casual-chat, heated-debate, comedy-duo), round count, language output (Chinese or English), and language register for Chinese output (classical, semi-classical, modern vernacular). Custom word limits can override style defaults.

The CLI outputs both to terminal (with color-coded formatting via Rich library) and markdown files. Each debate is saved with complete metadata including generation timestamp, model version, and configuration parameters.

### Web Interface

A Next.js frontend provides browser-based access with real-time streaming:

**Backend**: FastAPI server wraps the existing debate generation modules without modification. The server uses Server-Sent Events (SSE) to stream progress updates as characters are researched and debate rounds are generated. An in-memory job queue manages concurrent debate requests.

**Frontend**: React components consume the SSE stream, displaying messages as they're generated. The interface includes a debate gallery showing historical debates, a form for creating new debates with style selection, and a viewer with live progress tracking.

To run the web interface:

```bash
# Backend (FastAPI)
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env to add your ANTHROPIC_API_KEY

cd ..
PYTHONPATH=. uvicorn backend.main:app --reload --port 8000

# Frontend (Next.js)
cd frontend
npm install
npm run dev
```

Access the interface at http://localhost:3000. The backend API documentation is available at http://localhost:8000/docs.

## Debate Styles

The system implements four distinct debate formats, each optimized for different use cases:

**Academic**: Designed for in-depth intellectual exchange. Characters provide detailed reasoning with 250-400 character responses over typically 5 rounds. This style emphasizes logical progression and evidence-based argumentation. The temperature setting (0.8) balances creativity with coherent reasoning.

**Casual Chat**: Enables rapid conversational exchange with 30-50 character responses over 10+ rounds. Higher temperature (0.9) produces more varied responses while maintaining character consistency. This format works well for exploring how historical figures might discuss topics in informal settings.

**Heated Debate**: Produces confrontational discourse with 40-60 character responses over approximately 8 rounds. Maximum temperature (1.0) generates more unpredictable and emotionally charged rhetoric while staying within character bounds. Prompts encourage sharp disagreements and rhetorical intensity.

**Comedy Duo**: A collaborative rather than adversarial mode where characters perform together rather than debating. This style (30-50 characters, 12 rounds, temperature 0.95) treats the topic as material for joint exploration rather than a point of contention. The system assigns "lead" and "support" roles similar to traditional comedy partnerships.

## Context Management

Each character maintains an independent message history throughout the debate. When generating a response, the system provides that character's complete prior statements along with their opponent's most recent argument. This approach allows characters to build cumulative cases across multiple turns while responding specifically to counterarguments.

The isolation of contexts prevents characters from "knowing" how their opponent formulated arguments internally. They only see the final statements, much like in actual debates. This architectural choice significantly improves the realism of exchanges compared to shared context approaches.

## Implementation Details

The codebase follows a modular architecture:

```
src/
├── ai_client.py          # Claude API wrapper with retry logic
├── character_builder.py  # Dynamic character profile generation
├── debate_engine.py      # Turn management and context handling
├── prompter.py           # Style-aware prompt templates
├── formatter.py          # Terminal and markdown output
└── style_config.py       # Debate style parameters

backend/
├── main.py               # FastAPI application
├── routes/               # REST endpoints and SSE streaming
└── services/             # Job queue and debate orchestration

frontend/
├── app/                  # Next.js pages (App Router)
├── components/           # React UI components
├── hooks/                # SSE connection hook
└── lib/                  # API client and utilities
```

The CLI and web interface share the same core debate generation code. The backend server imports the original modules directly rather than wrapping them as subprocesses, reducing latency and simplifying error handling.

## API Costs

Each debate consumes Claude API tokens based on the depth of character research and the number of debate rounds. Typical costs range from $0.04 to $0.25 per debate, depending on configuration. Academic style with more rounds costs more than casual style with fewer rounds. The system uses Claude Sonnet 4.5 by default.

Character research accounts for a significant portion of token usage, as the system performs detailed analysis of each participant before generating debate content. This upfront investment ensures higher quality characterization throughout the exchange.

## Limitations

The system's output quality depends on Claude's training data coverage of the specified historical figures. Well-documented philosophers and scientists typically produce more historically grounded debates than obscure or poorly documented individuals. The system will attempt to construct plausible characterizations for any named person, but accuracy varies with available training data.

Generated content represents plausible extrapolations of documented positions rather than verified historical statements. The system should be used for exploration and education rather than as a source of historical facts. All generated debates are labeled as AI-generated and include metadata about the generation process.

The debate engine does not fact-check claims or ensure historical accuracy beyond what's implicit in the character research phase. Characters may make anachronistic references or cite developments that occurred after their deaths if the debate topic relates to later events.

## Development

The project uses Python 3.8+ for the core system and Node.js 18+ for the web frontend. Key dependencies include:

- anthropic: Claude API access
- fastapi: Web backend framework
- sse-starlette: Server-sent events support
- next.js: React framework for frontend
- rich: Terminal formatting (CLI only)

The codebase maintains separation between the original CLI implementation and the web interface additions. All original modules in src/ remain unmodified, with the web backend importing them directly.

## Installation

```bash
# Clone repository
git clone https://github.com/hexal1029/debate-ai.git
cd debate-ai

# CLI setup
pip install -r requirements.txt
cp .env.example .env
# Add ANTHROPIC_API_KEY to .env

# Web setup (optional)
cd backend && pip install -r requirements.txt && cd ..
cd frontend && npm install && cd ..
```

For detailed web interface setup instructions, see the backend and frontend directories.

## License

This project is provided for educational and research purposes. Generated content should not be cited as historical fact or used as authoritative source material.
