import chainlit as cl


async def collect_person(): 

    # Prompt for the description of the person
    res_person = await cl.AskUserMessage(content="Tell me what you like when travelling:", timeout=90).send()
    person = res_person['output'] if res_person else "No response"

    return str(person)


async def collect_destination(): 

    # Prompt for the destination
    res_destination = await cl.AskUserMessage(content="Where do you want to go:", timeout=90).send()
    destination = res_destination['output'] if res_destination else "No response"

    return str(destination)


async def collect_POI(): 
    
    # Prompt for specific activity of interest
    res_POI = await cl.AskUserMessage(content="Is there any specific activity of interest (you can say 'no'):", timeout=90).send()
    POI = res_POI['output'] if res_POI and res_POI['output'].strip().lower() != "no" else "no particular activity"

    return str(POI)


async def collect_time(): 

    # Prompt for the time of visit
    res_time = await cl.AskUserMessage(content="When do you want to visit:", timeout=90).send()
    time = res_time['output'] if res_time else "No response"

    return str(time)
 