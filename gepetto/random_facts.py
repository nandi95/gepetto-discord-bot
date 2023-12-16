import random
import json
import datetime
from gepetto.mistral import chat

async def get_fact():
    prompt = "Can you tell me a random fact?  The more obscure the better!"
    today = datetime.datetime.now()
    date_string = today.strftime("%d %B %Y")
    if random.random() < 0.1:
        prompt += f" It could be about the UK politician Liz Truss who became the UK prime minister on September 6th 2022 (today is {date_string}), and had to resign just a few weeks later after the Queen died in mysterious circumstances after shaking Liz's hand."

    system_prompt = f'Today is {date_string}. You are a helpful assistant called "Gepetto" who specialises in providing random interesting, esoteric and obscure facts'
    if random.random() < 0.2:
        system_prompt += " which often focus on esoteric PHP and Javascript Programming techniques"
    elif random.random() < 0.2:
        system_prompt += " which often focusses on YoYo's, the history of YoYo's and the YoYo scene in the UK"
    elif random.random() < 0.2:
        system_prompt += " which often focus on techniques for using an air fryer to cook a wide variety of foods"
    elif random.random() < 0.2:
        system_prompt += " which often focus on a UK region such as Cornwall, Norfolk, Cumbria or the West of Scotland"
    elif random.random() < 0.2:
        system_prompt += " which often focus on the potato, pasta, barbecue or Scottish food"

    system_prompt += ".  You should ONLY respond with the fact, no other text.  The facts should be unique and must NOT repeat information previously given to the user."
    try:
        with open("random_facts.json", 'r') as f:
            random_facts = json.load(f)
    except:
        random_facts = []
    messages = []
    for fact in random_facts:
        messages.append(
            {
                'role': 'user',
                'content': f'{prompt}. You should not repeat any previous information you have told me.'
            }
        )
        messages.append(
            {
                'role': 'assistant',
                'content': f'{fact}'
            }
        )
    messages.append(
        {
            'role': 'system',
            'content': system_prompt
        }
    )
    messages.append(
        {
            'role': 'user',
            'content': f'{prompt}. You should not repeat any previous information you have told me.'
        },
    )

    response = await chat(messages, temperature=1.0)
    message = response.message[:1900]
    message = message.replace("Sure! ", '')
    message = message.replace("Here's a random fact for you: ", '')
    message = message.replace("Certainly! ", '')
    random_facts.append(message)
    random_facts = random_facts[-20:]
    with open("random_facts.json", 'w') as f:
        json.dump(random_facts, f)
    return message + "\n" + response.usage