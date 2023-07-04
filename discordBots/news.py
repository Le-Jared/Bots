import discord
from discord.ext import commands
import requests
import json

bot = commands.Bot(command_prefix='!')

# Replace 'your-api-key' with your NewsAPI key
API_KEY = 'your-api-key'

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='news')
async def news(ctx):
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    for article in articles[:5]: # send top 5 news
        title = article['title']
        description = article['description']
        url = article['url']
        embed = discord.Embed(title=title, description=description, url=url)
        await ctx.send(embed=embed)

# Replace 'your-token-here' with your Bot's token
bot.run('your-token-here')
