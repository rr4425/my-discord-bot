import discord
import json
import os
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = discord.Client(intents=intents)

FILE = "am4k.json"

def load_data():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

@bot.event
async def on_ready():
    print(f"已上線: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    data = load_data()
    msg = message.content.strip()
    args = msg.split()

    if msg.startswith("增加") or msg.startswith("加幣"):
        if len(args) >= 3 and message.mentions:
            target = message.mentions[0]
            try:
                amount = int(args[-1])
                uid = str(target.id)
                data[uid] = data.get(uid, 0) + amount
                save_data(data)
                await message.channel.send(f"**增加Am4k**\n對象 {target.mention}\n增加 {amount} Am4k\n目前 {data[uid]}")
            except:
                pass
        return

    if msg.startswith("扣除") or msg.startswith("扣幣"):
        if len(args) >= 3 and message.mentions:
            target = message.mentions[0]
            try:
                amount = int(args[-1])
                uid = str(target.id)
                data[uid] = data.get(uid, 0) - amount
                save_data(data)
                await message.channel.send(f"**扣除Am4k**\n對象 {target.mention}\n扣除 {amount} Am4k\n目前 {data[uid]}")
            except:
                pass
        return

    if msg.startswith("設定") or msg.startswith("設置"):
        if len(args) >= 3 and message.mentions:
            target = message.mentions[0]
            try:
                amount = int(args[-1])
                data[str(target.id)] = amount
                save_data(data)
                await message.channel.send(f"**設定Am4k**\n對象 {target.mention}\n設定為 {amount} Am4k")
            except:
                pass
        return

    if msg.startswith("查看") or msg.startswith("查詢"):
        target = message.mentions[0] if message.mentions else message.author
        await message.channel.send(f"{target.mention} 目前Am4k **{data.get(str(target.id), 0)}**")
        return

    if msg.startswith("排行榜") or msg.startswith("排行"):
        if not data:
            await message.channel.send("目前還沒有人有Am4k")
            return
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]
        text = "**🏆 Am4k 排行榜 TOP 10**\n\n"
        for i, (uid, amount) in enumerate(sorted_data, 1):
            try:
                name = (await bot.fetch_user(int(uid))).display_name
            except:
                name = f"ID:{uid}"
            text += f"{i}. {name} - {amount} Am4k\n"
        await message.channel.send(text)
        return

    if msg.startswith("抽獎"):
        try:
            amount = int(args[-1])
            members = [m for m in message.guild.members if not m.bot]
            if message.mentions:
                winners = message.mentions
            else:
                count = int(args[1]) if len(args) >= 3 else 1
                count = min(count, len(members))
                winners = random.sample(members, count)
            for w in winners:
                data[str(w.id)] = data.get(str(w.id), 0) + amount
            save_data(data)
            winner_text = "、".join([w.mention for w in winners])
            await message.channel.send(f"**🎉 Am4k 抽獎**\n中獎者: {winner_text}\n每人獲得 {amount} Am4k！")
        except:
            await message.channel.send("用法: `抽獎 人數 金額` 例如 `抽獎 3 100`")
        return

bot.run(os.getenv("TOKEN"))
