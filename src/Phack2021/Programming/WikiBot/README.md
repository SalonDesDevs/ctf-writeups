# WikiBot - 256 points

Quand on lui envoie des messages (en privé), le bot nous permet de participer à un quiz (en répondant plusieurs fois "yes" à ses questions pour lancer celui-ci).
Il s'agit comme il le dit lui-même de diverses questions simples sur des personnes connues et dont on peut trouver la réponse par une simple recherche Google de la question. Néanmoins nous ne disposons que de 3 secondes pour répondre correctement à celles-ci. En essayant le quiz quelques fois, on se retrouve face aux mêmes questions assez vite, ce qui laisse penser que la liste de celles-ci est définie (elles ne sont pas créées à la volée) et assez courte (une petite dizaine).

J'ai alors créé un selfbot (sur un nouveau compte Discord) répondant aux questions par la réponse qu'il connaît quand il détecte celles-ci, et, après 6 bonnes réponses de suite, le bot nous donne le flag

```python
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio

TOKEN = ""

bot = Bot(command_prefix = "!!!")

answers = {
    "Barack Obama" : "08/04/1961",
    "nationality of Gal Gadot" : "Israeli",
    "best CTF event": "P'HackCTF",
    "birthplace of Daniel Ricciardo" : "Perth",
    "How old is Omar Sy" : "43",
    "What is the full name of birth of Billie Eilish" : "Billie Eilish Pirate Baird O'Connell"
}

@bot.event
async def on_ready():
    print("BOT READY")

@bot.event
async def on_message(msg):
    if msg.author.id == 819936988634808340 and "**Question" in msg.content:
        for i in answers:
            if i in msg.content:
                await msg.channel.send(answers[i])
                break
        else:
            pass

bot.run(TOKEN, bot = False)
```

Le challenge voulait probablement nous faire automatiser l'obtention de la réponse but it just works.