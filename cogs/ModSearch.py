from discord.ext import commands
import requests, re
import discord, asyncio
from time import sleep

active_search = False

class ModSearch(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot 
        
    @commands.hybrid_command(description="Search Northstar Thunderstore for mods")
    async def searchts(self, ctx, search_string: str):
        
        global active_search
        
        if len(search_string) < 3:
            await ctx.send("Search must be at least 3 characters")
            return
        
        if active_search:
            await ctx.send("Please wait for the active search to timeout")
            return
        
        try:
            response = requests.get("https://northstar.thunderstore.io/api/v1/package/")
            if response.status_code == 200:
                data = response.json()
        
        except requests.exceptions.RequestException as err:
            print(err)
            return
        
        mods = {}
        for i, item in enumerate(data):
            match = re.search(search_string, item["name"], re.IGNORECASE)
            if match:
                downloads = 0
                for version in item['versions']:
                    downloads = downloads + version['downloads']
                mods["result_" + str(i)] = {
                    "name": item['name'].replace("_", " "),
                    "owner": item['owner'],
                    "icon_url": item['versions'][0]['icon'],
                    "dl_url": item['versions'][0]['download_url'],
                    "last_update": item['date_updated'][:(item['date_updated'].index('T'))], # Remove time from date string
                    "total_dl": downloads,
                    "description": item['versions'][0]['description']
                }
                
        if not mods:
            await ctx.send("No mods found")
            return
        
        # Sort mods by most downloaded by default until we get better sorting later        
        sorted_mods_by_dl = dict(sorted(mods.items(), key=lambda item: item[1]['total_dl'], reverse=True))
        
        pages = list(sorted_mods_by_dl.keys())
        current_page = 0
        
        def get_mod_embed():
            key = pages[current_page]
            mod = sorted_mods_by_dl[key]
            mod_embed_desc = f"By {mod['owner']}\n{mod['description']}\nLast Updated: {mod['last_update']}\nDownloads: {mod['total_dl']}\n{mod['dl_url']}"
            embed_title = f"{mod['name']} ({current_page + 1}/{len(pages)})"
            embed = discord.Embed(
                title=embed_title,
                description=mod_embed_desc
            )
            embed.set_thumbnail(url=mod['icon_url'])
            return embed
        
        message = await ctx.send(embed=get_mod_embed())
        
        active_search = True
        
        reactions = ['⏮️', '◀️', '▶️', '⏭️']
        for reaction in reactions:
            await message.add_reaction(reaction)
            sleep(0.050) # Sleep for 100ms to hopefully avoid reactions getting placed out-of-order
            
        def check_react(reaction, user):
            return user == ctx.author and str(reaction.emoji) in reactions
        
        while True:
            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=30.0, check=check_react)
                
                if str(reaction.emoji) == '⏮️':
                    current_page = 0
                elif str(reaction.emoji) == '◀️':
                    current_page = (current_page - 1) % len(pages)
                elif str(reaction.emoji) == '▶️':
                    current_page = (current_page + 1) % len(pages)
                elif str(reaction.emoji) == '⏭️':
                    current_page = len(pages) - 1
                
                await message.edit(embed=get_mod_embed())
                await message.remove_reaction(reaction, ctx.author)
                
            except asyncio.TimeoutError:
                break
            
        await message.clear_reactions()
        active_search = False
        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ModSearch(bot))
