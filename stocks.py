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
import matplotlib.pyplot as plt

today = date.today()
yesterday = today - timedelta(days=1)

client = commands.Bot(command_prefix = '!')


apikey = 'Enter Your Key'


@client.event
async def on_ready():
	print("I am ready")

@client.command()
async def company(ctx,arg):

    company_overview_url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + arg + '&apikey=' + apikey
    company_overview_url_json = rq.get(company_overview_url)
    company_overview = company_overview_url_json.json()

    embed = discord.Embed(title = company_overview['Name'],description = company_overview['Description'],colour = discord.Colour.blue())
    embed.set_footer(text = yesterday)
    embed.add_field(name = 'Country' , value = company_overview['Country'],inline = False)
    embed.add_field(name = 'Sector' , value = company_overview['Sector'],inline = False)
    embed.add_field(name = 'FiscalYearEnd' , value = company_overview['FiscalYearEnd'],inline = False)
    embed.add_field(name = 'EBITDA' , value = "{:,}".format(int(company_overview['EBITDA'])),inline = False)
    embed.add_field(name = 'PERatio' , value = company_overview['PERatio'],inline = False)
    embed.add_field(name = 'PEGRatio' , value = company_overview['PEGRatio'],inline = False)
    embed.add_field(name = 'BookValue' , value = company_overview['BookValue'],inline = False)
    embed.add_field(name = 'AnalystTargetPrice' , value = company_overview['AnalystTargetPrice'],inline = False)
    embed.add_field(name = 'DividendPerShare' , value = company_overview['DividendPerShare'],inline = False)
    embed.add_field(name = 'EPS' , value = company_overview['EPS'],inline = False)
    embed.add_field(name = '52WeekHigh' , value = company_overview['52WeekHigh'],inline = False)
    embed.add_field(name = '52WeekLow' , value = company_overview['52WeekLow'],inline = False)
    embed.add_field(name = 'ReturnOnEquityTTM' , value = company_overview['ReturnOnEquityTTM'],inline = False)
    embed.add_field(name = 'ReturnOnAssetsTTM' , value = company_overview['ReturnOnAssetsTTM'],inline = False)



    await ctx.send(embed = embed)

@client.command()
async def daily_stock(ctx,arg):

	daily_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+ arg + '&apikey=' + apikey
	daily_url_json = rq.get(daily_url)
	daily = daily_url_json.json()

	company_overview_url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + arg + '&apikey=' + apikey
	company_overview_url_json = rq.get(company_overview_url)
	company_overview = company_overview_url_json.json()

	embed = discord.Embed(title = 'Company Name : '+ company_overview['Name'] + '\n' + '\n' + 'Company Code : ' + arg + '\n' + '\n' + 'Date(yyyy/mm/dd) : ' + str(yesterday),description = '' ,colour = discord.Colour.blue())
	embed.set_footer(text = 'Daily series updates every 24hrs')
	embed.add_field(name = '1. Open' , value = daily['Time Series (Daily)'][str(yesterday)]['1. open'],inline = False)
	embed.add_field(name = '2. High' , value = daily['Time Series (Daily)'][str(yesterday)]['2. high'],inline = False)
	embed.add_field(name = '3. Low' , value = daily['Time Series (Daily)'][str(yesterday)]['3. low'],inline = False)
	embed.add_field(name = '4. Close' , value = daily['Time Series (Daily)'][str(yesterday)]['4. close'],inline = False)
	embed.add_field(name = '5. Adjusted Close' , value = daily['Time Series (Daily)'][str(yesterday)]['5. adjusted close'],inline = False)
	embed.add_field(name = '6. Volume' , value = daily['Time Series (Daily)'][str(yesterday)]['6. volume'],inline = False)
	embed.add_field(name = '7. Dividend Amount' , value = daily['Time Series (Daily)'][str(yesterday)]['7. dividend amount'],inline = False)
	embed.add_field(name = '8. Split Coefficient' , value = daily['Time Series (Daily)'][str(yesterday)]['8. split coefficient'],inline = False)

	await ctx.send(embed = embed)



@client.command()
async def intraday(ctx,args):


		arg = re.split('-',args)
		open = []

		intraday_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+ arg[0] +'&interval='+ arg[1] +'&apikey=' + apikey
		intraday_url_json = rq.get(intraday_url)
		intraday = intraday_url_json.json()

		company_overview_url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + arg[0] + '&apikey=' + apikey
		company_overview_url_json = rq.get(company_overview_url)
		company_overview = company_overview_url_json.json()

		embed = discord.Embed(title = 'Intraday : '+ company_overview['Name'] + '\n' + '\n' + 'Company Code : ' + arg[0] + '\n' + '\n' + 'Date(yyyy/mm/dd) : ' + str(yesterday),description = '' ,colour = discord.Colour.blue())



		for i in intraday['Time Series (' + arg[1] + ')'].values():
			open.append(float(i['1. open']))


		plt.xticks(open,"")

		plt.plot(open)
		plt.savefig('image.png', dpi=600, format='png')
		plt.clf()

		await ctx.send(embed = embed)
		await ctx.send(file=discord.File('image.png'))


@client.command()
async def helpme(ctx):

	embed = discord.Embed(title = '!HELPME' + '\n' +'\n' + 'Help Has Arrived!!' + '\n' + '\n' + 'Command Examples :' , description = '',colour = discord.Colour.green())

	embed.add_field(name = 'Company Overview' , value = 'Example : !company IBM',inline = False)
	embed.add_field(name = 'Daily Stock Info' , value = 'Example : !daily_stock IBM',inline = False)
	embed.add_field(name = 'Intraday Day Info with Timestamp' , value = 'Example : !intraday IBM-60min',inline = False)
	embed.add_field(name = 'Further Information : ' ,value = 'lordhades4762@gmail.com')
	embed.set_image(url = 'https://contenthub-static.grammarly.com/blog/wp-content/uploads/2018/05/how-to-ask-for-help-760x400.jpg')
	embed.set_footer(text= 'We are always here to support you!')


	await ctx.send(embed = embed)



client.run('Your Bot Token')
