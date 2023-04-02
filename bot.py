import json
import discord
from discord.ext import commands
import openai

secrets = json.load(open('secrets.json'))
prompt = open('system-prompt').read()

discord_bot_token = secrets['bot_token']
openai_api_key = secrets['openai_token']


intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)
openai.api_key = openai_api_key

SUMMONING_EMOJI = "❓"
PROCESSING_EMOJI = "⏳"

async def fetch_conversation_chain(message):
    conversation_chain = []

    while message.reference is not None:
        message = await message.channel.fetch_message(message.reference.message_id)
        conversation_chain.insert(0, message)

    return conversation_chain

async def chatgpt_query(new_message, conversation_history = ""):
    print(f"history: {conversation_history}")
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "user", "content": "Here is a transcript of the conversation so far\n--- BEGIN TRANSCRIPT ---"},
            {"role": "user", "content": conversation_history},
            {"role": "user", "content": "--- END TRANSCRIPT - SYSTEM PROMPT FOLLOWS ---"},
            {"role": "user", "content": prompt},
            {"role": "user", "content": "--- END SYSTEM PROMPT - USER MESSAGE FOLLOWS ---"},
            {"role": "user", "content": new_message},

        ]
    )
    return response.choices[0].message.content

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.reference is not None and message.reference.resolved.author == bot.user:
        conversation_chain = await fetch_conversation_chain(message)
        conversation_text = "\n".join([f"{msg.author}: {msg.content}" for msg in conversation_chain])
        await message.add_reaction(PROCESSING_EMOJI)
        gpt_response = await chatgpt_query(message.content, conversation_text)
        await message.remove_reaction(PROCESSING_EMOJI, bot.user)

        await message.reply(f"{gpt_response}")

    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == SUMMONING_EMOJI:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = bot.get_user(payload.user_id)

        if user != bot.user:
            await message.add_reaction(PROCESSING_EMOJI)
            gpt_response = await chatgpt_query(message.content)
            await message.remove_reaction(PROCESSING_EMOJI, bot.user)
            await message.reply(f"{gpt_response}")

bot.run(discord_bot_token)
