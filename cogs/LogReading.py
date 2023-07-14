import discord
import os
from discord.ext import commands
import sys
import json



def decodetext(text, text_to_filter, text_to_filter2):
    filtered_bytes = text.replace(b'\x82', b'')
    decoded_string = filtered_bytes.decode('utf-8')
    split_v2 = str(decoded_string)
    lines_split = split_v2.splitlines()
    new_text = ""
    for i in lines_split:
        if text_to_filter in i or text_to_filter2 in i:
            new_text = new_text + i + "\n"
    return new_text


class LogReading(commands.Cog):

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True

    @commands.hybrid_command()
    async def setupconfig(self, ctx):
         if os.path.exists("cogs/JsonConfig/config.json") == False:
              #create config.json
                config = {
                    "modname": [],
                    "solution": [],
                }
                with open("cogs/JsonConfig/config.json", "w") as f:
                    json.dump(config, f, indent=4)
                    f.close()
                    print("Created config.json")
         else:
            print("config.json already exists")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            if message.attachments:
                filename = message.attachments[0].filename
                print(filename)
                if 'nslog' in filename and filename.endswith('.txt'):
                    print("found nslog in the file")
                    reading_text = await message.attachments[0].read()
                    try:
                        cooltext = decodetext(reading_text, "Loading mod", "Loaded mod")
                        with open("cogs/JsonConfig/config.json", "r") as f:
                            config = json.load(f)
                            f.close()
                        problems = discord.Embed(title="Mods that are breaking your game", description="", color=0x5D3FD3)
                        for i in config["modname"]:
                            if i in cooltext:
                                problems.add_field(name="Remove " + i, 
                                                    value=config["solution"][config["modname"].index(i)], inline=False)
                        if problems.fields.__len__() == 0:
                                with open(r'Logs/nslog.txt', 'w', encoding="utf-8") as file_to_write:
                                    file_to_write.write(cooltext)
                                    print("wrote to the file")
                                    file_to_write.close()
                        else:
                            problems.add_field(name="\u200b", value="If you still encounter issues after doing these, please send another log")
                            await message.channel.send(embed=problems, reference=message)
                    
             
                    except UnicodeDecodeError as E:
                        await message.channel.send("An error happened" + "\n" + E)
                    else:
                        print("Didn't find nslog in there")






async def setup(bot: commands.Bot) -> None:
        await bot.add_cog(LogReading(bot))

