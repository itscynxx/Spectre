import discord
from discord.ext import commands
import requests
import os

URL = "https://api.github.com/graphql" # GraphQL API endpoint
GH_ACCESS_TOKEN = os.getenv("GH_ACCESS_TOKEN")

def versionCheck():
    try:
        gh_api_response = requests.get("https://api.github.com/repos/R2Northstar/Northstar/releases/latest")
        if gh_api_response.status_code == 200:
                gh_data = gh_api_response.json()
        else:
            print(f"Error code when retrieving GitHub API: {gh_api_response.status_code}")
    except requests.exceptions.RequestException as err:
        print(f"GitHub API request failed: {err}")
        return None
    
    ns_current_version = gh_data["name"][1:] # This gets the version as the raw version number without the "v". So '1.7.3' vs 'v1.7.3'
    return ns_current_version

def getLatestDiscussion():
    # We need to pass a personal access token to the API in order to bypass the "rate limit". Pass this as an environment var
    headers = {
        "Authorization": f"Bearer {GH_ACCESS_TOKEN}"
    }
    # Query generated from https://docs.github.com/en/graphql/overview/explorer
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
        response = requests.post(URL, json={"query": query}, headers=headers) # Sending the query as json and the access token as the header
        if response.status_code == 200:
            raw_data = response.json()
            
    except requests.exceptions.RequestException as err:
        print(f"GitHub API request failed: {err}")
        return None
    
    # Dumping the important data into a new dict so it's easier to work with later
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

    # not entirely sure how this should be activated, hopefully you can do this 
    # basically just this works if you indent it and add something to actually activate it
    



    # this checks #northstar-git for "New tag created". the string here can be changed to "New release published", whichever works better
    # this worked on my testing server using an embed and printing to console
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 923675443729690695:
            if "New tag created" in message.content.lower():
                # do api request here, if wanting to check for messages in #northstar-git instead of periodically randomly


    # this code is for actually pinging the playtesters, do this after a prerelease is found. 
    # it errors because the if statement above doesnt do anything currently
    # the fact that the channel and role id are so close threw me off for a bit
    async def pingPlaytesters(self, ctx):
        playtesterChannel = self.bot.get_channel(936678773150081055)
        # note that Spectre does not have perms to ping playtesters currently... i think
        playtesterChannel.send("""
<@&1136471893944324177> we need some people to test [note1].\n\n
        
Includes:\n
[note2]
        
If you find any issues, let us know in the thread below [note3]\n\n
                               
**Release notes:** [note4]\n
**Files:** [note5]\n
Or, use FlightCore, enable, release candidates via the settings and select the beta channel in the main menu <:FlightCore:1047303899595427890>
        """)
        playtesterThread = await playtesterChannel.create_thread(name="[note1]", type=discord.ChannelType.public_thread)
        await playtesterThread.send("Please report any issues you find here! [note6]")

    #note1: some kind of way to automatically get version number
    #note2: some kind of way to automatically get changes. my idea for this is something like this:
    # use the api to get the discussion, then most likely it'll all go to one line.
    # from here, we can format it (somehow) to add a new line after every ":" and ")", then idrk for the spaces in between them 
    # apart from using an embed, so I'll have to figure that out later probably
    #note3: Spectre probably can't ping the thread before its created
    #note4: use api to get this
    #note5: either use api to get link and continue on with flightcore, or omit this and rename "Files"
    #note6: this can be reverted to the "." that is used currently if wanted