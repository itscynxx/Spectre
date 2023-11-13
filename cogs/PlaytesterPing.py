import discord
from discord.ext import commands
import re
import requests
import os

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

def getLatestReleaseName():
    headers = {
        "Authorization": f"Bearer {githubAccessToken}"
    }

    try:
        response = requests.get("https://api.github.com/repos/R2Northstar/NorthstarLauncher/releases", headers=headers)
            
    except requests.exceptions.RequestException as err:
        print(f"GitHub API request failed: {err}")
        return None
    
    return response.json()[0]["tag_name"]

class PlayTesterPing(commands.Cog):
    def __init__(self, bot :commands.Bot) -> None:
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        playtestPingChannel = self.bot.get_channel(936678773150081055)
        thunderstoreReleaseChannel = self.bot.get_channel(939573786355859498)

        if message.author == self.bot.user:
            return

        if message.channel == thunderstoreReleaseChannel:
            if not message.embeds:
                return
            if re.search(r'NorthstarReleaseCandidate v\d+.\d+.\d+', message.embeds[0].title) and message.embeds[0].author.name == "northstar":
                data = getLatestDiscussion()
                rcVersion = getLatestReleaseName()
                
                embed = discord.Embed(
                    title="Changelog:",
                    description=data["body"]
                )

                embed.set_author(name="Northstar " + rcVersion, icon_url="https://avatars.githubusercontent.com/u/86304187")
                
                pingMessage = await playtestPingChannel.send(f"<@&936669179359141908>s, there is a new Northstar release candidate, `{rcVersion}`. If you find any issues or have feedback, please inform us in the thread attached to this message.\n\n**Installation**:\nGo to settings in FlightCore, and enable testing release channels. (you only need to do this once) After you've done that, go to the play tab, click the arrow next to `LAUNCH GAME`, and select `Northstar release candidate`. Then, click the `UPDATE` button.", embed=embed)
                await pingMessage.create_thread(name=rcVersion)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PlayTesterPing(bot))
