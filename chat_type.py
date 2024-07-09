import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-pro")


def gemini_response(input):
    response = model.generate_content(input)
    for word in response.text.split():
        yield word + " "



st.header("Answer your queries")

# initializing session state

if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask me: ")
if prompt:

    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response =""
        response_generator = gemini_response(prompt)
        for word in response_generator:
            response += word
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

