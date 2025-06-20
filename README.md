# TraeDevMate - AI Pair Programmer & Code Reviewer & Deployment Master

Monk-AI is an intelligent multi-agent system that helps developers with code review, documentation generation, and test writing. Built with Trae AI IDE and integrated with Novita.ai for enhanced capabilities.


## Features

- Multi-agent system for different development tasks
- Automated PR reviews and suggestions
- Documentation generation
- Test case generation
-  Code analysis and improvement suggestions
- Context-Aware AI Dev Mentor (Auto-Learning Agent)
- Secure Code Copilot with Auto-Threat Modeling

## Tech Stack

- Backend: FastAPI (Python)
- Frontend: React + TypeScript
- AI: Trae AI Framework + Novita.ai integration
- Database: SQLite (for MVP)

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/traedevmate.git
cd traedevmate
```

2. Set up the backend:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Run the development servers:
```bash
# Backend (from root directory)
uvicorn app.main:app --reload

# Frontend (from frontend directory)
npm run dev
```

## Environment Variables

Create a `.env` file with the following variables:
```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
NOVITA_API_KEY=your_novita_key
```

## Project Structure

```
traedevmate/
├── app/
│   ├── agents/         # AI agent implementations
│   ├── api/           # API endpoints
│   ├── core/          # Core business logic
│   └── models/        # Data models
├── frontend/          # React frontend
├── tests/             # Test files
└── requirements.txt   # Python dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details 
