import discord
from discord.ext import commands
from discord import app_commands 
import asyncio
import enum
from typing import Optional
from discord.app_commands import Choice
import datetime
from discord.utils import get
import git
import os
import sys
import subprocess
import json
class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"We have logged in as {self.user}.")
        

client = aclient()
tree = app_commands.CommandTree(client)

intents = discord.Intents.all()
##intents.message_content = True
#intents.members = True  # Subscribe to the privileged members intent.
bot = commands.Bot(intents=intents, command_prefix='') 

mute_roles = [940902121044328468, 944252969577218149, 944252644275392642, 944252655147040818]


g = open("mutes.json")
global mutes_id
mutes_id = json.loads(g.read())
print(mutes_id)
g.close()

@client.event
async def on_ready():
   embed=discord.Embed(title="Бот онлайн", description="Бот запущен и может работать.", color=0x1ad1ff)
   await client.get_channel(1080882415666462830).send(embed=embed)

@tree.command(name = 'unmute')
@app_commands.describe(_user='Человек')
async def slash(interaction:discord.Interaction,
                _user: discord.Member):
    if(interaction.user.get_role(721335143364821003)):
        print("ohio")
        await _user.timeout(datetime.timedelta(seconds=0))
        embed=discord.Embed(color=discord.Color.from_rgb(0,205,0))
        embed.set_author(name=f"Участник {_user.name} размучен", icon_url=_user.avatar)
        
        await interaction.response.send_message(embed=embed)
        embed.add_field(name="Размутил", value=f"{interaction.user.mention}", inline=True)
        guild = interaction.guild
        await guild.get_channel(724614253079822418).send(embed=embed)
        embed.set_author(name=f"{_user.name}, вас размутили на сервере {guild.name}", icon_url=_user.avatar)
        await _user.send(embed=embed)

@tree.command(name = 'ага')
@app_commands.describe(_text='текст')
async def slash(interaction:discord.Interaction,
                _text: str):
    if(interaction.user.get_role(721335143364821003)):
        await interaction.channel.send("dfgsd")

@tree.command(name = 'restart')
async def slash(interaction:discord.Interaction):
    if(interaction.user.get_role(891255842924531762)):
        await interaction.response.defer()
        import git 
        from git import Repo

        g = git.cmd.Git(Repo.working_tree_dir)
        g.pull()
        embed=discord.Embed(title="Бот перезапускается", description="Бот обновлён. Он будет работать в скором времени.", color=0x1ad1ff)
        #await interaction.response.send_message(embed=embed)
        
        await asyncio.sleep(0.001)
        await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        os.execl(sys.executable, sys.executable, *sys.argv)
        
        #subprocess.call("start.bat")
        #subprocess.run("start.bat")

@tree.command(name = 'setmutes')
@app_commands.describe(_num='текст')
async def slash(interaction:discord.Interaction,
                _num: int):
    if(interaction.user.get_role(721335143364821003)):
        print(mutes_id)
        mutes_id[str(interaction.user.id)] = _num
        print(mutes_id)
        g = open("mutes.json",'w')
        print(json.dumps(mutes_id, sort_keys=True))
        g.write(json.dumps(mutes_id, sort_keys=True))
        g.close()

@tree.command(name='leaderboard')
async def slash(interaction:discord.Interaction):
    g = open("mutes.json",'r')
    
    sss = json.loads(g.read())
    b = 0
    str = ""
    embed=discord.Embed(title="Лидерборд модераторов")
    sss = dict(sorted(sss.items(), key=lambda item: item[1],reverse=True))
    for line in sss.keys():
        print(int(list(sss)[b]))
        user = await client.fetch_user(int(list(sss)[b]))
        print(user)
        #str += f"{user.mention} "
        embed.add_field(name="", value=f"{user.mention}: {sss[line]}", inline=False)
        b+=1
    await interaction.response.send_message(embed=embed)
    g.close()

@tree.command(name='addrule')
@app_commands.describe(_rule='текст')
@app_commands.describe(_text='текст')
async def slash(interaction:discord.Interaction,
                _rule: str,
                _text: str
                ):
    if(interaction.user.get_role(891255842924531762)):
        s = open("rules.json")
        rules = json.loads(s.read())
        s.close()
        rules[_rule] = _text
        g = open("rules.json",'w')
        #print(json.dumps(mutes_id, sort_keys=True))
        g.write(json.dumps(mutes_id, sort_keys=True))
        g.close()

@tree.command(name = 'rules')
async def slash(interaction:discord.Interaction):
    s = open("rules.json")
    rules = json.loads(s.read())
    s.close()
    await interaction.response.send_message(rules)

@tree.command(name = 'mute')
@app_commands.describe(_user='Человек')
@app_commands.describe(_time='Время')
@app_commands.describe(_reason='Причина')
@app_commands.describe(_role='добавлять роль мут-1,2,3,4')
@app_commands.describe(_inlb='добавлять роль мут-1,2,3,4')
async def slash(interaction:discord.Interaction,
                _user: discord.Member,
                _time: str,
                _reason: str,
                _role: Optional[bool] = True,
                _inlb: Optional[bool] = True
                ):
    if(interaction.user.get_role(721335143364821003)):
        message = f"{_user.mention} получил "
        
        if _inlb:
            mutes_id[str(interaction.user.id)] = mutes_id[str(interaction.user.id)]+1
            g = open("mutes.json",'w')
            print(json.dumps(mutes_id, sort_keys=True))
            g.write(json.dumps(mutes_id, sort_keys=True))
            g.close()

        #время 
        t = False
        g = 0
        for i in _time:
            if(_time[g] in ['1','2','3','4','5','6','7','8','9','0','s','m','h','d']):
                d = 0
            else:
                t = True
                break
            g+=1
        if(t == True):
            await interaction.response.send_message("Время указано неверно",ephemeral=True)
            return
        time = ""
        g = 0
        for i in _time:
            if(_time[g] in ['1','2','3','4','5','6','7','8','9','0']):
                time += _time[g]
                g+=1
            else:
                break
        timetype = _time.replace(time, "")
    
    
        if(timetype == "s"):
            timee = int(time)
        elif(timetype == "m"):
            timee = int(time) * 60
        elif(timetype == "h"):
            timee = int(time) * 60 * 60
        elif(timetype == "d"):
            timee = int(time) * 60 * 60 * 24
        else:
            timee = int(time)
        print(f"{int(time)}, {timetype}")
        print(timee)
        print(timetype == "m")
        role = interaction.guild.get_role(1078342498658816132)
        #await _user.add_roles(role)
        #await _user.timeout(_time)
        await _user.timeout(datetime.timedelta(seconds=timee))
        print(_user.is_timed_out())
        guild = interaction.guild
        s = _time.replace("s", " сек.")
        s = s.replace("m", " мин.")
        s = s.replace("h", " ч.")
        s = s.replace("d", " дн.")
        embed=discord.Embed(description="", color=discord.Color.from_rgb(240,72,72))
        #embed.add_field(name=f"Причина: {_reason}", value=f"{interaction.user.mention}", inline=False)
        embed.set_author(name=f"Участник {_user.name} замучен на {s}", icon_url=_user.avatar)
        embed.add_field(name="Замутил", value=f"{interaction.user.mention}", inline=True)
        embed.add_field(name="Получил", value=f"{_user.mention}", inline=True)

        if(_role):
            if(_user.get_role(mute_roles[3])):
                #message += f"5-й мут (бан)"
                embed.set_footer(text="В ближайшее время получит бан")
            elif(_user.get_role(mute_roles[2])):
                await _user.remove_roles(get(guild.roles, id=mute_roles[2]))
                await _user.add_roles(get(guild.roles, id=mute_roles[3]))
                embed.set_footer(text="Выдана роль мут-4")
            elif(_user.get_role(mute_roles[1])):
                await _user.remove_roles(get(guild.roles, id=mute_roles[1]))
                await _user.add_roles(get(guild.roles, id=mute_roles[2]))
                embed.set_footer(text="Выдана роль мут-3")
            elif(_user.get_role(mute_roles[0])):
                await _user.remove_roles(get(guild.roles, id=mute_roles[0]))
                await _user.add_roles(get(guild.roles, id=mute_roles[1]))
                embed.set_footer(text="Выдана роль мут-2")
            else:
                await _user.add_roles(get(guild.roles, id=mute_roles[0]))
                embed.set_footer(text="Выдана роль мут-1")
        
        message += f" на {s} Причина: {_reason}"
        embed.add_field(name=f"Причина: {_reason}", value=f"", inline=False)
        #await interaction.response.send_message(embed=embed)
        
        if(not _inlb):
            embed.set_footer(text="Не зачислено в лидерборд")
        
        await guild.get_channel(724614253079822418).send(embed=embed)
        await guild.get_channel(846747716348018750).send(embed=embed)
        embed.set_author(name=f"{_user.name}, вас замутили на {s} на сервере {guild.name}", icon_url=_user.avatar)
        await _user.send(embed=embed)

        s = open("rules.json")
        rules = json.loads(s.read())
        s.close()
        b = 0
        for line in rules.keys():
            #print(list(s)[b])
            #user = await client.fetch_user(int(list(s)[b]))
            if((_reason.lower()).__contains__(list(rules)[b])):
                break
            #str += f"{user.mention} "
            #embed.add_field(name="", value=f"{user.mention}: {sss[line]}", inline=False)
            b+=1
        embed=discord.Embed(title="Правило", description=f"{list(rules)[b]} - {rules[line]}", color=0x1ad1ff)
        await _user.send(embed=embed)
        #await asyncio.sleep(int(timee))
        #await _user.remove_roles(role)
    else:   
        await interaction.response.send_message("хаха бесправный", ephemeral=True)
#token = input('token: ')




f = open("token.txt", "r")
client.run(f.read()) #мф
f.close()