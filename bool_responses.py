import re
import random

def handle_response(message: str, author_name: str):
    try:
        p_message = message.lower()

        if p_message == "hello":
            if author_name == "syol_lareth":
                return "hi syol!!!! wly"
            if author_name == ".betafish.":
                return "stay mad beta"
            if author_name == "azo9_x":
                return "hi aZo thanks for helping with the bot, also hello slurpy"
            elif author_name == "omni6":
                return "shut up femboy"
            elif author_name == "glytching":
                return "gamering"
            elif author_name == "plasmawavemicrowave":
                return "hi plasma"
            elif author_name == "funkyllama":
                return "funkyllama? more like fuckyllama <:bool_laugh:1162699223981109358>"
            elif author_name == "._.ander":
                return "die"
            elif author_name == "noiamnotstealing":
                return "bro shut up youre like nine years old"
            elif author_name == "redjet99":
                return "HOLY SHIT ITS REDJET99"
            elif author_name == "naifkopi":
                return "https://cdn.discordapp.com/attachments/1209506360987877408/1230405211764297738/Good_Morning.gif?ex=66620066&is=6660aee6&hm=99c1252299e9816724eba83db3198e03f30807d24f24bf9cca2de5d3c1de0794&"
            else:
                return "wassup"

        if p_message == "ballin" or p_message == "balling":
            if p_message == "!jesus_ballin":
                return ""
            else:
                return (
                    "ballin? more like"
                    "https://tenor.com/view/repost-ballin-balling-repost-if-ballin-repost-if-balling-gif-27035246"
                )
            
        if p_message == "stfu" or p_message == "shut up":
            return (
                f"Listen here {author_name}, Dad will not tolerate you saying the words that consist of the letters 's h u t  u p' being said in this server, so take your own advice and close thine mouth in the name of Dad and the Christian Minecraft server owner."
            )

        match = re.search(r"\b(i['`]?m|im)\b\s*(.+)", p_message, re.IGNORECASE)
        if match:
            rest_of_message = match.group(2).strip()
            if rest_of_message.lower() != "dad!":
                return f"Hi {rest_of_message}, I'm bool!"

        if "ok ander" in p_message:
            return "ander? i hardly know her!"

        if "kys" in p_message:
            return "No, YOU kys!!!! *thunder*"
        
        if "Shut up, it's not my fault sub elitism(which is highly ableist against people with slow reading abilities like me) dominates anime fandom, so some companies don't even dub their anime" in p_message:
            return "syol its literally pride month you cant say that wtf"


        def is_shouting(message):
            words = message.split()
            if len(words) < 2:
                return False

            uppercase_count = sum(1 for char in message if char.isalpha() and char.isupper())
            total_letters = sum(1 for char in message if char.isalpha())
            percentage = uppercase_count / total_letters if total_letters > 0 else 0
            return percentage > 0.5

        if is_shouting(message):
            return "Keep your voice down!"

        return ""
        
    except Exception as exception:
        print(f"Error in handle_response: {exception}")
        return ""

# Example function to use this in your existing Discord bot setup
async def process_message(message):
    # Ensure message content and author name are passed
    response = handle_response(message.content, str(message.author))
    
    # Send response if not empty
    if response:
        await message.channel.send(response)
