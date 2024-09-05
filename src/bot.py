from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
from discord import app_commands
from dotenv import load_dotenv
import discord, os

intents = discord.Intents.default()
intents.members = True # メンバー管理の権限
intents.message_content = True # メッセージの内容を取得する権限

load_dotenv() # .envファイルを読み込む
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = discord.Object(id = os.getenv("TEST_GUILD_ID"))

class Client(discord.Client):
    def __init__(self, *, intents: discord.Intents):
      super().__init__(intents=intents)
      self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
       self.tree.copy_global_to(guild=GUILD)
       await self.tree.sync(guild=GUILD)
    
client = Client(intents=intents)

@client.tree.command(name='hello', description='Say hello to the world!') 
async def test(interaction: discord.Interaction): 
  await interaction.response.send_message('Hello, World!')

@client.tree.command(name='lhello', description='Say hello to the world!')
async def ltest(interaction: discord.Interaction):
  lhello = discord.embeds.Embed(
    title="Hello world!", description="ここは description です",
    color=0x29bcf2,
  )
  lhello.add_field(name="ここフィールド1です!", value="フィールド1のvalueはここ", inline=False)
  lhello.add_field(name="ここフィールド2です!", value="フィールド2のvalueはここ", inline=False)

  await interaction.response.send_message(embed=lhello)

class SampleView(discord.ui.View):
    def __init__(self, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="OK", style=discord.ButtonStyle.success)
    async def ok(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"{interaction.user.mention} clicked OK!")

    @discord.ui.button(label="NG", style=discord.ButtonStyle.gray)
    async def ng(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"{interaction.user.mention} clicked NG!", ephemeral=True)

@client.tree.command(name='view', description='View test')
async def view_test(interaction: discord.Interaction):
  view = SampleView()
  await interaction.response.send_message(view=view)

scheduler = BackgroundScheduler()
scheduler.start()

@client.tree.command(name='delay-message', description='Delay message test')
async def delay_message(interaction: discord.Interaction, content: str, delay: int):
    await interaction.response.send_message("I received your request!")
    run_time = datetime.now() + timedelta(seconds=delay)
    def send_message():
        client.loop.create_task(interaction.channel.send(content))
    scheduler.add_job(send_message, trigger=DateTrigger(run_date=run_time))

client.run(TOKEN)