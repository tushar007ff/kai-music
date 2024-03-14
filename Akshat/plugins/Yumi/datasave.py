from pyrogram import Client, filters
from pymongo import MongoClient
from config import MONGO_DB_URI
from Akshat import app
from Akshat.misc import SUDOERS

client = MongoClient(MONGO_DB_URI)
db = client.send
col = db.groups

# Command to display all group IDs
@app.on_message(filters.command("dgroups") & SUDOERS)
async def display_groups(client, message):
    group_ids = [str(group["_id"]) for group in col.find()]
    if group_ids:
        groups_text = "\n".join(group_ids)
        await message.reply_text(f"Group IDs:\n{groups_text}")
    else:
        await message.reply_text("No groups found!")


@app.on_message(filters.command("addgroup") & SUDOERS)
async def add_group(client, message):
    group_id = int(message.text.split()[1])
    col.insert_one({"_id": group_id})
    await message.reply_text("Group added successfully!")

@app.on_message(filters.command("rmgroup") & SUDOERS)
async def remove_group(client, message):
    group_id = int(message.text.split()[1])
    col.delete_one({"_id": group_id})
    await message.reply_text("Group removed successfully!")

@app.on_message(filters.command("dsave") & SUDOERS)
async def send_to_groups(client, message):
    command_parts = message.text.split(" ")
    if message.reply_to_message:
        text = message.reply_to_message
        for group in col.find():
            await text.forward(group["_id"])
    else:
        if len(command_parts) > 1:
            text = " ".join(command_parts[1:])
        else:
            return await message.reply_text("bsdk text kon dalega")
        for group in col.find():
            await app.send_message(group["_id"], text)
