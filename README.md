# Project 17: Document Intelligence System

A multi-agent AI system for analyzing documents, extracting key information, and identifying potential risks. Upload legal contracts, business documents, or any text files to receive comprehensive analysis including summaries, risk flags, and decision points.

## Features

- **Document Parsing**: Supports PDF, DOCX, and TXT file formats
- **Multi-Agent Analysis**: Three specialized AI agents collaborate to analyze documents
- **Automatic Summarization**: Generates concise summaries of document content
- **Risk Detection**: Identifies potential red flags, liabilities, and risky clauses
- **Decision Extraction**: Extracts key decisions, obligations, and action items
- **Local Processing**: All analysis runs locally using Ollama LLMs - no external API dependencies

## Architecture

### Core Agents

1. **Summary Agent** (`agents/summary_agent.py`)
   - Generates concise summaries of document content
   - Identifies main themes and key points
   - Provides an overview of document structure

2. **Red Flag Detector** (`agents/red_flag_detector.py`)
   - Identifies potential risks and liabilities
   - Flags unusual or concerning clauses
   - Highlights areas requiring legal review

3. **Decision Extractor** (`agents/decision_extractor.py`)
   - Extracts key decisions and commitments
   - Identifies explicit obligations and deadlines
   - Highlights action items and responsible parties

### Supporting Components

- **Document Parser** (`utils/document_parser.py`) - Extracts text from PDF, DOCX, and TXT files
- **Orchestrator** (`orchestrator.py`) - Coordinates agent workflows
- **Streamlit Frontend** (`frontend/app.py`) - User interface for document upload and results
- **TinyDB Memory** (`memory/memory_store.json`) - Persistent document storage

## Installation

### Prerequisites

- Python 3.8 or higher
- Ollama installed and running (for local LLM inference)

### Setup Steps

1. **Navigate to the project directory**:
   ```bash
   cd SchoolOfAI/Official/soai-17-doc-intelligence
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and start Ollama** (if not already installed):
   ```bash
   # Install Ollama from https://ollama.com
   # Pull a model (llama2 is recommended)
   ollama pull llama2
   # Start Ollama service
   ollama serve
   ```

## Running the Application

1. **Start the Streamlit application**:
   ```bash
   streamlit run frontend/app.py
   ```

2. **Open your browser**: Navigate to `http://localhost:8501`

## Usage

### 1. Upload a Document

- Navigate to the Upload tab
- Drag and drop a document or click to browse
- Supported formats: `.pdf`, `.docx`, `.txt`

### 2. Analyze the Document

- Select an LLM model (llama2 is recommended)
- Click "Analyze Document" to process through all agents
- Wait for the analysis to complete

### 3. Review Results

- **Summary**: View the document summary and main themes
- **Red Flags**: Review identified risks and concerning clauses
- **Decisions**: See extracted decisions, obligations, and action items

## Workflow

```
Upload Document → Extract Text → Store in Memory → Run Agents
     ↓                ↓               ↓              ↓
  Select file    Parse PDF/DOCX   Save to TinyDB   Sequential
  from device    into text        for sharing      analysis
                                   across agents
                                               ↓
                                        Aggregate Results
                                               ↓
                                        Display to User
```

## Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root:

```env
OLLAMA_MODEL=llama2
OLLAMA_API_URL=http://localhost:11434/api/generate
```

### Ollama Models

The system supports any Ollama model. Recommended models:
- `llama2` - Good balance of speed and accuracy
- `mistral` - Faster inference
- `codellama` - Better for technical documents

To change models, modify the `OLLAMA_MODEL` environment variable or update the model parameter in the UI.

## Project Structure

```
soai-17-doc-intelligence/
├── agents/
│   ├── __init__.py
│   ├── base.py                    # Shared LLM and memory utilities
│   ├── summary_agent.py           # Generates document summaries
│   ├── red_flag_detector.py       # Identifies risks and red flags
│   └── decision_extractor.py      # Extracts decisions and obligations
├── utils/
│   ├── __init__.py
│   └── document_parser.py         # Extracts text from PDF/DOCX/TXT
├── frontend/
│   ├── app.py                    # Streamlit UI
│   └── components.py             # Reusable UI components
├── memory/
│   └── memory_store.json         # TinyDB database (auto-created)
├── uploads/                      # Temporary file storage (auto-created)
├── orchestrator.py               # Agent workflow coordination
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (optional)
└── README.md                    # This file
```

## Dependencies

- `streamlit` - Web UI framework
- `requests` - HTTP client for Ollama API
- `tinydb` - Lightweight JSON database
- `pypdf` - PDF text extraction
- `python-docx` - DOCX text extraction
- `python-dateutil` - Date/time parsing

## Troubleshooting

### Document Parsing Issues

If text extraction fails:
1. Verify the file format is supported (PDF, DOCX, TXT)
2. Check if the file is password-protected (not supported)
3. Try converting the document to plain text format

### Ollama Connection Issues

If you see connection errors:
1. Verify Ollama is running: `ollama list`
2. Check the API URL: `curl http://localhost:11434/api/generate`
3. Ensure the model is pulled: `ollama pull llama2`

### Memory/Storage Issues

If you encounter database errors:
1. Delete the memory file: `rm memory/memory_store.json`
2. The application will recreate it on next run

### Slow Performance

For faster analysis:
1. Use a smaller model like `mistral`
2. Reduce document size before uploading
3. Increase Ollama's GPU resources if available

## Use Cases

- **Legal Document Review**: Quickly identify risks in contracts and agreements
- **Business Analysis**: Extract key decisions and obligations from meeting minutes
- **Compliance Checking**: Flag clauses that may violate policies
- **Document Summarization**: Get quick overviews of long documents

## Important Notes

- This tool provides AI-generated analysis and should not replace professional legal advice
- Always review red flags and extracted decisions carefully
- Document analysis quality depends on the clarity and structure of the source document
- All processing happens locally - no data is sent to external servers

## License

This project is part of the School of AI curriculum.
