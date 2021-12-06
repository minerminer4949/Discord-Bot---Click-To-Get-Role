#!/usr/local/bin/python3
# coding=UTF-8

import discord
import configparser
from discord.ext import commands

config = configparser.ConfigParser()
config.read("bot.config")
DISCORD_API_TOKEN=config.get("DISCORD","API_TOKEN")
DISCORD_CHANNEL_ID=config.get("DISCORD","CHANNEL_ID")

my_intents = discord.Intents.default()
my_intents.members = True
bot = commands.Bot( command_prefix="/", intents=my_intents)

@bot.event
async def on_member_join(member):
  #print(member)
  bHasNotVerifiedRole=False
  bHasHumanRole=False
  bHasNoRole=True
  for user_role in member.roles:
    if user_role.name != "@everyone":
      bHasNoRole=False
      if user_role.name == "Not Verified":
        bHasNotVerifiedRole=True
      if user_role.name == "Human":
        bHasHumanRole=True
  if(bHasNoRole):
    #print("has no role")
    not_verified_role = discord.utils.find(lambda r: r.name == 'Not Verified', member.guild.roles)
    await member.add_roles(not_verified_role)

@bot.event
async def on_raw_reaction_add(payload):
  #print(payload)
  if(payload.channel_id == int(DISCORD_CHANNEL_ID)):
    current_guild=bot.get_guild(payload.guild_id)
    member = await current_guild.fetch_member(payload.user_id)
    #print(member)
    if(payload.emoji.name == '🦍'):
      #print("emoji match")
      add_role = discord.utils.find(lambda r: r.name == 'Not Verified', current_guild.roles)
      delete_role = discord.utils.find(lambda r: r.name == 'Not Verified', current_guild.roles)
      for user_role in member.roles:
        if user_role.name != "@everyone":
          bHasNoRole=False
          if user_role.name == "Not Verified":
            add_role=discord.utils.find(lambda r: r.name == 'Human', current_guild.roles)
            delete_role = discord.utils.find(lambda r: r.name == 'Not Verified', current_guild.roles)
          if user_role.name == "Human":
            delete_role=discord.utils.find(lambda r: r.name == 'Human', current_guild.roles)
            add_role=discord.utils.find(lambda r: r.name == 'Not Verified', current_guild.roles)

      await member.add_roles(add_role)

      delete_role = discord.utils.find(lambda r: r.name == 'Not Verified', current_guild.roles)
      await member.remove_roles(delete_role)

bot.run(DISCORD_API_TOKEN)
