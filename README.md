Hello! This is a chatbot avaiable with or without online functionalities to plan trips.
The chatbot is Based on LlaMA, accessed through Ollama, and developed using the Langchain Framework and Chainlit as user interface framework. The chatbot relies on a variety of modules developed by us and external solutions such as Taivily and Spacy. 

Here we will briefly go through the functions and the modules used. 

1. Architecture and framework 
2. Collect Info 
3. Trip Functions 
4. Summary Functions 
5. ResOnlineFunctions 
6. Tavily search 
7. Spacy 
8. LangChain 
9. Chainlit
10. Disclaimers


The Architecture and Framework 

Briefly our architecture can be described as follows: 

When a user submits a query, the chatbot begins the process by retrieving relevant information. This retrieval chain leverages general knowledge and historical data to gather necessary information, which is then condensed into a summary. Only for the paid version, the chatbot identifies relevant cities related to the query and retrieves information on current activities available in those cities using Tavily Search API, which connects to the Tavily search engine for up-to-date information from the web. Tavily’s answer is also summarized. The main LLM then takes this information and generates a comprehensive answer for the user. Finally, the chatbot delivers this detailed answer back to the user.

To do this we rely on a variety of modules which will discuss afterwards. 

This first implementation it is based on LLaMA 2 7b, but it can be upgraded to any version of LLaMA supported by Ollama just changing the variable name “model”. 

To develop this model we used Langchain (more info in section 8) and Chainlit (more info in section 9)

Collect info 

Collect info is a module developed by us which collects info from the users using the following functions: 

async def collect_person(): 
async def collect_destination(): 
async def collect_POI(): 
async def collect_time(): 

These functions collect information from the user based on a prompt such as tastes of the user, destination, points of interest and time of the trip. 

For clarity we used different functions, but they all share the same structure and can be all replaced by a function like the following: 

Async def collect_info(prompt_info) 

NOTE: We used the async definition to make these functions work with chainlit despite limited resources. 
More on this here: https://docs.chainlit.io/guides/sync-async

Trip Info

The trip info is a module we developed that uses Spacy (more on Spacy in section 7) to retrieve the following information from a trip: 
 
- Cities 
- Time 
- Activities 
- Months
- Dates 

Summary Functions 

Summary functions is a module that we developed to summarize the following informations: 

- Tastes of the user 
- Documents 
- Web search results 

The module also includes a function to plan the trip (plan_trip)

This module relies heavily on llms which are used either to summarize or create information both from natural prompts and non natural ones (such as web search results or document) 


ResOnlineFunctions 

NB: to use this module you must obtain a tavily api key at: https://tavily.com/#pricing

This module has been developed by us to display information retrieved from the web using Tavily AI (more on that later) 
It includes a variety of functions to: 

- Run a tavily search 
- Convert the tavily output in a output readable to the final user 
- Runs a web search 
- Find (real time) activities 
- Find opening and closing times of activities 

note: there are two versions of the tavily search: WC and WS. WC uses the implementation of langchain of Taivily searches, while WS was developed by us. We found WS to be more effective, but in may be beneficial to have both options. The functions which include a WC prefix therefore differ from their WS counterparts for the kind of search they run. 

Spacy 

SpaCy is an open-source software library for advanced natural language processing, by using it we are able to identify all the entities from a text. In our case we use spacy as the foundation of the trip info module. 
More info on spacy should be found at https://spacy.io/api/doc

As a basic example of the functionality of Spacy we used, it must be understood that we can feed it a sentence like: 
“Amsterdam is a great city. On the 25th April, it became the center of the Northern European association” 
And Spacy will return 

Amsterdam: GPE (Geopolitical Entity) 
25th April: DATE (date) 
Northern European association: ORG (Organization) 


Tavily Search 

Tavily Search is an API designed to provide search results optimized for Large Language Models (LLMs). It facilitates comprehensive data retrieval by scraping, filtering, and aggregating information from multiple sources. 

More informations about tavily search must be found at the following links: 

Tavily Search Documentation


Langchain 

LangChain is a framework designed for developing applications powered by language models. It provides tools and libraries to facilitate tasks such as data preprocessing, model integration, and workflow orchestration. LangChain aims to simplify the development and deployment of language model applications.

More information about LangChain must be found at the following link: 
https://python.langchain.com/v0.1/docs/get_started/introduction

Chainlit 

Chainlit is a framework for building and deploying interactive applications powered by language models. It offers tools for creating user interfaces and managing interactions with language models, making it easier to develop applications that require human-computer interaction.

More information about Chainlit must be found at the following link: 
https://github.com/Chainlit/chainlit

Disclaimers 

note: Depending on the resources or your machine, to use the paid model it may be necessary to ask again to the chat the trip plan if it gets stuck to a blank screen. This is due to a timeout of Langchain as our devices were not able to run the script without Chainlit disconnecting. However, the script works, but this lack of resources causes a stop in the streaming of messages, therefore the message may not be displayed despite having been created.
