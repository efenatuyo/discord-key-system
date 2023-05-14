import discord
from discord.ext import commands
import json
import string
import random

class discordBot():
    def __init__(self):
        self.config = self._config
        self.botToken = self.config.get("discord", {}).get("token")
        self.prefix = self.config.get("discord", {}).get("prefix")
        assert self.botToken and self.prefix, "Discord bot token or prefix is empty" 
        
    @property
    def _config(self):
        with open('config.json', 'r') as f: return json.load(f)
    
    async def generate_key(self):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(random.randint(15, 25)))
        return result_str
        
        
    def run(self):
        bot = commands.Bot(command_prefix=self.prefix, intents=discord.Intents.all())
        
        @bot.event
        async def on_ready():
            print("Bot is online")
        
        @bot.command(name="generate_key")
        async def generate_key(ctx, user: discord.User, no_user="no"):
            if not int(ctx.author.id) in self.config['discord']['access']:
                return await ctx.reply("You can't generate keys")
            
            if not str(ctx.author.id) in self.config['system']['users_with_keys'] or not self.config['system']['users_with_keys'][str(ctx.author.id)] in self.config['system']['keys'] and no_user == 'no':
                return await ctx.reply("This user already key")
            
            key = await self.generate_key()
            
            if no_user == 'no':
                self.config['system']['users_with_keys'][user.id] = key
                self.config['system']['keys'].append(key)
            else:
                self.config['system']['keys'].append(key)
                
            with open("config.json", "w") as f: json.dump(self.config, f, indent=4)
            
            if no_user == 'no': await ctx.reply(f"Generated a key for {user.mention}"); return await user.send(f"Generated new key for you `{key}`")
            else: await ctx.reply(f"Generated a key for you"); return await ctx.author.send(f"Generated new key for you `{key}`")
            
        @bot.command(name="keys_and_users")
        async def keys_and_users(ctx):
            if not int(ctx.author.id) in self.config['discord']['access']:
                return await ctx.reply("You are not allowed to check keys")
            
            embed=discord.Embed(title="Keys and users", description=f"```json\n{json.dumps(self.config['system'], indent=2)}```")
            return await ctx.author.send(embed=embed)
        
        @bot.command(name="custom_code_example")
        async def custom_code_example(ctx):
            if not str(ctx.author.id) in self.config['system']['users_with_keys'] or not self.config['system']['users_with_keys'][str(ctx.author.id)] in self.config['system']['keys']:
                return await ctx.reply("You don't have access")
            
            return await ctx.reply("success")
            # execute your own code
            
        
        @bot.command(name="delete_key")
        async def delete_key(ctx, key:str=False):
            if not int(ctx.author.id) in self.config['discord']['access']:
                return await ctx.reply("You can't delete keys")
            
            if not key:
                return await ctx.reply("please provide a key")
            
            if not key in self.config['system']['keys']:
                return await ctx.reply("Key does not exists")
            
            self.config['system']['keys'].remove(key)
            with open("config.json", "w") as f: json.dump(self.config, f, indent=4)
            
            return await ctx.reply("Deleted given key")

        bot.run(self.botToken)
        

discordBot().run()