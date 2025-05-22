import streamlit as st
import datetime
import random
import openai
from openai import OpenAI, RateLimitError

client = OpenAI(api_key=st.secrets["openai_api_key"])

# Simulated user database (for now)
USERS = {"tara": "mindmesh123"}

def authenticate_user():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if USERS.get(username) == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("Invalid credentials")

def get_daily_prompt(username):
    today = datetime.date.today().isoformat()
    prompt_seed = random.choice([
        "mindfulness", "gratitude", "sleep", "hydration", "focus", "financial wellness"
    ])
    user_input = f"Give {username} a motivational insight or tip about {prompt_seed}."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return response.choices[0].message.content
    except RateLimitError:
        return "⚠️ OpenAI rate limit reached. Try again later or check your API usage."
# App flow
if "logged_in" not in st.session_state:
    authenticate_user()
else:
    st.title("🌱 MindMesh: Your Daily Insight")
    st.write(f"Welcome back, {st.session_state['username']}!")

    if st.button("Get My Daily Insight"):
        with st.spinner("Generating your daily moment..."):
            daily_message = get_daily_prompt(st.session_state["username"])
            st.success(daily_message)

    if st.button("Log Out"):
        st.session_state.clear()
