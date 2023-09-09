from PIL import Image
import pytesseract
from discord.ext import commands
import re
import util.JsonHandler
import os

class imageStuff(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot 

    @commands.Cog.listener()
    async def on_message(self, message):

        channels = util.JsonHandler.load_channels()
        users = util.JsonHandler.load_users()

        if str(message.author.id) in users:
            return
        
        if str(message.channel.id) in channels:
            if message.attachments:

                await message.attachments[0].save("image.png")
                image = Image.open('image.png')
                text = pytesseract.image_to_string(image)

                if re.search("windows.protected.your.pc", text.lower()):
                    await message.channel.send("Mod managers sometimes get auto flagged by Windows Defender because they don't have a digital signature, which Windows automatically (falsely) assumes is dangerous. These files, however, are not dangerous. They're all open source (so you can see all the code that make them up) if you want to confirm for yourself.\n\nYou can simply press `More Info` and `Run Anyway` to use the application. Please only do this when I respond if you're getting this message specifically for a Northstar mod manager, and nothing else.", reference=message)

                if re.search("items.nut", text.lower()) and re.search("INVALID_REF", text.lower()):
                    await message.channel.send("If you're encountering the \"INVALID_REF\" issue, please double check if you've removed any mods that do things like add skins to the game. A big cause of this is removing MoreSkins while a skin is equipped on a gun, making the game try to load something that doesn't exist. If you aren't sure or this didn't work, you'll have to reset multiplayer data, which should fix the issue. You can do this by opening the console on the main menu by hitting `~`, typing `ns_resetpersistence` , and then hitting enter.", reference=message)

                if re.search("Encountered.CLIENT.script.compilation.error", text.lower()) and re.search("error|help", message.content.lower()):
                    await message.channel.send("From this image alone, we can't see what's causing the issue. Please send a screenshot of the console (open it by hitting the `~` key), or send the newest log. You can find logs in `Titanfall2/R2Northstar/logs`, with the newest being on the bottom by default.", reference=message)

                os.remove("image.png")
                # is this bad? probably
                # does it work? also probably

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(imageStuff(bot))
