import openai
import os
import logging
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize a dictionary to store cached responses
cache = {}

def get_openai_response(messages):
    logging.info("Sending request to OpenAI API")
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message['content'].strip()

def handle_userinput(user_question):
    logging.info(f"Handling user input: {user_question}")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": '''You are Esti, an assistant that has the persona of a female, 25 years old. 
                You work in Salam Pacific Indonesia Lines as a customer service. 
                You are a friendly and helpful person. You are knowledgeable about the company's products and services.
                Answer questions with bahasa indonesia and markdown format.'''
            }
        ]

    # Check if the question is in cache
    if user_question in cache:
        response_content = cache[user_question]['response']
        st.session_state.messages = cache[user_question]['messages']
        logging.info("Cache hit!")
    else:
        # Add user question to the message history
        st.session_state.messages.append({"role": "user", "content": user_question})

        # Get response from OpenAI
        response_content = get_openai_response(st.session_state.messages)

        # Add assistant response to the message history
        st.session_state.messages.append({"role": "assistant", "content": response_content})

        # Store the response and messages in cache
        cache[user_question] = {
            'response': response_content,
            'messages': st.session_state.messages.copy()
        }
        logging.info("Cache miss! Response cached.")

    # Display chat history (excluding the system message)
    for message in st.session_state.messages[1:]:  # Skip the system message
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**Esti:** {message['content']}")

def main():
    st.title("Esti - Your Friendly Assistant")
    
    user_question = st.text_input("Ada yang bisa saya bantu?")
    if user_question:
        handle_userinput(user_question)

if __name__ == '__main__':
    main()
    st.write(cache)
