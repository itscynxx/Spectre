import discord
import util.JsonHandler
import os
from discord.ext import commands
import sys

class LogReading(commands.Cog):

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True


    @commands.hybrid_command()
    async def ping(self, ctx, arg):
        await ctx.send("pong")

    
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
                        decoded_string = reading_text.decode('utf-8')
                        split_v2 = str(decoded_string)
                        lines_split = split_v2.splitlines()
                        new_text = ""
                        for i in lines_split:
                            if 'Loading mod' in i:
                                new_text = new_text + i + "\n"
                                print(i)  
                         
                        if "S2.Primrose" in new_text:
                                await message.channel.send(":crimegoat:")
                        else:
                                with open(r'Logs/nslog.txt', 'w') as file_to_write:
                                    file_to_write.write(new_text)
                                    print("wrote to the file")
                                    file_to_write.close()
                                    await message.channel.send("Dingus")
                    except UnicodeDecodeError as E:
                                    filtered_bytes = reading_text.replace(b'\x82', b'')
                                    decoded_string = filtered_bytes.decode('utf-8')
                                    split_v2 = str(decoded_string)
                                    lines_split = split_v2.splitlines()
                                    print(lines_split[0])
                                    new_text = ""
                                    for i in lines_split:
                                        if 'Loading mod' in i:
                                            new_text = new_text + i + "\n"
                                            print(i)  
                         
                                    if "S2.Primrose" in new_text:
                                        await message.channel.send(":crimegoat:")
                                    else:
                                        with open(r'Logs/nslog.txt', 'w') as file_to_write:
                                            file_to_write.write(new_text)
                                            print("wrote to the file")
                                            file_to_write.close()
                                            await message.channel.send("Dingus\nHad to remove an invalid char")

                    else:
                        print("Didn't find nslog in there")

async def setup(bot: commands.Bot) -> None:
        await bot.add_cog(LogReading(bot))
