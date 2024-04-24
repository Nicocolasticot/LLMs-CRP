from langchain.llms.ollama import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable, RunnableConfig

import chainlit as cl
from chainlit.playground.config import add_llm_provider
from chainlit.playground.providers.langchain import LangchainGenericProvider

# Initialize the LLM model
model = Ollama(model="llama2")

# Register the LLM model in ChainLit
add_llm_provider(
    LangchainGenericProvider(
        id=model._llm_type,
        name="Llama 2",
        llm=model,
        is_chat=False,
    )
)

@cl.on_chat_start
async def on_chat_start():
    # Initialize chat history
    cl.user_session.set("chat_history", [])  # Initialize chat history

@cl.on_message
async def on_message(message: cl.Message):
    # Retrieve chat history from the session
    chat_history = cl.user_session.get("chat_history")
    
    # Append user message to chat history
    chat_history.append(("human", message.content))

    # Generate a prompt from the updated chat history
    prompt_messages = [("system", "You are a trip planner wanting to help me plan my next vacation.")]
    prompt_messages.extend(chat_history)  # Include chat history in the prompt
    prompt = ChatPromptTemplate.from_messages(prompt_messages)

    # Create a runnable that combines the new prompt, model, and output parser
    runnable = prompt | model | StrOutputParser()

    # Process the input message and stream the response
    response_message = cl.Message(content="", author="ViaggerAI")
    for chunk in await cl.make_async(runnable.stream)(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await response_message.stream_token(chunk)

    # Append system response to chat history
    chat_history.append(("system", response_message.content))

    # Update the chat history in the user session
    cl.user_session.set("chat_history", chat_history)

    # Send the response message to the user
    await response_message.send()