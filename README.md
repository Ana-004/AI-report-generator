# AI Research Report Generator

AI Research Report Generator is a multi-agent AI system that automates the process of researching a topic, collecting information from web and academic sources, generating a structured report, reviewing the content, and producing a finalized research document.

The system combines a Streamlit user interface, FastAPI backend, LangGraph-based agent orchestration, multiple LLM providers, web research through Tavily, academic research through BASE, and PostgreSQL for persistent report storage.

## Features

* Multi-agent research and report generation
* Automated research planning
* Web research using Tavily
* Academic literature research using BASE
* AI-powered report writing
* Automated report review
* Final report formatting
* Configurable LLM model selection
* PostgreSQL report storage
* Research history
* PDF report generation
* DOCX report generation
* REST API through FastAPI
* Interactive Streamlit interface
* Health-check endpoint
* Agent execution logging
* Retrieval of recent and previously generated reports

## Architecture

The application follows a multi-agent pipeline orchestrated using LangGraph.

```text
                         User
                          |
                          v
                 Streamlit Frontend
                          |
                          v
                    FastAPI API
                          |
                          v
                 Report Generation
                          |
                          v
                  LangGraph Workflow
                          |
                          v
                       Planner 
                          |                 
                          v                 
                   Web Researcher           
                          |                 
                       (Tavily)                                                        
                          |
                          v
                Academic Researcher
                          |
                        (BASE)
                          |
                          v
                       Writer
                          |
                          v
                      Reviewer
                          |
                          v
                     Formatter
                          |
                          v
                   Final Report
                          |
             +------------+------------+
             |                         |
             v                         v
          PostgreSQL              PDF / DOCX
```

The LangGraph workflow currently connects the agents in the following sequence:

```text
START
  |
Planner
  |
Web Researcher
  |
Academic Researcher
  |
Writer
  |
Reviewer
  |
Formatter
  |
END
```

The workflow is implemented using `StateGraph` and a shared `PipelineState`, allowing information collected by one agent to be passed to subsequent agents.

## Agent Pipeline

### 1. Planner Agent

The Planner Agent analyzes the user's research topic and creates an appropriate report outline.

Responsibilities:

* Understand the research topic
* Determine relevant sections
* Create a structured report plan
* Prepare the research workflow

### 2. Web Researcher Agent

The Web Researcher Agent collects information from the web using Tavily.

Responsibilities:

* Search for relevant online information
* Retrieve multiple sources
* Collect source metadata
* Add web sources to the shared pipeline state

The current workflow is configured to retrieve up to five web research results.

### 3. Academic Researcher Agent

The Academic Researcher Agent searches academic literature using the BASE research service.

Responsibilities:

* Search academic literature
* Collect relevant research papers
* Extract publication metadata
* Add academic sources to the report research context

The current workflow is configured to retrieve up to five academic results.

### 4. Writer Agent

The Writer Agent uses the selected LLM to transform the research material and planned outline into a structured report.

Responsibilities:

* Synthesize collected sources
* Write report sections
* Maintain the selected writing style
* Incorporate citations and references
* Generate the initial report draft

### 5. Reviewer Agent

The Reviewer Agent evaluates the generated report before finalization.

Responsibilities:

* Review the generated content
* Identify weaknesses or missing information
* Provide feedback
* Improve report quality and consistency

### 6. Formatter Agent

The Formatter Agent prepares the final report after the review stage.

Responsibilities:

* Format report sections
* Produce the final report content
* Prepare the report for storage and export

## Technology Stack

| Component              | Technology                       |
| ---------------------- | -------------------------------- |
| Frontend               | Streamlit                        |
| Backend                | FastAPI                          |
| Programming Language   | Python                           |
| Agent Orchestration    | LangGraph                        |
| LLM Integration        | LiteLLM                          |
| LLM Providers          | Anthropic, OpenAI, Google Gemini |
| Web Research           | Tavily                           |
| Academic Research      | BASE                             |
| Database               | PostgreSQL                       |
| ORM                    | SQLAlchemy                       |
| PDF Generation         | ReportLab                        |
| DOCX Generation        | python-docx                      |
| Environment Management | python-dotenv                    |
| API Server             | Uvicorn                          |

The repository's dependency configuration includes FastAPI, Uvicorn, Pydantic, Anthropic, LangGraph, ReportLab, python-docx, Streamlit, Requests, Tavily, LiteLLM, SQLAlchemy, and PostgreSQL support through psycopg2.

## Project Structure

```text
AI-report-generator/
│
├── app/
│   ├── agent/
│   │   ├── base.py
│   │   ├── planner.py
│   │   ├── webResearcher.py
│   │   ├── acadResearcher.py
│   │   ├── writer.py
│   │   ├── reviewer.py
│   │   └── formatter.py
│   │
│   ├── exporter/
│   │   ├── pdf_exporter.py
│   │   └── docx_exporter.py
│   │
│   ├── graph/
│   │   ├── nodes.py
│   │   └── workflow.py
│   │
│   ├── llm/
│   │   └── factory.py
│   │
│   ├── routers/
│   │   ├── reports.py
│   │   └── report_cache.py
│   │
│   ├── services/
│   │   ├── tavily_client.py
│   │   └── base_client.py
│   │
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── state.py
│
├── app.py
├── env_example
├── requirements.txt
└── .gitignore
```

The repository currently separates agents, graph orchestration, exporters, services, LLM integration, routers, database models, schemas, and shared state into dedicated modules.

## How It Works

A user enters a research topic through the Streamlit interface.

For example:

```text
Impact of Artificial Intelligence on Healthcare
```

The application sends the request to the FastAPI backend.

The backend creates a `PipelineState` containing information such as:

* Research topic
* Report length
* Report style
* Citation format
* Selected LLM model
* Research sources
* Generated sections
* Draft
* Review notes
* Final report
* Agent logs

The LangGraph orchestrator then executes the agents sequentially.

```text
Research Topic
      |
      v
    Planner
      |
      v
 Web Research
      |
      v
Academic Research
      |
      v
    Writer
      |
      v
   Reviewer
      |
      v
  Formatter
      |
      v
 Final Report
```

The generated report is stored in PostgreSQL together with its metadata, sections, and agent logs.

## LLM Support

The application uses a configurable LLM architecture through LiteLLM.

The Streamlit interface currently provides model choices including:

```text
Claude Sonnet
GPT-4o
Gemini 1.5 Pro
```

The selected model is passed to the FastAPI backend and used by the relevant AI agents.

## Research Sources

### Tavily

Tavily is used for web-based research.

It allows the Web Researcher Agent to retrieve relevant online sources for the requested topic.

### BASE

BASE is used for academic research.

The Academic Researcher Agent uses it to retrieve academic literature and associated metadata.

The system maintains source information such as:

```text
Title
URL
Authors
Year
DOI
Source Type
Provider
External ID
```

This information is represented by the `Source` model in the shared pipeline state.

## Report Configuration

The report generation request supports configuration such as:

```text
Topic
Length
Style
Citation Format
LLM Model
```

Supported report lengths include:

```text
short
medium
long
```

Supported styles include:

```text
academic
business
technical
```

Supported citation formats include:

```text
APA
MLA
Chicago
IEEE
```

These options are represented in the application's `PipelineState`.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ana-004/AI-report-generator.git
cd AI-report-generator
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The repository provides a `requirements.txt` file containing the project's backend, AI, research, database, and document-generation dependencies.

## Environment Configuration

Create a `.env` file in the project root.

You can use the provided `env_example` file as a reference.

```env
DATABASE_URL=your_postgresql_connection_string

TAVILY_API_KEY=your_tavily_api_key

ANTHROPIC_API_KEY=your_anthropic_api_key

OPENAI_API_KEY=your_openai_api_key

GEMINI_API_KEY=your_gemini_api_key
```

The repository currently expects configuration values for PostgreSQL, Tavily, Anthropic, OpenAI, and Gemini.

Do not commit your actual `.env` file or API keys to GitHub.

## PostgreSQL Setup

The application uses PostgreSQL for persistent storage of generated reports.

Create a PostgreSQL database and configure the connection string in `.env`.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/ai_report_generator
```

The FastAPI application initializes the database tables when the application starts.

## Running the Application

The system consists of two parts:

1. FastAPI backend
2. Streamlit frontend

### Start the FastAPI Backend

From the project root:

```bash
uvicorn app.main:app --reload
```

The backend runs by default on:

```text
http://127.0.0.1:8000
```

FastAPI provides the application's REST API and initializes the database when the application starts.

### Start the Streamlit Frontend

Open another terminal and activate the same virtual environment.

Run:

```bash
streamlit run app.py
```

The Streamlit application communicates with the FastAPI backend at:

```text
http://127.0.0.1:8000
```

The frontend uses the `/reports/generate` endpoint to request report generation.

## API Endpoints

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Generate Report

```http
POST /reports/generate
```

Example request:

```json
{
  "topic": "Impact of Artificial Intelligence on Healthcare",
  "length": "medium",
  "style": "academic",
  "citation_format": "APA",
  "model": "anthropic/claude-sonnet-4-20250514"
}
```

The endpoint executes the complete multi-agent workflow and stores the generated report in PostgreSQL.

### Get Recent Reports

```http
GET /reports/recent
```

Returns the five most recently generated reports.

### Get Latest Report

```http
GET /reports/latest
```

Returns the latest generated report.

### Get Specific Report

```http
GET /reports/{report_id}
```

Example:

```http
GET /reports/1
```

### Download PDF

```http
GET /reports/{report_id}/pdf
```

Returns the selected report as a PDF document.

### Download DOCX

```http
GET /reports/{report_id}/docx
```

Returns the selected report as a Microsoft Word document.

The report router implements generation, retrieval, recent-history, PDF, and DOCX endpoints.

## Example Workflow

Suppose the user enters:

```text
The impact of generative AI on software development
```

The system performs the following process:

```text
1. User enters research topic
           |
           v
2. Planner creates report outline
           |
           v
3. Web Researcher searches Tavily
           |
           v
4. Academic Researcher searches BASE
           |
           v
5. Writer generates report draft
           |
           v
6. Reviewer evaluates the draft
           |
           v
7. Formatter prepares final report
           |
           v
8. Report is stored in PostgreSQL
           |
           v
9. User receives final report
           |
           +----> PDF
           |
           +----> DOCX
```

## Database

PostgreSQL is used to persist generated reports.

Stored information includes:

* Report ID
* Topic
* Style
* Length
* Citation format
* Selected model
* Report content
* Report sections
* Agent logs
* Creation timestamp

The report-generation endpoint creates the database record after the multi-agent workflow has completed.

## Export Formats

The application supports two document formats:

### PDF

PDF reports are generated using ReportLab.

```text
research_report.pdf
```

### DOCX

Word documents are generated using `python-docx`.

```text
research_report.docx
```

Previously generated reports can also be downloaded through the API using their report ID.

## Frontend

The Streamlit interface provides:

* Research topic input
* LLM model selection
* Report generation
* Research history
* PDF downloads
* DOCX downloads
* Pipeline visualization
* System status information

The frontend communicates with the FastAPI backend using HTTP requests.

## API Documentation

Once the FastAPI backend is running, interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

## Error Handling

The backend handles common failures during report generation.

For example, missing or invalid LLM configuration can result in an HTTP 500 response with an appropriate error message.

The frontend also displays an error when it cannot connect to the FastAPI backend.

## Security

API credentials should be stored only in environment variables.

Required secrets include:

```text
DATABASE_URL
TAVILY_API_KEY
ANTHROPIC_API_KEY
OPENAI_API_KEY
GEMINI_API_KEY
```

Never hard-code production API keys in the source code.

For production deployments, additional security measures should be implemented, including:

* Authentication and authorization
* HTTPS
* Secure secret management
* Database access restrictions
* API rate limiting
* Input validation
* Logging and monitoring

## Future Improvements

Potential improvements include:

* User authentication and account management
* Streaming agent execution
* Parallel web and academic research
* More research providers
* More LLM providers
* Custom report templates
* Citation verification
* Source credibility scoring
* Improved fact verification
* Report versioning
* Background job processing
* Docker deployment
* Cloud deployment
* Automated testing and CI/CD
* Research source caching
* Advanced observability and agent tracing

## Project Goals

The main goal of this project is to demonstrate how multiple specialized AI agents can collaborate to automate an end-to-end research workflow.

Instead of relying on a single LLM prompt, the system separates the research process into specialized stages:

```text
Planning
   |
Research
   |
Academic Research
   |
Writing
   |
Review
   |
Formatting
```

This modular architecture makes the system easier to extend, maintain, and evaluate.

## License

This project does not currently specify a license in the repository metadata. If you intend to distribute or allow reuse of the project, add an appropriate `LICENSE` file to the repository.

## Repository

GitHub repository:

https://github.com/Ana-004/AI-report-generator

## Author

Developed by Ana.

For questions, suggestions, or bug reports, please open an issue in the GitHub repository.
