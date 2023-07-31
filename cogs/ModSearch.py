from discord.ext import commands
import requests, re
import discord


class ModSearch(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot
        
    @commands.hybrid_command(description="Search Northstar Thunderstore for mods")
    async def searchts(self, ctx, search_string: str):
        try:
            response = requests.get("https://northstar.thunderstore.io/api/v1/package/")
            if response.status_code == 200:
                data = response.json()
        
        except requests.exceptions.RequestException as err:
            print(err)
            return
           
        match_count = 0
        for mod in data:
            match = re.search(search_string, mod["name"], re.IGNORECASE)
            if match and match_count < 3:
                mod_desc = f"By {mod['owner']}\n{mod['versions'][0]['description']}\n{mod['versions'][0]['download_url']}"
                embed = discord.Embed(
                    title=mod["name"],
                    description=mod_desc
                )
                embed.set_thumbnail(url=mod['versions'][0]['icon'])
                await ctx.send(embed=embed)
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ModSearch(bot))
