# 🧠 UTA Chatbot

Mav Chatbot is a conversational assistant designed to provide accurate and context-aware answers about the University of Texas at Arlington (UTA). This chatbot leverages a Retrieval-Augmented Generation (RAG) pipeline to ensure that users receive up-to-date and relevant information.

The system integrates Google Custom Search to fetch real-time web results, followed by web scraping to extract the most relevant content from the pages. The extracted text is then transformed into vector embeddings for efficient retrieval. Using LangChain, the project orchestrates the interaction between components — from search and retrieval to response generation. Finally, a powerful language model (via Groq API) is used to generate natural, context-rich answers based on the retrieved content.

---

## 🌐 Live Demo

👉 [Try it out on Streamlit!](https://mav-chatbot.streamlit.app/)

---

## 🚀 Features

- Streamlit-based interactive chatbot UI
- Google Custom Search for live web results
- Web scraping using BeautifulSoup
- Vector store using ChromaDB + Sentence Transformers
- LLM integration with Groq’s LLaMA 3 model
- Context-aware, UTA-specific answers

---

## 📁 Project Structure

```
├── app.py                # Frontend: Streamlit UI with styled chat interface
├── backend.py            # Backend: Search, scrape, vectorize, query LLM
├── requirements.txt      # Required Python packages
└── scraped_urls.txt      # Stores scraped URLs (generated at runtime)
```

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/uta-chatbot.git
cd uta-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Your API Keys

Open `backend.py` and replace the following placeholders with your actual credentials:

- `GOOGLE_API_KEY`
- `CUSTOM_SEARCH_ENGINE_ID`
- `GROQ_API_KEY`

**Optional:** Use environment variables with `.env` + `python-dotenv` for security.

### 4. Run Locally

```bash
streamlit run app.py
```

---

## 🧠 How It Works

1. **User Input**: A query is entered into the chatbot.
2. **Google Search**: The backend uses a Google Custom Search Engine to fetch relevant UTA-related results.
3. **Scraping**: Pages are scraped for clean, visible text content.
4. **Embedding + Vector Store**: Text is embedded using Sentence Transformers and stored in ChromaDB.
5. **Similarity Search**: Top matching chunks are retrieved based on the user query.
6. **LLM Prompting**: Context and question are sent to the Groq-hosted LLM for response generation.
7. **Display**: The answer is shown in the Streamlit UI.

---

## 📦 Dependencies

Listed in `requirements.txt`, including:

- `streamlit`
- `requests`
- `beautifulsoup4`
- `langchain`
- `chromadb`
- `sentence-transformers`
- `aiohttp`

---

## 📌 Notes

- Stay within rate limits for Groq and Google APIs.
- App stores temporary vector DBs and scraped URLs locally.
- Use virtual environments for cleaner setups.
- You can customize the UI via CSS in `app.py`.

---

## 🛡️ Security Tip

Don't hardcode API keys in production. Use environment variables instead.

---

## ✨ Acknowledgments

- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [Groq](https://groq.com/)
- [Google Custom Search](https://programmablesearchengine.google.com/)
