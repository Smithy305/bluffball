import streamlit as st
import requests
from google import genai
from google.genai import types

# Page Config
st.set_page_config(page_title="Bluffball AI", page_icon="⚽")

st.title("⚽ Bluffball: The Pub Survivor")
st.caption("Don't know football? Fake it until you make it.")

# --- SIDEBAR CONFIG ---
with st.sidebar:
    st.header("Configuration")
    # We use a unique key to force a reload if you change the API key
    gemini_key = st.text_input("Gemini API Key", type="password", help="Get this from Google AI Studio")
    news_key = st.text_input("News API Key", type="password", help="Get this from NewsAPI.org")
    
    st.markdown("---")
    team_name = st.selectbox("Who are we supporting?", 
                             [
                                 "Arsenal", 
                                 "Aston Villa", 
                                 "Bournemouth",
                                 "Brentford", 
                                 "Brighton & Hove Albion",
                                 "Burnley",
                                 "Chelsea", 
                                 "Crystal Palace", 
                                 "Everton", 
                                 "Fulham", 
                                 "Leeds United",
                                 "Leicester City", 
                                 "Liverpool", 
                                 "Manchester City", 
                                 "Manchester United",
                                 "Newcastle United", 
                                 "Nottingham Forest", 
                                 "Sunderland",
                                 "Tottenham Hotspur", 
                                 "West Ham United", 
                                 "Wolverhampton Wanderers"
                                 ])
    
    if st.button("Clear Chat Memory"):
        st.session_state.messages = []
        st.rerun()

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- HELPER FUNCTIONS ---
def get_news(team, api_key):
    if not api_key: return "No News API Key provided."
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": f'"{team}" AND (football OR "Premier League")', 
            "sortBy": "publishedAt", 
            "apiKey": api_key, 
            "pageSize": 3
        }
        data = requests.get(url, params=params).json()
        articles = [f"- {a['title']}" for a in data.get("articles", [])]
        if not articles: return "No specific news found today."
        return "\n".join(articles)
    except Exception as e:
        return f"News Error: {e}"

# --- MAIN CHAT LOGIC ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What did your mate just say?"):
    # 1. Validation
    if not gemini_key or not news_key:
        st.error("🚨 STOP! You need to enter both API Keys in the sidebar to play.")
        st.stop()

    # 2. Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Generate Response
    with st.chat_message("assistant"):
        status_box = st.empty() # Placeholder for status updates
        
        with st.spinner(f"Consulting the {team_name} archives..."):
            # A. Fetch Context
            news = get_news(team_name, news_key)
            
            # B. Setup Client
            client = genai.Client(api_key=gemini_key)
            
            system_instruction = f"""
            You are 'Bluffball'. 
            CONTEXT: {news}
            INSTRUCTIONS: Help the user reply to a friend about {team_name}. 
            - Adopt a persona relevant to {team_name}.
            - Keep it short (under 25 words).
            """
            
            # C. Chat History Context (Last 4 turns)
            chat_history = [m["content"] for m in st.session_state.messages[-4:]]
            full_prompt = f"Chat History: {chat_history}\n\nFriend said: {prompt}"
            
            # D. The "Robust" Fallback Logic
            response_text = ""
            
            # TRY PRIMARY MODEL (Smartest)
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_prompt,
                    config=types.GenerateContentConfig(system_instruction=system_instruction)
                )
                response_text = response.text
                
            except Exception as e_primary:
                # IF FAILED, TRY BACKUP (Most Stable)
                # status_box.warning(f"Primary model busy ({e_primary}). Switching to backup...")
                
                try:
                    response = client.models.generate_content(
                        model="gemini-flash-latest", 
                        contents=full_prompt,
                        config=types.GenerateContentConfig(system_instruction=system_instruction)
                    )
                    response_text = f"{response.text} *(Backup)*"
                except Exception as e_backup:
                    # IF BOTH FAIL, PRINT THE REAL ERROR
                    st.error(f"❌ CRITICAL ERROR: {e_backup}")
                    st.stop()
            
            # E. Display Result
            status_box.empty() # Clear status messages
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})