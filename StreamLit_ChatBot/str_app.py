import streamlit as st 
from langchain.llms.ollama import Ollama
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = Ollama(model="llama2")
memory = ConversationBufferWindowMemory(memory_key="chat_history")
llm_chain = LLMChain(
    llm=llm,
    memory=memory, 
    prompt=prompt
)


st.set_page_config(
    page_title="ViaggerAI"
)