# LinkedIn Icebreaker Bot

An advanced Retrieval-Augmented Generation (RAG) application that analyzes LinkedIn profiles, generates personalized icebreakers, and answers detailed career questions through an interactive web interface.

The project supports a built-in mock profile source and live LinkedIn profile retrieval through EnrichLayer.

## Key Features

- Retrieves LinkedIn profile data through EnrichLayer or mock data
- Splits profiles into section-aware document chunks
- Generates embeddings with Google Gemini
- Stores embeddings persistently in ChromaDB
- Retrieves relevant profile evidence using LlamaIndex
- Generates grounded answers with evidence labels
- Supports contextual follow-up questions
- Provides specialized advanced Q&A modes
- Offers a Gradio web interface and command-line interface
- Includes Docker configuration and unit tests

## Advanced Q&A Modes

- **Career analysis** - Summarize experience, responsibilities, and career trajectory
- **Career comparison** - Compare roles, companies, or career periods
- **Interview preparation** - Suggest likely questions and profile-based talking points
- **Icebreaker generation** - Generate natural, personalized networking conversation starters
- **Skill and gap analysis** - Identify skills, transitions, and unsupported conclusions

## Architecture

```text
LinkedIn URL or mock source
        |
        v
Profile extraction
        |
        v
Section-aware chunking
        |
        v
Google Gemini embeddings
        |
        v
ChromaDB persistent vector store
        |
        v
LlamaIndex retrieval
        |
        v
Google Gemini + grounded prompt
        |
        v
Gradio chat or CLI response
```

## Project Structure

```text
icebreaker/
├── app.py                  # Gradio web application
├── main.py                 # Command-line application
├── config.py               # Configuration and prompt templates
├── evaluate.py             # Retrieval evaluation harness
├── Dockerfile              # Container configuration
├── requirements.txt        # Python dependencies
├── tests/
│   ├── test_app.py         # Chat interface tests
│   └── test_data_processing.py
└── modules/
    ├── data_extraction.py  # EnrichLayer and mock profile extraction
    ├── data_processing.py  # Chunking, ChromaDB, and embeddings
    ├── llm_interface.py    # Gemini LLM and embedding setup
    ├── query_engine.py     # Retrieval and grounded question answering
    └── __init__.py
```

## Requirements

- Python 3.11 or newer
- Google Gemini API key
- EnrichLayer API key for live LinkedIn profiles
- Docker, optional, for containerized execution

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/HaileyTQuach/icebreaker.git
cd icebreaker
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

For macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your-gemini-api-key
ENRICHLAYER_API_KEY=your-enrichlayer-api-key
```

The EnrichLayer key is optional when using mock profile data.

On Windows PowerShell, environment variables can also be set directly:

```powershell
$env:GEMINI_API_KEY="your-gemini-api-key"
$env:ENRICHLAYER_API_KEY="your-enrichlayer-api-key"
```

Never commit `.env` or share API keys in source code or documentation.

## Running the Web Application

```bash
python app.py
```

Open the URL printed by Gradio, usually:

```text
http://127.0.0.1:5000
```

### Web workflow

1. Enable **Use Mock Data** for a demo profile, or enter a LinkedIn URL.
2. Select a Gemini model.
3. Process the profile.
4. Open the **Chat** tab.
5. Select an advanced Q&A mode.
6. Ask about the person's roles, skills, career trajectory, experience, or networking opportunities.

Example questions:

- What are this person's strongest technical skills?
- Compare their first and most recent roles.
- What should I ask this person during an interview?
- Generate five professional icebreakers based on their career.
- What evidence suggests leadership experience?

## Running the CLI

Use mock profile data:

```bash
python main.py --mock
```

Use a live LinkedIn profile:

```bash
python main.py --url "https://www.linkedin.com/in/username/" --api-key "your-enrichlayer-api-key"
```

Select a model:

```bash
python main.py --mock --model "gemini-2.5-flash"
```

## Vector Database

Profile embeddings are persisted in ChromaDB under:

```text
data/chroma/
```

Each processed profile uses a separate session-specific collection, preventing profile data from mixing between conversations.

## Testing

Run the test suite:

```bash
python -m pytest -q
```

The tests cover:

- Section-aware profile chunking
- Chat behavior for an unloaded profile

## Retrieval Evaluation

Run the included retrieval evaluation harness:

```bash
python evaluate.py
```

This script loads mock profile data, creates embeddings, retrieves context for representative questions, and reports whether expected profile terms appear in the retrieved evidence.

## Docker

Build the image:

```bash
docker build -t icebreaker .
```

Run the container:

```bash
docker run --env-file .env -p 5000:5000 icebreaker
```

Open `http://localhost:5000`.

## Data and Privacy

- LinkedIn profile data is retrieved only for processing requested profiles
- Live profile access requires a valid EnrichLayer key
- Mock mode retrieves public demonstration data
- API keys are loaded from environment variables or `.env`
- Persistent profile collections are stored locally under `data/chroma`
- Delete `data/chroma` to remove locally persisted profile vectors

## Current Limitations

- The retrieval pipeline is grounded in profile data and may not cover information outside that profile
- ChromaDB persistence is local rather than hosted or distributed
- Session state is stored in application memory
- Answer quality depends on profile completeness and Gemini availability
- Retrieval metrics are a basic retrieval harness rather than a full production evaluation framework

## Technology Stack

- Python
- LlamaIndex
- Google Gemini
- Google Gemini Embeddings
- ChromaDB
- Gradio
- EnrichLayer
- Docker
- Pytest

## License

This project is provided for learning and portfolio demonstration.

## Acknowledgments

- LlamaIndex for retrieval and indexing infrastructure
- Google Gemini for generation and embeddings
- EnrichLayer for LinkedIn profile data retrieval
- Gradio for the interactive web interface
