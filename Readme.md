# Data Analysis Agent with Agno

## Overview

A low-code AI application built with **Agno** (formerly Phidata) that analyzes CSV, Excel, and PDF files, summarizes key statistics, embeds metadata into a vector store, and retrieves similar datasets using semantic search. It leverages **Google Gemini** for natural language understanding, **FastEmbed** for embeddings, and **Pinecone** as the vector store — all integrated through a **Streamlit** interface.

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
- Describes the data using statistical summaries via an AI agent
- Chunks and embeds summaries using FastEmbed (`all-MiniLM-L6-v2`)
- Stores embeddings in Pinecone for semantic search
- Allows querying for similar datasets
- Presents results in an easy-to-use Streamlit UI

---

## Features

- Upload and analyze CSV, Excel, and PDF files
- AI-generated dataset descriptions via Google Gemini
- Chunk and embed summary metadata automatically
- Store and search embeddings using Pinecone vector DB
- Find similar datasets with semantic search
- Download dataset summaries as CSV

---

## Tech Stack

| Component | Purpose |
|---|---|
| [Agno](https://github.com/agno-agi/agno) | Agent framework (formerly Phidata) |
| Google Gemini (`ggemini-3-flash-preview`) | Natural language generation |
| FastEmbed (`all-MiniLM-L6-v2`) | Local text embeddings via ONNX |
| Pinecone | Vector store for semantic search |
| Streamlit | Frontend interface |
| python-dotenv | Environment configuration |

---

## Project Structure

```
agentic-ai-mod6-demo-1/
├── app4.py              # Streamlit app and agent logic
├── requirements.txt     # Python dependencies
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
| **Agent** | Orchestrates tools to run analysis workflows |
| **Tools** | Describe data, embed & store metadata, search similar datasets |
| **Chunking** | Metadata split into smaller parts for embedding |
| **Embeddings** | `all-MiniLM-L6-v2` via FastEmbed for semantic similarity |
| **Vector Store** | Pinecone for persistent embedding storage and retrieval |
| **LLM** | Google Gemini for natural language responses |

---

## Example Output

**Dataset Summary (agent response):**

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
>
> Overall, the dataset is focused on workforce demographics, compensation history, and job-related factors like satisfaction and travel requirements.

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

**Semantic Search Result:**

Query: `"Prior Salary"`

> Based on your search for "Prior Salary", the following datasets are most similar as they contain explicit information regarding employee salaries and raises:
>
> **sample_data.csv**
> - Key Columns: age, employee_satisfaction, recent_salary, prior_salary, last_raise, commute_distance, percent_travel
> - Prior Salary Stats: Mean: 116,702.15 | Min: 43,975 | Max: 199,742
> - Number of records: 1,745
>
> **data.csv**
> - Key Columns: age, employee_satisfaction, recent_salary, prior_salary, last_raise, commute_distance, percent_travel, employee_id
> - Prior Salary Stats: Mean: 117,040.99 | Min: 43,975 | Max: 199,742
> - Number of records: 1,821
>
> These datasets are well-suited for analyzing salary trends, calculating pay increases (the difference between recent_salary and prior_salary should align with last_raise), and exploring correlations between salary and factors like employee satisfaction or age.

---

## Ideal For

- Data analysts and data scientists exploring multiple datasets
- Educators teaching data summarization and semantic search
- Developers building intelligent data analysis pipelines
