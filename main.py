import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# =========================
# WEB SERVER (Render)
# =========================
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# =========================
# DISCORD BOT
# =========================

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ===== ID ห้องยืนยัน =====
VERIFY_CHANNEL_ID = 123456789012345678


# =========================
# MODAL
# =========================
class VerifyModal(discord.ui.Modal, title="📋 ยืนยันตัวตน"):

    game_name = discord.ui.TextInput(label="ชื่อในเกม")
    uid = discord.ui.TextInput(label="UID (ตัวเลข)")
    nickname = discord.ui.TextInput(label="ชื่อเล่น")
    age = discord.ui.TextInput(label="อายุ (ตัวเลข)")

    async def on_submit(self, interaction: discord.Interaction):

        member = interaction.user

        # ===== เช็คตัวเลข =====
        if not self.uid.value.isdigit():
            return await interaction.response.send_message(
                "❌ UID ต้องเป็นตัวเลข",
                ephemeral=True
            )

        if not self.age.value.isdigit():
            return await interaction.response.send_message(
                "❌ อายุ ต้องเป็นตัวเลข",
                ephemeral=True
            )

        # ===== Embed =====
        embed = discord.Embed(
            title="✅ ยืนยันตัวตนสำเร็จ",
            color=discord.Color.green()
        )

        embed.add_field(
            name="🎮 ชื่อในเกม",
            value=self.game_name.value,
            inline=False
        )

        embed.add_field(
            name="🆔 UID",
            value=self.uid.value,
            inline=False
        )

        embed.add_field(
            name="👤 ชื่อเล่น",
            value=self.nickname.value,
            inline=False
        )

        embed.add_field(
            name="🎂 อายุ",
            value=self.age.value,
            inline=False
        )

        embed.set_footer(
            text=f"ยืนยันโดย {member}"
        )

        # ===== ส่งไปห้อง =====
        channel = await bot.fetch_channel(
            VERIFY_CHANNEL_ID
        )

        await channel.send(embed=embed)

        # ===== ตอบกลับ =====
        await interaction.response.send_message(
            "✅ ยืนยันสำเร็จแล้ว",
            ephemeral=True
        )


# =========================
# BUTTON
# =========================
class VerifyView(discord.ui.View):

    @discord.ui.button(
        label="ยืนยันตัวตน",
        style=discord.ButtonStyle.green,
        emoji="✅"
    )
    async def verify(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_modal(
            VerifyModal()
        )


# =========================
# COMMAND
# =========================
@bot.command()
async def verify(ctx):

    embed = discord.Embed(
        title="📋 ระบบยืนยันตัวตน",
        description="กดปุ่มเพื่อเริ่ม",
        color=discord.Color.blue()
    )

    await ctx.send(
        embed=embed,
        view=VerifyView()
    )


# =========================
# READY
# =========================
@bot.event
async def on_ready():
    print(f"ออนไลน์แล้ว: {bot.user}")


# =========================
# RUN
# =========================
keep_alive()
bot.run(TOKEN)