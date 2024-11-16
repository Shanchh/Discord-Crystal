import discord
import datetime

def init():
    embed = discord.Embed(timestamp = datetime.datetime.now())
    embed.set_footer(text="Crystal", icon_url="https://i.imgur.com/jsMle7g.jpeg")
    return embed

def basic(title = None, description = None, color = None):
    embed = init()
    embed.title = title
    embed.description = description
    embed.color = color
    return embed

def request_error(title = None):
    embed = init()
    embed.title = title
    embed.description = "處理請求時發生問題"
    embed.color = 0xff0000
    return embed

async def listDetail_embed(bot, dataList, count):
    embed = init()
    embed.title = f"總明細查詢:第{count + 1}筆至第{count + len(dataList)}筆"
    for index, data in enumerate(dataList):
        user = await bot.fetch_user(data["userId"])
        embed.add_field(name = f"{count + index + 1}.識別編號:{data['dataId']}", value = f"訂閱者: {user.mention}，訂閱日期: {data['purchaseDate']}\n數量: {data['quantity']}，購買方式: {data['payment']}", inline = False)
    embed.color = 0xf0e033
    return embed

def getDetail_embed(avatar):
    embed = init()
    embed.description = "已收到請求！"
    embed.color = 0x00ff11
    embed.set_author(name = "訂閱明細", icon_url = avatar)
    return embed

def getDetail_info(count, data, avatar):
    embed = init()
    embed.title = f"第 {count + 1} 筆訂閱明細: {data['dataId']}" + "\u3000" * 10
    embed.add_field(name="📅 訂閱日期", value=data["purchaseDate"], inline=True)
    embed.add_field(name="🗓️ 月數", value=data["quantity"], inline=True)
    embed.add_field(name="💳 訂閱方式", value=data["payment"], inline=True)
    embed.set_thumbnail(url = avatar)
    embed.color = 0xff9f1a
    return embed

def checkstatus(content, color, avatar):
    embed = init()
    embed.title = "訂閱狀態查詢"
    embed.description = content
    embed.set_thumbnail(url = avatar)
    embed.color = color
    return embed