from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_core.runnables import RunnablePassthrough
from SummaryFunctions import search2useSHORT

api_key = ""  # INSERT API KEY


# Runs a search on Taivily (query), picking the top k results
def ResTavilySearch(query, k):
    try:
        retriever = TavilySearchAPIRetriever(api_key=api_key, k=k)
        result = retriever.invoke(query)
        return result
    except Exception as e:
        return f"info from the web couldn't been retrieved due to error: {str(e)}"


# This function gives a readable output from taivily using search2use
def ResWebSearch(query, k, llm, output_parser):
    try:
        result = search2useSHORT(ResTavilySearch(query, k=k), query, llm, output_parser)
        return result
    except Exception as e:
        return f"info from the web couldn't been retrieved due to error: {str(e)}"


# Same as before but using chain summary (langchain)
def ResWebSearchChain(query, k, llm):
    try:
        prompt = ChatPromptTemplate.from_template(
            """Answer the question based only on the context provided.
        
            Context: {context}
        
            Question: {question}"""
        )

        retriever = TavilySearchAPIRetriever(api_key=api_key, k=k)

        chain = (
                RunnablePassthrough.assign(context=(lambda x: x["question"]) | retriever)
                | prompt
                | llm
                | StrOutputParser()
        )
        return chain.invoke({"question": query})
    except Exception as e:
        return f"info from the web couldn't been retrieved due to error: {str(e)}"


# Finds num_activities (number) activities to suit the taste of the person (person)
# given the list of cities
# This uses WebSearch
async def RS_WS_find_activities(cities, tastes, time, llm, num_activities, output_parser):
    try:
        activities = []
        # print(tastes)

        for city in cities:
            query = "activities for someone " + tastes + " in " + str(time) + " in " + str(city)
            # print ("SEARCH for: ", query)
            summary_activities = ResWebSearch(query, num_activities, llm, output_parser)
            activities.append(city + ": " + summary_activities)

        return activities
    except Exception as e:
        return f"info from the web couldn't been retrieved due to error: {str(e)}"


# Same as before but uses webchain instead of websearch
def RS_WC_find_activities(cities, tastes, time, llm, num_activities, output_parser):
    try:
        activities = []
        # print(tastes)

        for city in cities:
            query = "activities for someone " + tastes + " in " + str(time) + " in " + str(city)
            # print ("SEARCH for: ", query)
            summary_activities = ResWebSearchChain(query, num_activities, llm)
            activities.append(city + ": " + summary_activities)

        return activities
    except Exception as e:
        return f"info from the web couldn't been retrieved due to error: {str(e)}"


# retrieving opening times given a list of activities based on k results from the web
# This uses WebSearch
async def RS_WS_opening_times(activities, k, llm, output_parser):
    try:
        opening_times = []
        question = "opening time "

        for activity in activities:
            query = question + activity
            opening_times.append(ResWebSearch(query, k, llm, output_parser))

        return opening_times
    except Exception as e:
        return f"info from the web couldn't been retrieved due to error: {str(e)}"


# This is the same but uses WebChain
# retrieving opening times
def RS_WC_opening_times(activities, k, llm):
    try:
        opening_times = []
        question = "opening time "

        for activity in activities:
            query = question + activity
            opening_times.append(ResWebSearchChain(query, k, llm))

        return opening_times
    except Exception as e:
        return f"info from the web couldn't been retrieved due to error: {str(e)}"
