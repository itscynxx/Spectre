import discord
from discord.ext import commands
import re
import requests
import os
import time

url = "https://api.github.com/graphql"
githubAccessToken = os.getenv("githubAccessToken")

def getLatestDiscussion():
    headers = {
        "Authorization": f"Bearer {githubAccessToken}"
    }

    query = """
    query {
        repository(owner: "R2Northstar", name: "Northstar") {
            discussions(first: 1) {
                edges {
                    node {
                        author {
                            login
                            url
                        }
                        title
                        number
                        body
                        url
                    }
                }
            }
        }
    }
    """
    try:
        response = requests.post(url, json={"query": query}, headers=headers)
        if response.status_code == 200:
            raw_data = response.json()
            
    except requests.exceptions.RequestException as err:
        print(f"GitHub API request failed: {err}")
        return None
    
    discussion_post = {
        'author': raw_data["data"]["repository"]["discussions"]["edges"][0]["node"]["author"]["login"],
        'title': raw_data["data"]["repository"]["discussions"]["edges"][0]["node"]["title"],
        'body': raw_data["data"]["repository"]["discussions"]["edges"][0]["node"]["body"],
        'number': raw_data["data"]["repository"]["discussions"]["edges"][0]["node"]["number"],
        'url': raw_data["data"]["repository"]["discussions"]["edges"][0]["node"]["url"]
    }
    
    return discussion_post

class PlayTesterPing(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if not message.embeds:
            return

        if message.channel.id == 923675443729690695:
            if re.search(r'\[R2Northstar/NorthstarLauncher\] New release published: v\d+.\d+.\d+-rc\d+', message.embeds[0].title):
                data = getLatestDiscussion()
                vIndex = message.embeds[0].title.index("v")
                rcVersion = message.embeds[0].title[vIndex:]
                playtestPingChannel = self.bot.get_channel(936678773150081055)

                embed = discord.Embed(
                    title="Changelog:",
                    description=data["body"]
                )

                embed.set_author(name="Northstar " + rcVersion, icon_url="https://avatars.githubusercontent.com/u/86304187")
                
                pingMessage = await playtestPingChannel.send(f"<@&936669179359141908>s, there is a new Northstar release candidate, `{rcVersion}`. If you find any issues, please let us know in the thread attached to this message.\n\n**Installation**:\nGo to settings in FlightCore, and enable testing release channels. After you've done that, go to the play tab, click the arrow next to `LAUNCH GAME`, and select `Northstar release candidate`. Then, click the `UPDATE` button.", embed=embed)
                await pingMessage.create_thread(name=rcVersion)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PlayTesterPing(bot))
