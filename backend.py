
# %%writefile backend.py
import streamlit as st
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import aiohttp
import asyncio

# Import necessary classes from LangChain
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma




GOOGLE_API_KEY = "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"  # Replace with your Google API key
CUSTOM_SEARCH_ENGINE_ID = "d4d5c5f3dd58e41b3"  # Replace with your Custom Search Engine ID

# Groq API configuration
GROQ_API_KEY = "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"  # Replace with your Groq API key or other LLM API key
CHROMA_DB_DIR = "chroma_db"            # Directory to store your vector database
EMBEDDING_MODEL = "all-MiniLM-L6-v2"     # Embedding model for text representation
GROQ_MODEL = "llama3-70b-8192"




def google_site_search(query, api_key, cse_id, num_results=5):
    """
    Performs a Google Custom Search limited to the site specified in your CSE.

    Args:
        query (str): The search query.
        api_key (str): Your Google API key.
        cse_id (str): Your Custom Search Engine ID.
        num_results (int): Number of search results to return (max=10 per request).

    Returns:
        list: A list of dictionaries containing titles, links, and snippets.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": num_results
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get("items", [])
        formatted_results = []
        for item in results:
            formatted_results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })
        return formatted_results
    else:
        print("Error during Google search:", response.status_code, response.text)
        return []





def scrape_text_from_url(url):
    """
    Scrapes the visible text content from the provided URL.

    Args:
        url (str): The URL to scrape.

    Returns:
        Document: A LangChain Document containing the scraped text and metadata.
    """
    print(f"Scraping URL: {url}")
    try:
        response = requests.get(url, timeout=7)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove non-visible elements
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        # Extract and clean visible text
        elements = soup.find_all(text=True)
        visible_text = [el.strip() for el in elements if el.strip()]
        clean_text = "\n".join(visible_text)
        return Document(page_content=clean_text, metadata={"source": url})
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


def query_groq(prompt):
    """
    Sends a prompt to the Groq API and retrieves the answer.

    Args:
        prompt (str): The final prompt containing your context and question.

    Returns:
        str: The answer provided by the language model.
    """
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("Error calling Groq API:", response.status_code, response.text)
        return "Error retrieving answer."




def get_chatbot_response(user_query):
    try:
        # Step 1: Get search results
        search_results = google_site_search(user_query, GOOGLE_API_KEY, CUSTOM_SEARCH_ENGINE_ID)
        if not search_results:
            return "No search results found."
        
        # Optional: Save URLs for reference
        with open("scraped_urls.txt", "w") as f:
            for result in search_results:
                f.write(result["link"] + "\n")
        
        # Step 2: Scrape content
        documents = []
        for result in search_results:
            doc = scrape_text_from_url(result["link"])
            if doc and doc.page_content.strip():
                documents.append(doc)
            time.sleep(1)
            
        if not documents:
            return "No documents was successfully scraped."
        
        # Step 3: Split documents into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = splitter.split_documents(documents)
        
        # Step 4: Create vector DB and generate embeddings
        try:
            embedding_function = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
            vectordb = Chroma.from_documents(docs, embedding=embedding_function, persist_directory=CHROMA_DB_DIR)
            vectordb.persist()
        except Exception as e:
            st.error("Error creating vector database: " + str(e))
            return "Error in vector database creation."
        
        # Step 5: Similarity search to get context
        similarity_results = vectordb.similarity_search(user_query, k=4)
        context = "\n\n".join([doc.page_content for doc in similarity_results])
        
        # Step 6: Compose the final prompt and query the LLM
        final_prompt = f"""You are an expert assistant for the University of Texas at Arlington (UTA).
    Answer the question using the context below. Be concise and clear.
    
    Context:
    {context}
    
    Question: {user_query}
    
    Answer:"""
        answer = query_groq(final_prompt)
        return answer

    except Exception as error:
        # Capture any error and return it for debugging
        st.error("An error occurred in get_chatbot_response: " + str(error))
        return "An error occurred while retrieving the answer."
