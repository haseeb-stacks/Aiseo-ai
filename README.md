# SEO Article Generator

Backend service that generates SEO-optimized articles using AI. Built for the Backend Engineer take-home assessment.

## Project Structure

```
├── app/
│   ├── agent.py           # LLM agent for article generation
│   ├── main.py            # FastAPI routes and job processing
│   ├── models.py          # Pydantic data models
│   └── services/
│       ├── serp.py        # SERP data fetching (currently mocked)
│       └── storage.py     # Job persistence layer
├── tests/
│   └── test_main.py       # Integration tests
├── .env                   # Environment configuration
├── requirements.txt       # Python dependencies
├── environment.yml        # Conda environment spec
├── EXAMPLE.md            # Input/output example
└── README.md             # This file
```

## Quick Start

```bash
# Install dependencies
conda activate vents
pip install -r requirements.txt

# Start the server
PYTHONPATH=. uvicorn app.main:app --reload

# Run tests
PYTHONPATH=. pytest tests/test_main.py -v
```

API documentation: http://127.0.0.1:8000/docs

## Features Implemented

### Core Requirements ✓
- ✅ Agent-based system analyzing SERP data
- ✅ Structured article generation (H1, H2, H3)
- ✅ SEO metadata (title tag, meta description, keywords)
- ✅ Internal linking suggestions (3-5)
- ✅ External references (2-4 authoritative sources)
- ✅ Pydantic models for validation
- ✅ Graceful error handling
- ✅ Job persistence and tracking

### Bonus Features ✓
- ✅ Job management (pending, running, completed, failed)
- ✅ Durability (jobs persist to disk, can resume)
- ✅ Test coverage

## How It Works

1. **Job Creation**: POST to `/jobs` with topic, word count, and language
2. **SERP Analysis**: System fetches top 10 search results (currently mocked)
3. **Article Generation**: LLM analyzes SERP data and generates SEO-optimized content
4. **Persistence**: Job saved to `jobs.json` with status tracking
5. **Retrieval**: GET `/jobs/{id}` returns complete result

## Configuration

The system supports both OpenAI and Ollama. Set via `.env`:

**Ollama (default):**
```
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=gemma3:4b
```

**OpenAI:**
```
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-4o
```

## Design Decisions

**Background Processing**: FastAPI's BackgroundTasks handles async article generation without blocking the API response.

**Job Persistence**: Simple JSON file storage (`jobs.json`) provides durability while keeping the implementation straightforward. Easy to swap for a database later.

**LLM Abstraction**: OpenAI client works with both OpenAI and Ollama (via OpenAI-compatible API), making it easy to switch providers.

**SERP Mocking**: Currently generates realistic mock data. Production version would integrate SerpAPI or similar by updating `app/services/serp.py`.

**Structured Output**: Pydantic models + LLM JSON mode ensures consistent, validatable output every time.

## Testing

```bash
PYTHONPATH=. pytest tests/test_main.py -v
```

Tests verify:
- Job creation and status tracking
- Article generation with all required fields
- SERP data collection
- Error handling

## Example

See [EXAMPLE.md](EXAMPLE.md) for a complete input → output demonstration.

Quick test:
```bash
curl -X POST "http://127.0.0.1:8000/jobs" \
  -H "Content-Type: application/json" \
  -d '{"topic": "best productivity tools", "word_count": 1000, "language": "English"}'
```

## Future Enhancements

- Real SERP API integration (SerpAPI, DataForSEO)
- Content quality scoring
- FAQ generation from search results
- Database backend for job storage
- Rate limiting and caching