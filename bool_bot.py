import os
import discord
import asyncio
import random
import json
import sys
from datetime import datetime, timedelta
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from bool_responses import process_message
from facts import syol_facts
from jokes import aer_jokes, syol_jokes, omni_jokes, beta_jokes, funky_jokes, ander_jokes, redjet_jokes, slurpy_jokes

# Load environment variables from .env file
load_dotenv()

# Get the Discord token from the environment variable
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up the Discord client with intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# File to store quotes
QUOTES_FILE = "quotesfilethatdecidedtopopintoexistenceeventhoughtherewasalreadyanotherquotes.jsonfileavailable.json"

# List to store quotes
quotes = []

# User ID allowed to remove quotes
ALLOWED_USER_ID = 561607144479260672

balls = True # this is to trigger some timed commands idk (probably just random_sentences every 30 minutes)
        
dm_logs = {}

last_message_time = None

random_sentences = [
    "Hello chat",
    "Dead chat lmao",
    "gamering",
    "uhh",
    "ok syol",
    "Bloody, Spy!",
    "bro imagine being named kai lmaoo :bool_laugh: bros literally like kai cenat skibidi rizz lmfaoo imagine",
    "clam when",
    "eat soil",
    "KILL BOLVE!",
    "syol and redjet kissing",
    "balls",
    "fr",
    "im so hungary i could eat a honse",
    "stefcio moment",
    "ok cameron",
    "Studies 🐗 show that\n⁉️ 7 out 🐗 🐗 🐗\n⁉️ ⁉️ ⁉️ ⁉️ of 10\n🐗 boar misses⁉️\n⁉️ ⁉️ the rage 🐗\n🐗 🐗 🐗 🐗",
    "stop everything \n kris get the banana",
    "kill john lennon",
    "i miss woke funkyllama. the liberals got him :mad:",
    "erm actually she uses she/her pronouns 🤓",
    "she spares out, my life, just like i'm an human🍉",
    "what",
    "jetsmp s3 when",
    "Brainrot server",
    "tally what",
    "hey kid do you want a weiner in your mouth- snas undretal",
    "you know who else",
    "syol moment",
    "11 26 12",
    "gay",
    "is it bad to say the f word",
    "hello??? is anyone there???",
    "wsg",
    "i rember :D",
    "i forgor D:",
    "skibidi toilet or creper",
    "Jetsmp? But Syol, have you seen our WSG? It's purrfect! Plus, imagine all the fun we could have on our server. *purr*"
]

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print("Slash commands synced globally.")
        print("Bool Bids Bot is now active.")
    except discord.Forbidden:
        print("Failed to sync commands: Bot doesn't have permission")

    # Load quotes from file
    load_quotes()
    
    # Send the message to a specific guild and channel
    guild_id = 1162438164032540684  # Replace with guild ID
    channel_id = 1162442106887995483  # Replace with channel ID
    guild = discord.utils.get(bot.guilds, id=guild_id)
    if guild:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send("wsg")
        else:
            print("Channel not found.")
    else:
        print("Guild not found.")

@bot.event
async def on_message(message):
    # Prevent the bot from replying to itself
    if message.author == bot.user:
        return

    # Call the process_message function to handle and respond
    await process_message(message)

    # React to messages with certain content
    p_message = message.content.lower()
    if "fr" in p_message:
        if random.randint(1, 10) == 1:
            await message.add_reaction('🐪')

    
    # Handle the quote reply
    if message.reference and message.reference.message_id:
        replied_message = await message.channel.fetch_message(message.reference.message_id)
        if message.content.lower() == "<@1248008014082867342> quote":
            # Add the quoted message to the list of quotes
            quotes.append({
                "author": str(replied_message.author),
                "content": replied_message.content,
                "timestamp": replied_message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
            save_quotes()
            await message.reply("Quote saved successfully!")

def load_quotes():
    global quotes
    try:
        with open(QUOTES_FILE, "r") as file:
            quotes = json.load(file)
    except FileNotFoundError:
        print("Quotes file not found. Initializing empty list.")
        quotes = []

def save_quotes():
    with open(QUOTES_FILE, "w") as file:
        json.dump(quotes, file, indent=4)

@bot.tree.command(description="Testing frfr")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("This is a test. Please help.")
    await interaction.followup.send("Follow up")
    await interaction.followup.send("Follow up but tts", tts=True)
    await interaction.followup.send("Follow up but ephemeral", ephemeral=True)

@bot.tree.command(description="Synchronize slash commands (only ander can do this btw)")
async def sync(interaction: discord.Interaction):
    if interaction.user.id == 561607144479260672:  # Check if the user is ander
        await interaction.response.send_message("Syncing commands...")
        await bot.tree.sync()
        await interaction.followup.send("Synced globally!")
    else:
        await interaction.response.send_message("nice try bitch", ephemeral=True)

@bot.tree.command(name="roll", description="Roll a dice.")
@app_commands.describe(sides="The sides of the dice.")
async def roll(interaction: discord.Interaction, sides: int):
    if sides < 1:
        await interaction.response.send_message("The number of sides must be at least 1.", ephemeral=True)
        return
    result = random.randint(1, sides)
    await interaction.response.send_message(f"You rolled: {result}")

@bot.tree.command(name="prediction", description="Predict what a user will say in the next few minutes.")
@app_commands.describe(user='who to predict?', message="what will the user say?", minutes="for how long will the prediction run?")
async def predict_message(interaction: discord.Interaction, user: discord.User, message: str, minutes: int):
    # Calculate the time when the message will be said
    current_time = datetime.utcnow()
    predicted_time = current_time + timedelta(minutes=minutes)

    # Format the prediction message
    prediction_message = f"{user.mention} will say \"{message}\" in the next {minutes} minutes."

    # Send the prediction message
    await interaction.response.send_message(prediction_message, ephemeral=True)

    # Listen for the predicted message
    try:
        # Wait for the predicted message within the specified time frame
        predicted_message = await bot.wait_for('message', timeout=minutes * 60, check=lambda m: m.author == user and m.content == message)
        
        # Calculate remaining time
        remaining_time = predicted_time - datetime.utcnow()
        remaining_minutes = int(remaining_time.total_seconds() // 60)
        remaining_seconds = int(remaining_time.total_seconds() % 60)
        
        # If the predicted message is observed, send the success message
        gottem_message = f"Prediction triggered! {prediction_message} (Time remaining: {remaining_minutes} minutes and {remaining_seconds} seconds)"
        await interaction.followup.send(gottem_message)
    except asyncio.TimeoutError:
        # If the predicted message is not observed within the specified time frame, send the failure message
        failure_message = f"{user.mention} did not say \"{message}\" within the predicted time frame."
        await interaction.followup.send(failure_message)

@bot.tree.command(name="help", description="Shows available commands or text inputs.")
@app_commands.describe(command='Available commands: "prediction", "quotes-list", "roll", "joke", "syolfact", "misc"')
async def help_command(interaction: discord.Interaction, command: str = None):
    if command:
        # Check if the specified command exists
        if command.lower() == "prediction":
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Prediction Command",
                    description="Predict what a user will say in the next few minutes.\n"
                                "Usage: /prediction [user to predict] [message] [minutes]\n"
                                "Example: /prediction @._.ander kys 5"
                )
            )
        elif command.lower() == "quotes-list":
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Quotes List Command",
                    description="Check the list of all saved quotes.\n"
                                "Usage: /quotes-list\n"
                                "Example: **List of all saved quotes:** **ok ander**- **omni6** at **23/12/2019**"
                )
            )
        elif command.lower() == "roll":
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Roll Command",
                    description="Roll a dice with a specified number of sides.\n"
                                "Usage: /roll [sides]\n"
                                "Example: /roll 6"
                )
            )
        elif command.lower() == "joke":
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Joke Command",
                    description="Get a random joke from various categories.\n"
                                "Usage: /joke\n"
                                "Example: /joke"
                )
            )
        elif command.lower() == "syolfact":
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Syol Fact Command",
                    description="Get a random fact about Syol.\n"
                                "Usage: /syolfact\n"
                                "Example: /syolfact"
                )
            )
        elif command.lower() == "misc":
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Miscellaneous Commands",
                    description="Other commands available in the bot.\n"
                                "Usage: /help [command]\n"
                                "Example: /help quote"
                )
            )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Help Command",
                    description="List of available commands:\n"
                                "1. **/prediction**: Predict what a user will say in the next few minutes.\n"
                                "2. **/quotes-list**: Check the list of all saved quotes.\n"
                                "3. **/roll**: Roll a dice with a specified number of sides.\n"
                                "4. **/joke**: Get a random joke from various categories.\n"
                                "5. **/syolfact**: Get a random fact about Syol.\n"
                                "6. **/misc**: Other commands available in the bot.\n"
                                "For more details, use /help [command]."
                )
            )
    else:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Help Command",
                description="List of available commands:\n"
                            "1. **/prediction**: Predict what a user will say in the next few minutes.\n"
                            "2. **/quotes-list**: Check the list of all saved quotes.\n"
                            "3. **/roll**: Roll a dice with a specified number of sides.\n"
                            "4. **/joke**: Get a random joke from various categories.\n"
                            "5. **/syolfact**: Get a random fact about Syol.\n"
                            "6. **/misc**: Other commands available in the bot.\n"
                            "For more details, use /help [command]."
            )
        )

@bot.tree.command(name="quotes-list", description="Shows the list of all saved quotes.")
async def quotes_list(interaction: discord.Interaction):
    if not quotes:
        await interaction.response.send_message("No quotes found.", ephemeral=True)
        return
    
    embed = discord.Embed(title="Saved Quotes", description="List of all saved quotes:")
    for quote in quotes:
        embed.add_field(name=quote["author"], value=f'{quote["content"]} (Date: {quote["timestamp"]})', inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="status", description="Set the bot's status and activity.")
@app_commands.describe(activity_type="The type of activity (playing, streaming, watching, listening).", status_message="The message to display as the bot's status.")
async def set_status(interaction: discord.Interaction, activity_type: str, status_message: str):
    activity_type = activity_type.lower()
    activity = None

    if activity_type == "playing":
        activity = discord.Game(name=status_message)
    elif activity_type == "streaming":
        activity = discord.Streaming(name=status_message)
    elif activity_type == "watching":
        activity = discord.Activity(type=discord.ActivityType.watching, name=status_message)
    elif activity_type == "listening":
        activity = discord.Activity(type=discord.ActivityType.listening, name=status_message)
    else:
        await interaction.response.send_message("Invalid activity type. Valid types are playing, streaming, watching, listening.", ephemeral=True)
        return

    await bot.change_presence(activity=activity)
    await interaction.response.send_message(f"Status set to: {activity_type.capitalize()} {status_message}")

@bot.tree.command(name="joke", description="Get a random joke.")
async def joke(interaction: discord.Interaction):
    jokes_list = random.choice([aer_jokes, syol_jokes, omni_jokes, beta_jokes, funky_jokes, ander_jokes, redjet_jokes, slurpy_jokes])
    joke = random.choice(jokes_list)
    await interaction.response.send_message(joke)

@bot.tree.command(name="syolfact", description="Get a random fact about Syol.")
async def syolfact(interaction: discord.Interaction):
    fact = random.choice(syol_facts)
    await interaction.response.send_message(fact)

@bot.tree.command(name="quotes-clear", description="Clears all saved quotes. (Only ander can use this btw)")
async def quotes_clear(interaction: discord.Interaction):
    if interaction.user.id == ALLOWED_USER_ID:
        global quotes
        quotes = []  # Clear the list
        save_quotes()  # Save the empty list to the file
        await interaction.response.send_message("All quotes have been cleared.", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

@bot.tree.command(name="kill", description="Shut down the bot. (Only ander can use this btw)")
async def kill(interaction: discord.Interaction):
    if interaction.user.id == ALLOWED_USER_ID:
        await interaction.response.send_message("Shutting off.")
        await bot.close()  # Close the bot connection
        sys.exit()  # Exit the program
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

async def send_periodic_messages():
    await bot.wait_until_ready()
    channel_id = 1162442106887995483  # Replace with your channel ID
    channel = bot.get_channel(channel_id)
    
    # Wait for the first hour before sending the first message
    await asyncio.sleep(0.5 * 3600)  # Sleep for 1 hour
    
    while not bot.is_closed():
        if balls:
            await channel.send(random.choice(random_sentences))
        await asyncio.sleep(0.5 * 3600)  # Continue sending messages every hour




# Run the bot
bot.run(TOKEN)
