import discord
from discord.ext import commands
import os
from datetime import datetime

TOKEN = os.getenv("DISCORD_TOKEN")

# ID des salons (à remplacer par les tiens)
COMMANDES_CHANNEL_ID = 123456789012345678
HISTORIQUE_CHANNEL_ID = 123456789012345678
STOCK_ARGENT_CHANNEL_ID = 123456789012345678
STOCK_MARCHANDISE_CHANNEL_ID = 123456789012345678

# Utilisateurs autorisés
AUTHORIZED_USERS = ["Alpha-1", "Alpha-4", "Alpha-5"]

# Stock initial
stock = {
    "contrats": 0,
    "kit_crochetage": 0,
    "graines_cannabis": 0,
    "argent_sale": 0,
    "argent_propre": 0,
}

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Vérifie si l’utilisateur est autorisé
def is_authorized(user):
    return user.display_name in AUTHORIZED_USERS

# Met à jour les salons de stock
async def update_stocks():
    argent_channel = bot.get_channel(STOCK_ARGENT_CHANNEL_ID)
    marchandises_channel = bot.get_channel(STOCK_MARCHANDISE_CHANNEL_ID)

    argent_msg = (
        f"💵 Argent propre : {stock['argent_propre']}\n"
        f"💸 Argent sale : {stock['argent_sale']}"
    )

    marchandises_msg = (
        f"📜 Contrats : {stock['contrats']}\n"
        f"🛠️ Kits de crochetage : {stock['kit_crochetage']}\n"
        f"🌱 Graines de cannabis : {stock['graines_cannabis']}"
    )

    await argent_channel.send(argent_msg)
    await marchandises_channel.send(marchandises_msg)

# Commande ajout/retrait
@bot.command()
async def stock(ctx, action: str, item: str, quantite: int):
    if not is_authorized(ctx.author):
        await ctx.send("❌ Tu n’as pas l’autorisation.")
        return

    if item not in stock:
        await ctx.send("❌ Objet inconnu.")
        return

    if action == "+":
        stock[item] += quantite
    elif action == "-":
        stock[item] -= quantite
    else:
        await ctx.send("❌ Action invalide. Utilise + ou -.")
        return

    # Historique
    historique_channel = bot.get_channel(HISTORIQUE_CHANNEL_ID)
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    await historique_channel.send(
        f"📦 [{now}] {ctx.author.display_name} a fait **{action}{quantite} {item}**"
    )

    await update_stocks()
    await ctx.send("✅ Stock mis à jour !")

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

bot.run(TOKEN)
