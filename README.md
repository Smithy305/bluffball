# ⚽ Bluffball: The AI Pub Survivor

A Retrieval-Augmented Generation (RAG) application that helps non-football fans hold their own in pub conversations.

🔗 **Live Demo:** [Click here to use Bluffball](https://bluffball-8uzjpkved7w5ttojubhunt.streamlit.app/)

## 📺 The Inspiration
This project is a real-world implementation of the "Bluffball" website from *The IT Crowd*.
> *"Did you see that ludicrous display last night?"*

[Watch the original clip here](https://www.youtube.com/watch?v=MpjYGjSeLoE)

## 🏗 Architecture
* **Frontend:** Streamlit (Python)
* **AI Engine:** Google Gemini 2.5 Flash (Primary) + Gemini Flash Latest (Backup)
* **Data Sources:** NewsAPI (Live Context) + Static Squad Lists (Structured Data)

## 📜 Project Evolution
This tool started as a simple terminal script before evolving into a web application:
1.  **Phase 1: The CLI Prototype (`bluffball.py`)** - I initially built a Python script to test the RAG logic in the terminal. You can still run this file locally to see the raw "backend" logic without the UI.
2.  **Phase 2: The Web App (`app.py`)** - Once the logic was solid, I wrapped it in Streamlit to make it accessible on mobile devices for "in-the-field" use (i.e., at the pub).

## 🚀 Key Features
* **Context-Aware Persona:** The AI adopts the slang, nicknames, and tone of the selected team (e.g., "Geordie" for Newcastle, "Scouse" for Liverpool).
* **Self-Healing Backend:** Implements a `try/except` failover pattern. If the primary LLM is overloaded (HTTP 429/503), the system automatically routes the prompt to a fallback model to ensure zero downtime.
* **Hallucination Guardrails:** System prompts are engineered to prioritize "News Context" over internal training data to prevent the bot from referencing outdated players.

## 🛠 How to Run Locally
1.  Clone the repo
2.  Install dependencies: `pip install -r requirements.txt`
3.  Run the app: `streamlit run app.py`
