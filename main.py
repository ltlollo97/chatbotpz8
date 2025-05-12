import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

#load_dotenv(find_dotenv()) for local deployment
load_dotenv()

client = OpenAI(
    api_key = os.getenv("AZUREAOI_API_KEY"),
    base_url = 'https://proxy.lasso.security/v1/azure/',
    default_headers={
        'lasso-x-api-key': os.getenv("LASSO_API_KEY"),
        'lasso-azure-service': os.getenv("AZURE_ENDPOINT"),
    },
    default_query={ 'api-version': '2024-12-01-preview' }
)

deployment = os.getenv("AZUREAOI_DEPLOYMENT_NAME") # aoi deployment name

st.set_page_config(
    page_title="ChatGPT PZ8",
    page_icon=":robot:",
    layout="centered"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("ChatGPT PZ8")
st.subheader("Chat with your own PZ8 AI assistant")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask anything to PZ8!")
if user_prompt:
    # add user prompt to chat and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model = deployment,
        messages = [
            {"role": "system", "content": "You are an helpful assistant."},
            *st.session_state.chat_history
        ]
    )
    
    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)


