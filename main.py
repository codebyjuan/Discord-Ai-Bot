import discord
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Constants
MAX_DISCORD_MESSAGE_LENGTH = 2000
MEMORY_FILE = "memory.json"  # File to store user memory
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)


# Load memory from file
def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return empty memory if file doesn't exist


# Save memory to file
def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


# Read existing memory
memory = load_memory()


def split_message(message, max_length=MAX_DISCORD_MESSAGE_LENGTH):
    """Split a message into chunks that fit within Discord's message length limit."""
    chunks = []
    current_chunk = ""
    lines = message.split('\n')

    for line in lines:
        if len(line) > max_length:
            words = line.split(' ')
            for word in words:
                if len(current_chunk) + len(word) + 1 > max_length:
                    chunks.append(current_chunk.strip())
                    current_chunk = word + ' '
                else:
                    current_chunk += word + ' '
        elif len(current_chunk) + len(line) + 1 > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = line + '\n'
        else:
            current_chunk += line + '\n'

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


@bot.event
async def on_ready():
    print(f'✅ Bot is online as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore its own messages

    user_id = str(message.author.id)  # Convert ID to string for JSON storage

    if message.content.startswith("!chat") or bot.user in message.mentions:
        prompt = message.content.replace("!chat", "").strip()
        if not prompt:
            await message.channel.send(
                "❓ Please ask something! Example: `!chat How does AI work?`")
            return

        # Retrieve user memory
        user_memory = memory.get(user_id, [])

        # Keep only the last 20 interactions (to limit file size)
        if len(user_memory) > 20:
            user_memory = user_memory[-20:]

        # Add the new user prompt
        user_memory.append(f"You: {prompt}")

        # Combine user memory with the new prompt
        full_prompt = "\n".join(user_memory) + "\nAI:"

        try:
            # Google Gemini API call with memory
            response = model.generate_content(full_prompt)
            reply = response.text

            # Add AI response to memory
            user_memory.append(f"AI: {reply}")
            memory[user_id] = user_memory  # Update the memory dictionary
            save_memory(memory)  # Save memory to file

            # Split the response into chunks if it's too long
            chunks = split_message(reply)

            # Send each chunk as a separate message
            for chunk in chunks:
                await message.channel.send(chunk)

        except Exception as e:
            await message.channel.send(
                "⚠️ Error communicating with Google Gemini API.")
            print(e)


bot.run(DISCORD_TOKEN)
