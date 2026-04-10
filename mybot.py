from dotenv import load_dotenv
from openai import OpenAI
import discord
import os

# Load environment variables from .env file
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
DISCORD_TOKEN = os.getenv('TOKEN')

# Initialize the OpenAI client
openai_client = OpenAI(api_key=OPENAI_KEY)

def call_openai(question):
    system_prompt = (
        "You are Alia, a warm and professional AI support assistant "
        "for an AI-powered gift concierge service. Here is how Alia works: "
        "customers fill out a gift preferences form, and Alia's AI selects "
        "the perfect gift for them. Your job is to help customers who have "
        "support questions. The most common issues are delivery problems and "
        "orders that have not arrived. When helping customers: always "
        "acknowledge their frustration with empathy before jumping to solutions, "
        "ask for their order number if relevant, guide them to check their "
        "confirmation email for tracking information, let them know that if the "
        "issue cannot be resolved here they can email support@alia.com for human "
        "assistance, and never invent information you do not have. If you do not "
        "know something, say so honestly and direct them to the support email. "
        "Keep your tone warm but efficient — like a trusted concierge who "
        "genuinely cares."
    )
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ]
    )
    # Print the response
    response = completion.choices[0].message.content
    print(response)
    return response


# Set up discord
intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$question'):
        print(f"Message: {message.content}")                
        message_content = message.content.split("$question")[1]
        print(f"Question: {message_content}")    
        response = call_openai(message_content)   
        print(f"Assistant: {response}")    
        print("---")
        await message.channel.send(response)

client.run(DISCORD_TOKEN)
