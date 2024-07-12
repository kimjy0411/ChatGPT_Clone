import streamlit as st
from utils import print_messages, StreamHandler
from langchain_core.messages import ChatMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from dotenv import load_dotenv



st.set_page_config(page_title="ChatGPT", page_icon=" ")
st.title("ChatGPT")

#api key 설정
#os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
load_dotenv()


if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 채팅 대화기록을 저장하는 store 세션 상태 변수
if "store" not in st.session_state:
    st.session_state["store"] = dict()

with st.sidebar:
    session_id = st.text_input("Session ID")
    clear_btn = st.button("대화기록 초기화")
    if clear_btn:
        st.session_state["messages"] = []
        st.experimental_rerun()


print_messages()


# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_ids: str) -> BaseChatMessageHistory:
    if session_ids not in st.session_state["store"] :  # 세션 ID가 store에 없는 경우
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        st.session_state["store"][session_ids] = ChatMessageHistory()
    return st.session_state["store"] [session_ids]  # 해당 세션 ID에 대한 세션 기록 반환




if user_input := st.chat_input("Say something"):
    #사용자가 입력한 내용
    st.chat_message("user").write(f"{user_input}")
    st.session_state["messages"].append(ChatMessage(role="user" , content=user_input))
    
    #LLM을 사용하여 AI의 답변을 생성

   
    

    #AI의 답변
    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())

         #1. 모델생성성
        llm = ChatOpenAI(streaming = True, callbacks=[stream_handler])
    
        #2. 프롬포드 생성
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "질문에 짧고 간결하게 답변해 주세요",
                ),
                # 대화 기록을 변수로 사용, history 가 MessageHistory 의 key 가 됨
                MessagesPlaceholder(variable_name="history"),
                ("human", "{question}"),  # 사용자 질문을 입력
            ]
        )
        chain = prompt | llm # 프롬프트와 모델을 연결하여 runnable 객체 생성
    

        chain_with_memory = (
        RunnableWithMessageHistory(  # RunnableWithMessageHistory 객체 생성
            chain,  # 실행할 Runnable 객체
            get_session_history,  # 세션 기록을 가져오는 함수
            input_messages_key="question",  # 사용자 질문의 키
            history_messages_key="history",  # 기록 메시지의 키
            )
        )

        response = chain_with_memory.invoke(
        # 수학 관련 질문 "코사인의 의미는 무엇인가요?"를 입력으로 전달합니다.
            { "question": user_input},
        #  세션 ID 설정
            config={"configurable": {"session_id": session_id}},
            )
       
        st.session_state["messages"].append(
            ChatMessage(role="assistant" , content=response.content)
        )