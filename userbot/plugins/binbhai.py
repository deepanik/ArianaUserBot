"""Emoji
Available Commands:
.BinBhai
Credits to @BinBhai
"""

from telethon import events

import asyncio

from userbot.utils import admin_cmd


@borg.on(admin_cmd("BinBhai"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1.5
    animation_ttl = range(0,36)
    #input_str = event.pattern_match.group(1)
   # if input_str == "BinBhai":
    await event.edit("@BinBhai")
    animation_chars = [
            "@BinBhai tera baap",
            "@BinBhai is bot ka creator",
            "@BinBhai bot ko jaan dene wala",
            "@BinBhai owner of ArianaUserBot ",
            "tujhe aur kya chaiye vo hai mere sath",
            "tera baap",
            "@BinBhai"
         ]
            

    for i in animation_ttl:
        	
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 18])
