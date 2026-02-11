# ⚽ Bluffball: The AI Pub Survivor

A Retrieval-Augmented Generation (RAG) application that helps non-football fans hold their own in pub conversations.

🔗 **Live Demo:** [Click here to use Bluffball](https://bluffball-8uzjpkved7w5ttojubhunt.streamlit.app/)

## 🏗 Architecture
* **Frontend:** Streamlit (Python)
* **AI Engine:** Google Gemini 2.5 Flash (Primary) + Gemini Flash Latest (Backup)
* **Data Sources:** NewsAPI (Live Context) + Static Squad Lists (Structured Data)

## 🚀 Key Features
* **Context-Aware Persona:** The AI adopts the slang, nicknames, and tone of the selected team (e.g., "Geordie" for Newcastle, "Scouse" for Liverpool).
* **Self-Healing Backend:** Implements a `try/except` failover pattern. If the primary LLM is overloaded (HTTP 429/503), the system automatically routes the prompt to a fallback model to ensure zero downtime.
* **Hallucination Guardrails:** System prompts are engineered to prioritize "News Context" over internal training data to prevent the bot from referencing outdated players.

## 🛠 How to Run Locally
1.  Clone the repo
2.  Install dependencies: `pip install -r requirements.txt`
3.  Run the app: `streamlit run app.py`
