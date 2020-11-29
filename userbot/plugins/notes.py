# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""notes
Available Commands:
.save
.listnotes
.clear"""
from telethon import events, utils
from telethon.tl import types
from userbot.plugins.sql_helper.notes_sql import get_notes, add_note, remove_note, get_all_notes
from userbot.utils import admin_cmd


TYPE_TEXT = 0
TYPE_PHOTO = 1
TYPE_DOCUMENT = 2


@borg.on(events.NewMessage(pattern=r'\#(\S+)', outgoing=True))
async def on_note(event):
    name = event.pattern_match.group(1)
    note = get_notes(name)
    if note:
        if note.note_type == TYPE_PHOTO:
            media = types.InputPhoto(
                int(note.media_id),
                int(note.media_access_hash),
                note.media_file_reference
            )
        elif note.note_type == TYPE_DOCUMENT:
            media = types.InputDocument(
                int(note.media_id),
                int(note.media_access_hash),
                note.media_file_reference
            )
        else:
            media = None
        message_id = event.message.id
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        await borg.send_message(
            event.chat_id,
            note.reply,
            reply_to=message_id,
            file=media
        )
        await event.delete()


@borg.on(admin_cmd("save (.*)"))
async def on_note_save(event):
    name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if msg:
        note = {'type': TYPE_TEXT, 'text': msg.message or ''}
        if msg.media:
            media = None
            if isinstance(msg.media, types.MessageMediaPhoto):
                media = utils.get_input_photo(msg.media.photo)
                note['type'] = TYPE_PHOTO
            elif isinstance(msg.media, types.MessageMediaDocument):
                media = utils.get_input_document(msg.media.document)
                note['type'] = TYPE_DOCUMENT
            if media:
                note['id'] = media.id
                note['hash'] = media.access_hash
                note['fr'] = media.file_reference
        add_note(name, note['text'], note['type'], note.get('id'), note.get('hash'), note.get('fr'))
        await event.edit("note {name} saved successfully. Get it with #{name}".format(name=name))
    else:
        await event.edit("Reply to a message with `notes keyword` to save the note")


@borg.on(admin_cmd("listnotes"))
async def on_note_list(event):
    all_notes = get_all_notes()
    OUT_STR = "Available notes:\n"
    if len(all_notes) > 0:
        for a_note in all_notes:
            OUT_STR += f"✔ #{a_note.note} \n"
    else:
        OUT_STR = "No notes. Start Saving using `.notes`"
    if len(OUT_STR) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "notes.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available notes",
                reply_to=event
            )
            await event.delete()
    else:
        await event.edit(OUT_STR)


@borg.on(admin_cmd("clear (\S+)"))
async def on_note_delete(event):
    name = event.pattern_match.group(1)
    remove_note(name)
    await event.edit("note #{} deleted successfully".format(name))
