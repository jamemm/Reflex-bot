import discord
from discord.ext import commands

from reflexserver import server_on




intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 🔥 ใส่ ID ห้อง "ยืนยันสำเร็จ"
VERIFY_CHANNEL_ID = 1480615666062200965


class VerifyModal(discord.ui.Modal, title="📋 ยืนยันตัวตน"):

    game_name = discord.ui.TextInput(label="ชื่อในเกม")
    uid = discord.ui.TextInput(label="UID (ตัวเลข)")
    nickname = discord.ui.TextInput(label="ชื่อเล่น")
    age = discord.ui.TextInput(label="อายุ (ตัวเลข)")

    async def on_submit(self, interaction: discord.Interaction):

        member = interaction.user

        # ===== เช็คเลข =====
        if not self.uid.value.isdigit():
            return await interaction.response.send_message("❌ UID ต้องเป็นตัวเลข", ephemeral=True)

        if not self.age.value.isdigit():
            return await interaction.response.send_message("❌ อายุ ต้องเป็นตัวเลข", ephemeral=True)

        # ===== Embed =====
        embed = discord.Embed(
            title="✅ ยืนยันตัวตนสำเร็จ",
            color=discord.Color.green()
        )
        embed.add_field(name="Discord", value=f"{member.mention}\n({member})", inline=False)
        
            
        embed.add_field(name="ชื่อในเกม", value=self.game_name.value, inline=False)
        embed.add_field(name="UID", value=self.uid.value, inline=False)
        embed.add_field(name="ชื่อเล่น", value=self.nickname.value, inline=False)
        embed.add_field(name="อายุ", value=self.age.value, inline=False)
        

        embed.set_footer(text=f"ยืนยันโดย {member}")

        # 🔥 สำคัญ: ใช้ fetch_channel (ชัวร์กว่า get_channel)
        channel = await bot.fetch_channel(1480615666062200965)

        await channel.send(embed=embed)

        await interaction.response.send_message(
            "✅ ยืนยันสำเร็จแล้ว",
            ephemeral=True
        )


class VerifyView(discord.ui.View):

    @discord.ui.button(label="ยืนยันตัวตน", style=discord.ButtonStyle.green, emoji="✅")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_modal(VerifyModal())


@bot.command()
async def v(ctx):

    embed = discord.Embed(
        title="📋 ระบบยืนยันตัวตน",
        description="กดปุ่มเพื่อเริ่ม",
        color=discord.Color.blue()
    )

    await ctx.send(embed=embed, view=VerifyView())


@bot.event
async def on_ready():
    print(f"ออนไลน์แล้ว: {bot.user}")

server_on()

bot.run(os.getenv('TOKEN'))