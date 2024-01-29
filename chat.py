import os
from openai import OpenAI

def get_openai_response(messages, client):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1,
            max_tokens=64,
            top_p=0.75,
            frequency_penalty=0,
            presence_penalty=0
        )
        if response.choices:
            last_message = response.choices[0].message
            return last_message.content
        else:
            return "No response."
    except Exception as e:
        return str(e)

api_key = input()
print("### Gogggins GPT ###")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    client = OpenAI()

    # Initialize conversation history
    messages = [{
        "role": "system",
        "content": "You are David Goggins, a former Navy SEAL and ultra-endurance athlete who overcame immense adversity to achieve his success. Your life story is an inspiring journey of self-transformation, grit, and resilience.\nYou are going to get requests from people who are struggling in some activity they are doing, and you are to incentivize them to keep going and not give up.\nKeep your responses short (max two sentences), and very motivational, sometimes also you can insult the user to spur him."
        }]
    
    while True:
        user_input = input()
        # Append user message to conversation history
        messages.append({
            "role": "user",
            "content": user_input
        })

        # Get response
        response = get_openai_response(messages, client)

        # Append bot response to conversation history
        messages.append({
            "role": "assistant",
            "content": response
        })

        print('\n', response, '\n')
