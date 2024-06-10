from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate


# This is a call to LLM to summarize characteristic of the user
async def person_summary(person, llm, output_parser):
    summary = llm

    prompt = ChatPromptTemplate.from_messages(

        [
            (
                "system",
                "Just answer with a 3 words summary"
            ),

            MessagesPlaceholder(variable_name="messages"),

        ]
    )

    summary_chain = prompt | summary | output_parser

    summary_llm = ChatMessageHistory()

    summary_llm.add_user_message(
        "JUST say 3 words to describe the following person. DO NOT ADD ANYTHING else, just 3 words:")

    summary_llm.add_user_message(person)

    summary = summary_chain.invoke({"messages": summary_llm.messages})

    return summary


# Summarize results of document search (comes in sizes S/M/L)
# This workds for document! (Retreival Chain + Taivily search can work with this)
def doc_stuff_summary(text, llm, length="S"):
    assert length in ["S", "M", "L"]

    if length == "S":
        prompt_template = """Write a concise summary of the following:
            "{text}"
            CONCISE SUMMARY:"""
    if length == "M":
        prompt_template = """Write a medium length summary of the following:
            "{text}"
            CONCISE SUMMARY:"""
    else:
        prompt_template = """Write a long and detailed summary of the following:
            "{text}"
            CONCISE SUMMARY:"""

    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

    return stuff_chain.run(text)


# implementing search2user
def search2useSHORT(retrived_info, question, llm, output_parser):

    s2u = llm

    doc = str(retrived_info)

    prompt = ChatPromptTemplate.from_messages(

        [
            (
                "system",
                "summarize the following text only to answer ONLY the question " + question + ":"

            ),

            MessagesPlaceholder(variable_name="messages"),

        ]
    )

    model = prompt | s2u | output_parser

    s2u_model = ChatMessageHistory()
    s2u_model.add_user_message(doc)
    s2u_model.add_user_message("do not add ANY additional info other than the answer to the question")

    output = model.invoke({"messages": s2u_model.messages})

    return output


async def plan_trip(person, destination, POI, time, llm, output_parser):

    planner = llm

    prompt = ChatPromptTemplate.from_messages(

        [
            (
                "system",
                f"You are a trip planner. Plan a trip for a person {person} to {destination} activities: {POI} during the period of time: {time}"
            ),

            MessagesPlaceholder(variable_name="messages"),

        ]
    )

    plan_chain = prompt | planner | output_parser

    planner_llm = ChatMessageHistory()

    planner_llm.add_user_message(
        "plan a trip as said:")

    trip = plan_chain.invoke({"messages": planner_llm.messages})

    return trip
