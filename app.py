import os

import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import datetime
import time
import random

from langchain import OpenAI
from streamlit_option_menu import option_menu
from conversations import conversations

st.set_page_config(layout="wide", page_title='数翼 Streamlit Chat 示例')

default_title = '新的对话'


# 输出一条聊天消息
def chat(user, message):
    with st.chat_message(user):
        print(user, ':', message)
        st.markdown(message)


if 'conversations' not in st.session_state:
    st.session_state.conversations = conversations
conversations = st.session_state.conversations

#  当前选择的对话
if 'index' not in st.session_state:
    st.session_state.index = 0

AVAILABLE_MODELS = [
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "text-davinci-003",
    "code-davinci-002",
]

with st.sidebar:
    st.image('assets/hero.png')
    st.subheader('', divider='rainbow')
    st.write('')
    llm = st.selectbox('选择您的模型', AVAILABLE_MODELS, index=4)

    if st.button('新的对话'):
        conversations.append({'title': default_title, 'messages': []})
        st.session_state.index = len(conversations) - 1

    titles = []
    for idx, conversation in enumerate(conversations):
        titles.append(conversation['title'])

    option = option_menu(
        'Conversations',
        titles,
        default_index=st.session_state.index
    )

# get api key from env
openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(model_name=llm)

st.session_state.messages = conversations[st.session_state.index]['messages']

prompt = st.chat_input("请输入你的问题")
if prompt:
    if conversations[st.session_state.index]['title'] == default_title:
        conversations[st.session_state.index]['title'] = prompt[:12]
    for user, message in st.session_state.messages:
        chat(user, message)
    chat('user', prompt)
    answer = openai.predict(prompt)
    st.session_state.messages.append(('user', prompt))
    st.session_state.messages.append(('assistant', answer))
    chat('assistant', answer)
else:
    for user, message in st.session_state.messages:
        chat(user, message)
