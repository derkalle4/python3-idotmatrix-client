import json
import os

# OpenAI imports
import openai
from openai import OpenAI


with open("assistant/tools.json") as f:
    tools = json.load(f)

# Initialize OpenAI client with API key
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

SYSTEM_PROMPT = "You are an expert assistant who can control a 32x32 pixel screen. The user asks you to perform a task and you have to choose the correct action to take."

def gpt_call(model = "gpt-4o-mini", messages = []):
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": messages[-1]}]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        # response_format=response_format,
        temperature = 0,
        tools = tools

    )
    return response