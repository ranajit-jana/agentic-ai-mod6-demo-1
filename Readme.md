# Data Analysis Agent with Agno

## Overview

A low-code AI application built with **Agno** (formerly Phidata) that analyzes CSV, Excel, and PDF files, summarizes key statistics, embeds metadata into a vector store, and retrieves similar datasets using semantic search. It uses **3 dedicated AI agents** — each with a single responsibility — powered by **Google Gemini**, with **FastEmbed** for local embeddings and **Pinecone** as the vector store, all integrated through a **Streamlit** interface.

---

## Scenario

A data analyst working with multiple datasets wants to quickly:

- Understand the structure and statistical summary of each dataset
- Index summaries for fast semantic retrieval
- Search for similar datasets based on metadata patterns

This tool automates that workflow — uploading a file generates an AI summary, stores metadata embeddings in Pinecone, and enables natural language queries to retrieve similar datasets.

---

## Problem Statement

Build a Data Insights application that:

- Accepts user-uploaded CSV, Excel, and PDF files
- Describes the data using statistical summaries via a dedicated AI agent
- Chunks and embeds summaries using FastEmbed (`all-MiniLM-L6-v2`)
- Stores embeddings in Pinecone for semantic search
- Allows querying for similar datasets via a dedicated search agent
- Presents results in an easy-to-use Streamlit UI

---

## Features

- Upload and analyze CSV, Excel, and PDF files
- AI-generated dataset descriptions via Google Gemini
- Automatic chunk, embed, and store of metadata into Pinecone
- Find similar datasets with semantic search
- 3 independent agents — isolated, debuggable, single-responsibility
- Download dataset summaries as CSV

---

## Tech Stack

| Component | Purpose |
|---|---|
| [Agno](https://github.com/agno-agi/agno) | Agent framework (formerly Phidata) |
| Google Gemini (`gemini-1.5-flash`) | Natural language generation |
| FastEmbed (`all-MiniLM-L6-v2`) | Local text embeddings via ONNX — no API needed |
| Pinecone | Vector store for semantic search |
| Streamlit | Frontend interface |
| python-dotenv | Environment configuration |

---

## Architecture — 3 Dedicated Agents

This app uses **3 separate agents**, each with a single tool and a single responsibility. This makes failures easy to isolate and each agent easy to debug independently.

| Agent | Tool | Responsibility |
|---|---|---|
| `describe_agent` | `describe_data` | Reads a file and generates a natural language summary |
| `store_agent` | `embed_and_store` | Chunks the summary, embeds it, and stores in Pinecone |
| `search_agent` | `search_similar` | Converts a query to a vector and finds similar datasets |

```python
describe_agent = Agent(tools=[describe_data], model=model, name="Describe Agent")
store_agent    = Agent(tools=[embed_and_store], model=model, name="Store Agent")
search_agent   = Agent(tools=[search_similar], model=model, name="Search Agent")
```

---

## Application Workflow

```
STARTUP (once)
  .env → GOOGLE_API_KEY, PINECONE_API_KEY
  Gemini(gemini-1.5-flash) initialized
  Pinecone "data-insights" index created if missing
  FastEmbed loads all-MiniLM-L6-v2 locally
         │
         ▼
USER UPLOADS A FILE (CSV / Excel / PDF)
  Streamlit reads file → pandas DataFrame
  File saved to disk using its original filename
         │
         ▼
describe_agent.run("Describe the dataset in <filename>")
  → describe_data() tool called
  → pandas loads file, computes statistics
  → Gemini generates plain English narrative
  → Displayed in UI via st.markdown()
         │
         ▼
store_agent.run("Embed and store the dataset at <filename>")
  → embed_and_store() tool called
  → Summary split into 300-character chunks
  → FastEmbed converts each chunk → 384-dim vector
  → Vectors upserted to Pinecone with ID "<filename>_chunk_N"
  → Confirmation shown in UI via st.info()
         │
         ▼
Raw stats table shown (st.dataframe) + Download CSV button

─────────────────────────────────────────

USER TYPES A SEARCH QUERY (always visible)
         │
         ▼
search_agent.run("Search for datasets similar to: <query>")
  → search_similar() tool called
  → FastEmbed converts query → 384-dim vector
  → Pinecone returns top-5 closest stored vectors
  → Gemini formats matches into readable response
  → Displayed in UI via st.markdown()
```

---

## Project Structure

```
agentic-ai-mod6-demo-1/
├── app4.py              # Streamlit app — agents, tools, UI
├── requirements.txt     # Python dependencies
├── setup.txt            # Step-by-step setup instructions
├── .env                 # API keys (not committed)
├── .gitignore
└── Readme.md
```

---

## Setup Instructions

### 1. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 2. Activate the Virtual Environment

```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> On first run, FastEmbed will download the `all-MiniLM-L6-v2` model (~91MB). This is a one-time download cached at `~/.cache/fastembed/`.

### 4. Add API Keys

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

### 5. Run the Application

```bash
streamlit run app4.py
```

The app will open at `http://localhost:8501`

---

## Key Concepts

| Concept | Description |
|---|---|
| **Agent** | An AI unit with a model and a set of tools — decides when and how to use them |
| **Tool** | A Python function decorated with `@tool` — performs a specific task |
| **Chunking** | Long text split into smaller parts so each chunk fits in an embedding |
| **Embeddings** | Numbers (384-dim vectors) representing the meaning of text |
| **Vector Store** | Pinecone stores embeddings and finds the closest ones to a query |
| **Semantic Search** | Finding datasets by meaning, not exact keyword match |

---

## Example Output

**Dataset Summary — `describe_agent`:**

File: `sample_data.csv`

> The dataset contains 1,745 entries with various employee-related metrics. Here is a description of the key columns:
>
> - **Age:** Ranges from 35 to 61 years, average ~47.5 years
> - **Employee Satisfaction:** Score from 30 to 100, average 65.4
> - **Recent Salary:** $50,011 to $199,951, average ~$124,223
> - **Prior Salary:** $43,975 to $199,742, average ~$116,702
> - **Last Raise:** $0 to $25,995, average ~$7,521
> - **Commute Distance:** 0 to 45 units, average 22.6
> - **Percent Travel:** 10% to 100%, average 54.4%

**Statistical Table:**

| Metric | Age | Satisfaction | Recent Salary | Prior Salary | Last Raise | Commute | % Travel |
|--------|-----|-------------|---------------|--------------|------------|---------|----------|
| count  | 1745 | 1745 | 1745 | 1745 | 1745 | 1745 | 1745 |
| mean   | 47.5 | 65.4 | 124,224 | 116,702 | 7,521 | 22.6 | 54.4 |
| std    | 7.4 | 20.6 | 43,858 | 41,429 | 6,343 | 13.3 | 26.6 |
| min    | 35 | 30 | 50,011 | 43,975 | 0 | 0 | 10 |
| 25%    | 41 | 47 | 85,275 | 80,584 | 2,002 | 11 | 31 |
| 50%    | 48 | 65 | 123,622 | 116,434 | 6,335 | 22 | 53 |
| 75%    | 54 | 84 | 162,742 | 153,167 | 11,733 | 34 | 78 |
| max    | 61 | 100 | 199,951 | 199,742 | 25,995 | 45 | 100 |

**Semantic Search — `search_agent`:**

Query: `"Prior Salary"`

> Based on your search for "Prior Salary", the following datasets are most similar:
>
> **sample_data.csv**
> - Key Columns: age, employee_satisfaction, recent_salary, prior_salary, last_raise, commute_distance, percent_travel
> - Prior Salary Stats: Mean: 116,702.15 | Min: 43,975 | Max: 199,742
> - Records: 1,745
>
> **data.csv**
> - Key Columns: age, employee_satisfaction, recent_salary, prior_salary, last_raise, commute_distance, percent_travel, employee_id
> - Prior Salary Stats: Mean: 117,040.99 | Min: 43,975 | Max: 199,742
> - Records: 1,821
>
> These datasets are well-suited for analyzing salary trends and exploring correlations between salary and factors like employee satisfaction or age.

---

## Ideal For

- Data analysts and data scientists exploring multiple datasets
- Educators teaching agentic AI, RAG, and semantic search
- Developers building intelligent data analysis pipelines
