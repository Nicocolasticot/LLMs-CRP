# Langchain imports
from langchain.llms.ollama import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableConfig

# Chainlit Imports
import chainlit as cl
from chainlit.playground.config import add_llm_provider
from chainlit.playground.providers.langchain import LangchainGenericProvider

# Custom Function Imports
from SummaryFunctions import person_summary, plan_trip
from TripFunctions import trip_activities
from CollectInfo import collect_person, collect_destination, collect_POI, collect_time
import spacy
import ResOnlineFunctions as tv
import TripFunctions as tp
from TripFunctions import countries


def log_progress(message):
    print(f"[INFO] {message}")


instructions = "answer the question of the users as a useful travel planner"

# Initialize the LLM model
log_progress("Initializing LLM model...")
model = Ollama(model="llama2")

output_parser = StrOutputParser()


# Register the LLM model in ChainLit
log_progress("Registering LLM model in ChainLit...")
add_llm_provider(
    LangchainGenericProvider(
        id=model._llm_type,
        name="Llama 2",
        llm=model,
        is_chat=False,
    )
)
# Loading Spacy 

log_progress("Loading spaCy model...")
nlp = spacy.load('en_core_web_lg')


@cl.on_chat_start
async def collect_info():
    
    log_progress("Collecting person information...")
    person = await collect_person()
    log_progress("Collecting destination information...")
    destination = await collect_destination()
    log_progress("Collecting POI information...")
    POI = await collect_POI()
    log_progress("Collecting time information...")
    tme = await collect_time()

    sum_pers = await person_summary(person, model, output_parser)

    # plan a trip with the collected info
    log_progress("Generating a trip..")
    trip = await plan_trip(sum_pers, destination, POI, tme, model, output_parser)

    log_progress("Retrieving the activities...")
    activities = await trip_activities(trip, nlp)

    # adding opening times to the memory
    log_progress("Retrieving opening times...")
    opening_times = await tv.RS_WS_opening_times(activities, 1, model, output_parser)

    # adding real time activities to the memory
    cities = await tp.trip_cities(trip, countries, nlp)
    log_progress("Retrieving real time activities...")
    rt_activities = await tv.RS_WS_find_activities(cities, sum_pers, tme, model, 1, output_parser)

    # add info, trip, activity, opening times and real time activities to the memory
    cl.user_session.set("chat_history", [person, destination, POI, tme, trip] + activities + opening_times + rt_activities)

    await cl.Message(content=trip).send()

    log_progress("Finish collect info...")


@cl.on_message
async def on_message(message: cl.Message):
    log_progress("New message received. Processing...")
    # Retrieve chat history from the session
    chat_history = cl.user_session.get("chat_history")

    # Append user message to chat history
    chat_history.append(("human", message.content))

    # Generate a prompt from the updated chat history
    prompt_messages = [("system", instructions)]
    prompt_messages.extend(chat_history)  # Include chat history in the prompt
    prompt = ChatPromptTemplate.from_messages(prompt_messages)

    # Create a runnable that combines the new prompt, model, and output parser
    runnable = prompt | model | StrOutputParser()

    # Process the input message and stream the response
    response_message = cl.Message(content="")
    for chunk in await cl.make_async(runnable.stream)(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await response_message.stream_token(chunk)

    # Append system response to chat history
    chat_history.append(("system", response_message.content))

log_progress("Script execution completed.")
