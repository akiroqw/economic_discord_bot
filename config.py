from ast import alias
from dis import disco
from glob import glob
from pydoc import cli, describe
import sqlite3
import string
import discord
from discord.ext import commands
from pandas import describe_option
import datetime
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from discord.ui import Button,View
from operator import inv
from random import randint
from numpy import append
from easy_pil import*
from PIL import*
from discord import File

setting = {
    'TOKEN' : 'OTg1MjI2Mjg3ODE3ODIyMjk5.Gi8JD2.WXzAl2e698pTVNfeBSm9DeW-wuSbdwx7jVd0CI',
    'NAME BOT' : 'Падлаツ',
    'ID'       : '985226287817822299',
    'PREFIX'   : '!'
}
collecting_roles = {"Administrator" : 250000,
                    "Moderator" : 12323,
                    "G. Administrator": 123
}
text_work = {1: 'None',
             2: 'None2',
             3: 'None3'}
             
client = commands.Bot(command_prefix = setting['PREFIX'], intents = discord.Intents.all())
client.remove_command('help')
connection = sqlite3.connect('server.db')
cursor = connection.cursor()
time_conection = datetime.today()
