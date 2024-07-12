import streamlit as st
from utils import print_messages
from langchain_core.messages import ChatMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from dotenv import load_dotenv



st.set_page_config(page_title="ChatGPT", page_icon=" ")
st.title("ChatGPT")

#api key 설정
#os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
load_dotenv()


if "messages" not in st.session_state:
    st.session_state["messages"] = []



print_messages()

if user_input := st.chat_input("Say something"):
    #사용자가 입력한 내용
    st.chat_message("user").write(f"{user_input}")
    st.session_state["messages"].append(ChatMessage(role="user" , content=user_input))
    
    #LLM을 사용하여 AI의 답변을 생성
    prompt = ChatPromptTemplate.from_template(
        """질문에 대하여 간결하게 답변해 주세요
        {question}"""
    )

    chain = prompt | ChatOpenAI()
    response = chain.invoke({"question": user_input})
    msg = response.content

    #AI의 답변
    with st.chat_message("assistant"):
        
        st.write(msg)
        st.session_state["messages"].append(ChatMessage(role="assistant" , content=msg))