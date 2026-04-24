import os
import io
import pandas as pd
import streamlit as st
from PyPDF2 import PdfReader
from agno.agent import Agent
from agno.tools import tool
from agno.models.google import Gemini
from pinecone import Pinecone, ServerlessSpec
from fastembed import TextEmbedding
from dotenv import load_dotenv

# ---- 1. Load Environment Variables from .env ----
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# ---- 2. Initialize LLM ----
model = Gemini(id="gemini-3-flash-preview" , api_key=GOOGLE_API_KEY)

# ---- 3. Initialize Pinecone (v7 syntax) ----
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "data-insights"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

# ---- 4. Load SentenceTransformer model for embeddings ----
embedding_model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ---- 5. Tool: Describe CSV/Excel data ----
@tool
def describe_data(filepath: str) -> str:
    df = pd.read_csv(filepath) if filepath.endswith(".csv") else pd.read_excel(filepath)
    return df.describe().to_string()

# ---- 6. Tool: Chunk, Embed, and Store CSV/Excel metadata ----
@tool
def embed_and_store(filepath: str) -> str:
    df = pd.read_csv(filepath) if filepath.endswith(".csv") else pd.read_excel(filepath)
    text_summary = df.describe().to_string()

    max_chunk_size = 300
    chunks = [text_summary[i:i+max_chunk_size] for i in range(0, len(text_summary), max_chunk_size)]

    vectors = []
    for i, chunk in enumerate(chunks):
        embedding = list(embedding_model.embed([chunk]))[0].tolist()
        vector_id = f"{filepath}_chunk_{i}"
        vectors.append((vector_id, embedding))

    index.upsert(vectors=vectors)
    return f"Stored {len(vectors)} chunks for {filepath}"

# ---- 7. Tool: Search similar datasets by metadata ----
@tool
def search_similar(query: str) -> str:
    query_embedding = list(embedding_model.embed([query]))[0].tolist()
    results = index.query(vector=query_embedding, top_k=5, include_metadata=False)
    matches = [f"ID: {match['id']}, Score: {match['score']}" for match in results['matches']]
    return "\n".join(matches)

# ---- 8. Create the Agent ----
agent = Agent(
    tools=[describe_data, embed_and_store, search_similar],
    model=model,
    name="Data Analyst Agent",
    description="Analyzes CSV, Excel, and PDF files, chunks and stores metadata, and retrieves similar datasets."
)


# ---- 9. Streamlit UI ----
st.title("Data Analysis Agent")

uploaded_file = st.file_uploader(
    label="Upload a data file (CSV, Excel, or PDF)",
    type=["csv", "xlsx", "xls", "pdf"],
    help="Supported formats: .csv, .xls, .xlsx, .pdf"
)

st.caption("Supports CSV, Excel (.xls/.xlsx), and PDF files. Max size: 200MB.")

if uploaded_file is not None:
    try:
        file_type = uploaded_file.name.split('.')[-1].lower()

        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
            st.success("CSV file loaded successfully!")
            file_summary_df = df.describe()

        elif file_type in ["xlsx", "xls"]:
            df = pd.read_excel(uploaded_file)
            st.success("Excel file loaded successfully!")
            file_summary_df = df.describe()

        elif file_type == "pdf":
            pdf_reader = PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            file_summary = text if text else "No extractable text found in PDF."
            st.success("PDF file loaded successfully!")

        else:
            st.error("Unsupported file format.")
            file_summary_df = None

        # For CSV and Excel, save file temporarily and run the agent
        if file_type in ["csv", "xlsx", "xls"]:
            temp_path = uploaded_file.name
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            response = agent.run(f"Describe the dataset in {temp_path}")
            st.subheader("Dataset Summary from Agent")
            st.markdown(response.content if hasattr(response, "content") else str(response))

            with st.spinner("Storing dataset in Pinecone for future comparison..."):
                store_response = agent.run(f"Embed and store the dataset at {temp_path}")
                st.info(store_response.content if hasattr(store_response, "content") else str(store_response))

        elif file_type == "pdf":
            st.write("Extracted PDF Text Summary:")
            st.text(file_summary)

        # Show basic summary and download button for CSV/Excel
        if file_type in ["csv", "xlsx", "xls"] and file_summary_df is not None:
            st.write("Basic Summary:")
            st.dataframe(file_summary_df)

            csv_bytes = file_summary_df.to_csv().encode('utf-8')
            st.download_button(
                label="Download Summary as CSV",
                data=csv_bytes,
                file_name="summary.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error processing file: {e}")

# ---- Find Similar Datasets ----
st.divider()
st.subheader("Find Similar Datasets")
search_query = st.text_input(
    "Describe what you're looking for:",
    placeholder="e.g. sales data with revenue and profit columns"
)
if st.button("Search Similar Datasets") and search_query:
    with st.spinner("Searching Pinecone..."):
        try:
            search_response = agent.run(f"Search for datasets similar to: {search_query}")
            result_text = search_response.content if hasattr(search_response, "content") else str(search_response)
            st.markdown(result_text)
        except Exception as e:
            st.error(f"Search failed: {e}")
