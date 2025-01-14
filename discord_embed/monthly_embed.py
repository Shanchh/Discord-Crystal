from discord_embed import init, basic

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

def active_result(count, uncount, guild_avatar):
    embed = basic("活躍用戶總計", f"目前活躍用戶數量: {count}\n非活躍用戶數量: {uncount}", 0xac21de)
    embed.set_thumbnail(url = guild_avatar)
    return embed

def active_user(count, user_mention, dateDeadLine, avatar):
    embed = basic(f"第{count + 1}名", f"訂閱者: {user_mention}\n訂閱到期日: {dateDeadLine}", 0x6077e6)
    embed.set_thumbnail(url = avatar)
    return embed
    
def statistics(quantity, amount, avatar):
    embed = basic("總計月數金額", f"總月數: {quantity}\n總金額: {amount}", 0x72fde1)
    embed.set_thumbnail(url = avatar)
    return embed