import streamlit as st


def print_messages():
    #이전 대화 기록을 출력해주는 코드
    if "messages" in st.session_state and len(st.session_state["messages"]) > 0:
        for chat_message in st.session_state["messages"]:
            st.chat_message(chat_message.role).write(chat_message.content)