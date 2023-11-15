from PIL import Image
import pytesseract
from discord.ext import commands
import re
import util.JsonHandler
import os
import discord

imageReadEmbed = discord.Embed(
    title="Automatic Image Reading:", description="", color=0x5D3FD3
)


class imageStuff(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
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
                image = Image.open("image.png")
                text = pytesseract.image_to_string(image)

                if re.search("windows.protected.your.pc", text.lower()):
                    imageReadEmbed.add_field(
                        name="",
                        value="Mod managers sometimes get auto flagged by Windows Defender because they don't have a digital signature, which Windows automatically (falsely) assumes is dangerous. These files, however, are not dangerous. They're all open source (so you can see all the code that make them up) if you want to confirm for yourself.\n\nYou can simply press `More Info` and `Run Anyway` to use the application. Please only do this when I respond if you're getting this message specifically for a Northstar mod manager, and nothing else.",
                    )

                if re.search("items.nut", text.lower()) and re.search(
                    "INVALID_REF", text.lower()
                ):
                    imageReadEmbed.add_field(
                        name="",
                        value="If you're encountering the \"INVALID_REF\" issue, please double check if you've removed any mods that do things like add skins to the game. A big cause of this is removing MoreSkins while a skin is equipped on a gun, making the game try to load something that doesn't exist. If you aren't sure or this didn't work, you'll have to reset multiplayer data, which should fix the issue. You can do this by opening the console on the main menu by hitting `~`, typing `ns_resetpersistence` , and then hitting enter.",
                    )

                if re.search(
                    "Encountered.CLIENT.script.compilation.error", text.lower()
                ) and re.search("error|help", message.content.lower()):
                    imageReadEmbed.add_field(
                        name="",
                        value="From this image alone, we can't see what's causing the issue. Please send a screenshot of the console (open it by hitting the `~` key), or send the newest log. You can find logs in `Titanfall2/R2Northstar/logs`, with the newest being on the bottom by default.",
                    )

                if re.search(
                    "Invalid.or.expired.masterserver.token", text.lower()
                ) or re.search("Couldn't.find.player.account", text.lower()):
                    imageReadEmbed.add_field(
                        name="",
                        value='Try following the guide on solving the "Couldn\'t find player account" and "Invalid master server token" errors [here](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/troubleshooting#playeraccount)',
                    )

                if re.search("MSVCP120.dll", text.lower()):
                    imageReadEmbed.add_field(
                        name="",
                        value='The "MSVCP120.dll" error comes up when you\'re missing a dependency Titanfall 2 uses to run. Follow the [wiki section for this issue](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/troubleshooting#msvcr) to solve it.',
                    )

                # FlightCore specific errors
                if re.search("Mod.failed.sanity.check", text.lower()):
                    imageReadEmbed.add_field(
                        name="",
                        value="The \"Mod failed sanity check\" error is specific to FlightCore, and means that the mod isn't properly formatted and FlightCore can't automatically install it. However, you can still follow the [manual mod install guide](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/manual-installation#installing-northstar-mods-manually) to install the mod you wanted.",
                    )

                # Viper specific errors
                if re.search("Unknown.error*an.unknown.error.occurred", text.lower()):
                    imageReadEmbed.add_field(
                        name="",
                        value="If you're using Viper, please click on the error message shown in this image and send a screenshot of the actual error message that pops up afterwards.",
                    )

                if re.search("operation.not.permitted", text.lower()) and re.search(
                    "EA.Games", text.lower()
                ):
                    imageReadEmbed.add_field(
                        name="",
                        value="EA's default install directory has some issues associated with it, which can be solved by following the [wiki section about this error](https://r2northstar.gitbook.io/r2northstar-wiki/installing-northstar/troubleshooting#cannot-write-log-file-when-using-northstar-on-ea-app)",
                    )

                if len(imageReadEmbed.fields) > 0:
                    if len(imageReadEmbed) > 1:
                        return
                    else:
                        imageReadEmbed.add_field(
                            name="",
                            value="\nPlease note that I'm a bot automatically reading your image. There is a chance this information is wrong, in which case please ping @Cyn",
                        )
                        await message.channel.send(
                            embed=imageReadEmbed, reference=message
                        )
                        imageReadEmbed.clear_fields()

                os.remove("image.png")
                # is this bad? probably
                # does it work? also probably


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(imageStuff(bot))
