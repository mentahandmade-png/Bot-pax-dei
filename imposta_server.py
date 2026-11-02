"""Ricostruisce il server Discord seguendo struttura.json.

Uso:
  python imposta_server.py            # crea ruoli/canali mancanti
  python imposta_server.py --reset    # PRIMA cancella tutti i canali esistenti
"""
import json
import os
import sys

import discord

TOKEN = os.environ.get("DISCORD_TOKEN")
GUILD_ID = int(os.environ.get("GUILD_ID", "0"))
RESET = "--reset" in sys.argv

with open("struttura.json", encoding="utf-8") as f:
    STRUTTURA = json.load(f)

client = discord.Client(intents=discord.Intents.default())


async def imposta_ruoli(guild):
    ruoli = {}
    for r in STRUTTURA["ruoli"]:
        ruolo = discord.utils.get(guild.roles, name=r["nome"])
        perms = discord.Permissions.all() if r.get("admin") else discord.Permissions.general()
        colore = discord.Colour.from_str(r["colore"])
        if ruolo is None:
            ruolo = await guild.create_role(name=r["nome"], colour=colore, permissions=perms, hoist=True)
            print(f"+ ruolo {r['nome']}")
        ruoli[r["nome"]] = ruolo
    return ruoli


async def imposta_canali(guild, ruoli):
    for c in STRUTTURA["categorie"]:
        overwrites = {}
        if c.get("solo_ruoli"):
            overwrites[guild.default_role] = discord.PermissionOverwrite(view_channel=False)
            for nome in c["solo_ruoli"]:
                overwrites[ruoli[nome]] = discord.PermissionOverwrite(view_channel=True)
        if c.get("sola_lettura"):
            overwrites[guild.default_role] = discord.PermissionOverwrite(send_messages=False)
            for nome in ("Capo Clan", "Ufficiale"):
                if nome in ruoli:
                    overwrites[ruoli[nome]] = discord.PermissionOverwrite(send_messages=True)

        cat = discord.utils.get(guild.categories, name=c["nome"])
        if cat is None:
            cat = await guild.create_category(c["nome"], overwrites=overwrites)
            print(f"+ categoria {c['nome']}")
        for nome in c.get("testo", []):
            if not discord.utils.get(cat.text_channels, name=nome):
                await guild.create_text_channel(nome, category=cat)
                print(f"  + #{nome}")
        for nome in c.get("vocali", []):
            if not discord.utils.get(cat.voice_channels, name=nome):
                await guild.create_voice_channel(nome, category=cat)
                print(f"  + 🔊 {nome}")


@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        print("Server non trovato: controlla GUILD_ID e che il bot sia nel server.")
    else:
        print(f"Imposto il server: {guild.name}")
        if RESET:
            for ch in list(guild.channels):
                await ch.delete()
            print("- cancellati tutti i canali esistenti")
        ruoli = await imposta_ruoli(guild)
        await imposta_canali(guild, ruoli)
        print("Fatto!")
    await client.close()


if not TOKEN or not GUILD_ID:
    sys.exit("Imposta le variabili DISCORD_TOKEN e GUILD_ID prima di avviare.")
client.run(TOKEN)
