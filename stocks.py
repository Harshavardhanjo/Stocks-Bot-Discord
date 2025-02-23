import requests as rq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import re
import json
from datetime import date
from datetime import timedelta
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

today = date.today()
yesterday = today - timedelta(days=1)

# Initialize bot with intents
client = commands.Bot(command_prefix='!', intents=intents)

# Get API key from environment variable
apikey = os.getenv('ALPHA_VANTAGE_API_KEY')

@client.event
async def on_ready():
    print("I am ready")

@client.command()
async def company(ctx, arg):
    try:
        company_overview_url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + arg + '&apikey=' + apikey
        company_overview_url_json = rq.get(company_overview_url)
        company_overview = company_overview_url_json.json()

        # Check if we got valid data
        if "Error Message" in company_overview:
            await ctx.send(f"Error: Could not find company with symbol {arg}")
            return
            
        if "Note" in company_overview:
            await ctx.send("API call limit reached. Please try again later.")
            return

        embed = discord.Embed(title=company_overview['Name'], description=company_overview['Description'], colour=discord.Colour.blue())
        embed.set_footer(text=yesterday)
        embed.add_field(name='Country', value=company_overview['Country'], inline=False)
        embed.add_field(name='Sector', value=company_overview['Sector'], inline=False)
        embed.add_field(name='FiscalYearEnd', value=company_overview['FiscalYearEnd'], inline=False)
        embed.add_field(name='EBITDA', value="{:,}".format(int(company_overview['EBITDA'])), inline=False)
        embed.add_field(name='PERatio', value=company_overview['PERatio'], inline=False)
        embed.add_field(name='PEGRatio', value=company_overview['PEGRatio'], inline=False)
        embed.add_field(name='BookValue', value=company_overview['BookValue'], inline=False)
        embed.add_field(name='AnalystTargetPrice', value=company_overview['AnalystTargetPrice'], inline=False)
        embed.add_field(name='DividendPerShare', value=company_overview['DividendPerShare'], inline=False)
        embed.add_field(name='EPS', value=company_overview['EPS'], inline=False)
        embed.add_field(name='52WeekHigh', value=company_overview['52WeekHigh'], inline=False)
        embed.add_field(name='52WeekLow', value=company_overview['52WeekLow'], inline=False)
        embed.add_field(name='ReturnOnEquityTTM', value=company_overview['ReturnOnEquityTTM'], inline=False)
        embed.add_field(name='ReturnOnAssetsTTM', value=company_overview['ReturnOnAssetsTTM'], inline=False)

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@client.command()
async def daily_stock(ctx, arg):
    try:
        daily_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + arg + '&apikey=' + apikey
        daily_url_json = rq.get(daily_url)
        daily = daily_url_json.json()

        # Check for API errors
        if "Error Message" in daily:
            await ctx.send(f"Error: Could not find stock data for symbol {arg}")
            return
            
        if "Note" in daily:
            await ctx.send("API call limit reached. Please try again later.")
            return

        company_overview_url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + arg + '&apikey=' + apikey
        company_overview_url_json = rq.get(company_overview_url)
        company_overview = company_overview_url_json.json()

        embed = discord.Embed(title='Company Name: ' + company_overview['Name'] + '\n\n' + 'Company Code: ' + arg + '\n\n' + 'Date(yyyy/mm/dd): ' + str(yesterday), description='', colour=discord.Colour.blue())
        embed.set_footer(text='Daily series updates every 24hrs')
        embed.add_field(name='1. Open', value=daily['Time Series (Daily)'][str(yesterday)]['1. open'], inline=False)
        embed.add_field(name='2. High', value=daily['Time Series (Daily)'][str(yesterday)]['2. high'], inline=False)
        embed.add_field(name='3. Low', value=daily['Time Series (Daily)'][str(yesterday)]['3. low'], inline=False)
        embed.add_field(name='4. Close', value=daily['Time Series (Daily)'][str(yesterday)]['4. close'], inline=False)
        embed.add_field(name='5. Adjusted Close', value=daily['Time Series (Daily)'][str(yesterday)]['5. adjusted close'], inline=False)
        embed.add_field(name='6. Volume', value=daily['Time Series (Daily)'][str(yesterday)]['6. volume'], inline=False)
        embed.add_field(name='7. Dividend Amount', value=daily['Time Series (Daily)'][str(yesterday)]['7. dividend amount'], inline=False)
        embed.add_field(name='8. Split Coefficient', value=daily['Time Series (Daily)'][str(yesterday)]['8. split coefficient'], inline=False)

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@client.command()
async def intraday(ctx, args):
    try:
        arg = re.split('-', args)
        if len(arg) != 2 or arg[1] not in ['1min', '5min', '15min', '30min', '60min']:
            await ctx.send("Invalid format. Use: !intraday SYMBOL-INTERVAL (e.g., IBM-60min)")
            return

        open_prices = []

        intraday_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + arg[0] + '&interval=' + arg[1] + '&apikey=' + apikey
        intraday_url_json = rq.get(intraday_url)
        intraday = intraday_url_json.json()

        # Check for API errors
        if "Error Message" in intraday:
            await ctx.send(f"Error: Could not find intraday data for symbol {arg[0]}")
            return
            
        if "Note" in intraday:
            await ctx.send("API call limit reached. Please try again later.")
            return

        company_overview_url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + arg[0] + '&apikey=' + apikey
        company_overview_url_json = rq.get(company_overview_url)
        company_overview = company_overview_url_json.json()

        embed = discord.Embed(title='Intraday: ' + company_overview['Name'] + '\n\n' + 'Company Code: ' + arg[0] + '\n\n' + 'Date(yyyy/mm/dd): ' + str(yesterday), description='', colour=discord.Colour.blue())

        for i in intraday['Time Series (' + arg[1] + ')'].values():
            open_prices.append(float(i['1. open']))

        plt.figure(figsize=(10, 6))
        plt.plot(open_prices, color='blue')
        plt.title(f"{arg[0]} Intraday Prices ({arg[1]} intervals)")
        plt.ylabel('Price')
        plt.grid(True)
        plt.xticks([])
        plt.tight_layout()
        plt.savefig('image.png', dpi=600, format='png')
        plt.close()

        await ctx.send(embed=embed)
        await ctx.send(file=discord.File('image.png'))
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@client.command()
async def helpme(ctx):
    try:
        embed = discord.Embed(
            title='Stock Market Bot Help',
            description='Available commands and their usage:',
            colour=discord.Colour.green()
        )

        embed.add_field(
            name='Company Overview',
            value='`!company SYMBOL`\nExample: `!company IBM`\nShows detailed company information',
            inline=False
        )
        
        embed.add_field(
            name='Daily Stock Info',
            value='`!daily_stock SYMBOL`\nExample: `!daily_stock AAPL`\nShows today\'s stock performance',
            inline=False
        )
        
        embed.add_field(
            name='Intraday Trading Info',
            value='`!intraday SYMBOL-INTERVAL`\nExample: `!intraday MSFT-60min`\n' +
                  'Available intervals: 1min, 5min, 15min, 30min, 60min\n' +
                  'Shows intraday trading chart',
            inline=False
        )

        embed.set_footer(text='Data provided by Alpha Vantage API')

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Run the bot using the token from environment variable
client.run(os.getenv('DISCORD_TOKEN'))