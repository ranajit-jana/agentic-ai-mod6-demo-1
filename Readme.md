Data Analysis Agent with Agno
🔍 Overview
This is a low-code AI application built with Agno (formerly Phidata), designed to analyze CSV files, summarize key statistics, embed metadata, and retrieve similar datasets using semantic search. It leverages Google Gemini for natural language understanding, SentenceTransformers for embeddings, and Pinecone as a vector store, all integrated through a Streamlit interface.
📘 Scenario
Suppose a data analyst is working with multiple CSV datasets and wants to quickly:
•	Understand the structure and statistical summary of each dataset,
•	Index summaries for fast semantic retrieval,
•	Search for similar datasets based on metadata patterns.
This tool automates that workflow — uploading a CSV file generates a summary, stores metadata embeddings in Pinecone, and enables natural language queries to retrieve similar datasets.
🧩 Problem Statement
Create a CSV Data Insights application that:
•	Accepts user-uploaded CSV files,
•	Describes the data using statistical summaries,
•	Chunks and embeds summaries using SentenceTransformers,
•	Stores embeddings in Pinecone for semantic search,
•	Allows querying for similar datasets,
•	Presents results in an easy-to-use Streamlit UI.
________________________________________
🛠️ Features
•	📂 Upload and analyze CSV files
•	📈 View detailed data summaries
•	🧩 Chunk & embed summary metadata
•	🧠 Store and search using Pinecone vector DB
•	🔍 Query similar datasets with semantic search
•	📤 Download dataset summaries as CSV
________________________________________
🧠 Tech Stack
•	Phidata (Agno) – Agent framework and workflow orchestration
•	Google Gemini API – Natural language generation
•	SentenceTransformers – Text embedding via all-MiniLM-L6-v2
•	Pinecone – Vector store for semantic search
•	Streamlit – Frontend interface
•	dotenv – Environment configuration
________________________________________

📦 Project Structure
├── app.py                # Streamlit frontend and main app logic
├── .env                  # API key and environment variables
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
________________________________________
⚙️ Setup Instructions
1. Clone the Repository
git clone https://github.com/your-username/csv-data-insights.git
cd csv-data-insights
2. Create and Activate Virtual Environment
python -m venv venv
source venv/bin/activate      # or venv\Scripts\activate on Windows
3. Install Dependencies
pip install -r requirements.txt
4. Add API Keys
Create a .env file in the root directory and add:
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key
5. Run the Application
streamlit run app4.py
________________________________________
📚 Key Concepts in Use
•	✅ Agent: Orchestrates tools to run analysis workflows
•	🧰 Tools: Describe CSV, Embed & Store metadata, Search similar
•	✂️ Chunking: Metadata split into digestible parts for embedding
•	🧠 Embeddings: Using all-MiniLM-L6-v2 for semantic similarity
•	📦 Vector Store: Pinecone for persistent embedding storage
•	🖼️ LLM: Google Gemini for question-answering and UI responses
•	🖥️ UI: Streamlit frontend for file upload and report interaction
________________________________________
📈 Example Output
Dataset Summary:
	age	employee_satisfaction	recent_salary	prior_salary	last_raise	employee_id
count	1821	1821	1821	1821	1821	1821	
mean	47.4849	65.34761	124521.5	117041	7480.488	2E+09	
std	7.37373	20.59141	43997.97	41595.74	6361.387	525.8217	
min	35	30	50011	43975	0	2E+09	
25%	41	47	85275	80658	1962	2E+09	
50%	47	65	124544	116950	6318	2E+09	
75%	54	84	162981	153402	11720	2E+09	
max	61	100	199951	199742	25995	2E+09	
							

Semantic Query: "Find datasets similar to sales data from Q2"
Results:
ID: uploaded_data.csv_chunk_0, Score: 0.87
ID: sales_2023_chunk_3, Score: 0.85
...
________________________________________
👤 Ideal For
•	Data analysts and data scientists
•	Educators teaching data summarization and semantic search
•	Developers building intelligent CSV analysis pipelines
