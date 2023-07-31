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
        
        mods = {}
        for i, item in enumerate(data):
            match = re.search(search_string, mod["name"], re.IGNORECASE)
            if match:
                downloads = 0
                for version in item['versions']:
                    downloads = downloads + version['downloads']
                mods["result_" + str(i)] = {
                    "name": item['name'],
                    "owner": item['owner'],
                    "icon_url": item['versions'][0]['icon'],
                    "dl_url": item['versions'][0]['download_url'],
                    "last_update": item['date_updated'],
                    "total_dl": downloads,
                    "description": item['versions'][0]['description']
                }
        
        # Sort mods by most downloaded by default until we get better sorting later        
        sorted_mods_by_dl = dict(sorted(mods.items(), key=lambda item: item[1]['total_dl'], reverse=True))
        
        # WARNING: In it's current state, Spectre will spam the channel with complete search results
        for key in sorted_mods_by_dl:
            mod = sorted_mods_by_dl[key]
            mod_embed_desc = f"By {mod['owner']}\n{mod['description']}\nLast Updated: {mod['last_update']}\nDownloads: {mod['total_dl']}\n{mod['dl_url']}"
            embed = discord.Embed(
                title=mod["name"],
                description=mod_embed_desc
            )
            embed.set_thumbnail(url=mod['icon_url'])
            await ctx.send(embed=embed)
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ModSearch(bot))
