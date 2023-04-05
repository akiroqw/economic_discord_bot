from config import*
from levelcard import*
from page_class import*

class Bot:

    def start(self, token):
        client.run(token)
    
    def bot_ready_event(self):
        @client.event
        async def on_ready():

            cursor.execute("""CREATE TABLE IF NOT EXISTS users(name TEXT,id INT, bank BIGINT,cash BIGINT, server_id INT)""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS shop(role_id INT,id INT,cost BIGINT, description TEXT)""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS inventory(id INT, role_id INT,count INT)""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS levels(level INT, xp INT, required_xp INT, user INT, guild INT, banner TEXT)""")

            for guild in client.guilds:
                for member in guild.members:
                    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                        cursor.execute(f"INSERT INTO users VALUES ('{member}',{member.id},0,0, {guild.id})")
                        cursor.execute(f"INSERT INTO inventory VALUES ({member.id},0,0)")
                        cursor.execute(f"INSERT INTO levels VALUES (0,0,250, {member.id}, {guild.id}, '{None}')")
                    else:
                        pass

                    connection.commit()
            time_conection = datetime.today()
            print(f'The bot is connected. Connection time: {time_conection}')

    def member_join_event(self):
        @client.event
        async def on_member_join(member):
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}',{member.id},0 ,0, {member.guild.id})")
                cursor.execute(f"INSERT INTO inventory VALUES ({member.id}, 0,0)")
                cursor.execute(f"INSERT INTO levels VALUES (0,0,250, {member.id}, {member.guild.id}, '{None}')")
                connection.commit()

            else:
                pass
            
    def balance_event(self):
        @client.command(aliases = ['balance', 'bal', '$'])
        async def _balance(ctx, member: discord.Member = None):
            counter = 0
            if member is None:
                for row in cursor.execute("SELECT name, cash FROM users WHERE server_id = {} ORDER BY cash DESC LIMIT 10".format(ctx.guild.id)):
                        counter += 1
                        if(row[0] == str(ctx.author)):
                            break
                        else:
                            pass
                
                embed =  discord.Embed(color = discord.Color.from_str("#FFFFFF"), description= f'Leaderboard Rank: {counter} th')
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                embed.add_field(value = f"""{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}""",name = f"*Cash:*",inline = True)
                embed.add_field(value = f"""{cursor.execute("SELECT bank FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}""",name = f"*Bank:*",inline = True)
                embed.add_field(value = f"""{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}""",name = f"*Total:*",inline = True)

                now = datetime.now()
                embed.set_footer(text = f'Cегодня, в {now.strftime("%H:%M")}')
                await ctx.send(embed=embed)

            else:
                for row in cursor.execute("SELECT name, cash FROM users WHERE server_id = {} ORDER BY cash DESC LIMIT 10".format(ctx.guild.id)):
                        counter += 1
                        print(member)
                        if(row[0] == str(member)):
                            break
            
                embed =  discord.Embed(color= discord.Color.from_str("#FFFFFF"), description= f'Leaderboard Rank: {counter} th')
                embed.add_field(value = f"""{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]}""",name = f"*Balance:*",inline = True)
                embed.set_author(name=member.display_name, icon_url=member.avatar.url)
                now = datetime.now()
                embed.set_footer(text = f'Cегодня, в {now.strftime("%H:%M")}')
                await ctx.send(embed=embed)

    def give_event(self):
        @client.command(aliases = ['give'])
        async def _give(ctx, member: discord.Member = None, amount:int = None):

            if member is None:
                embed =  discord.Embed(color= discord.Color.from_str("#78dbe2"), description = "Too few arguments given.\n\nUsage:\n`<give-money <member> <amount or all>`")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            else:
                if amount is None:
                    embed =  discord.Embed(color= discord.Color.from_str("#78dbe2"), description = "Too few arguments given.\n\nUsage:\n`<give-money <member> <amount or all>`")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)

                elif amount < 1:
                    embed =  discord.Embed(color= discord.Color.from_str("#78dbe2"), description = "You cannot transfer a **negative amount.**")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)

                else:
                    cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount,member.id))
                    connection.commit()

                    embed = discord.Embed(color= discord.Color.from_str("#FFFFFF"), description = f"{member.mention} has received your **{amount}**")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    now = datetime.now()
                    embed.set_footer(text = f'Cегодня, в {now.strftime("%H:%M")}')
                    await ctx.send(embed=embed)
        
    def remove_bal_event(self):
        @client.command(aliases = ['remove-money'])
        @commands.has_permissions (administrator = True)
        async def _remove(ctx, member: discord.Member = None, amount = None):

            if member is None:
                embed =  discord.Embed(color= discord.Color.from_str("#78dbe2"), description = "Too few arguments given.\n\nUsage:\n`<remove-money <member> <amount or all>`")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            else:
                if amount is None:
                    embed =  discord.Embed(color= discord.Color.from_str("#78dbe2"), description = "Too few arguments given.\n\nUsage:\n`<remove-money <member> <amount or all>`")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)

                elif amount == 'all':
                    cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0,member.id))
                    connection.commit()

                    embed = discord.Embed(color= discord.Color.from_str("#FFFFFF"), description = f"**all** money has been removed from the balance {member.mention}")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    now = datetime.now()
                    embed.set_footer(text = f'Cегодня, в {now.strftime("%H:%M")}')
                    await ctx.send(embed=embed)

                elif int(amount) < 1:
                    embed =  discord.Embed(color= discord.Color.from_str("#78dbe2"), description = "You can't take a negative amount.\n\nUsage:\n`<remove-money <member> <amount or all>`")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)

                else:
                    cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount),member.id))
                    connection.commit()
                    embed = discord.Embed(color= discord.Color.from_str("#FFFFFF"), description = f"Removed **{amount}** from {member.mention}'s cash balance. ")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    now = datetime.now()
                    embed.set_footer(text = f'Cегодня, в {now.strftime("%H:%M")}')
                    await ctx.send(embed=embed)

    def info_event(self):
        @client.command(aliases = ['info', 'информация'])
        async def _info(ctx, member:discord.Member = None):
            if member == None:
                    emb = discord.Embed(title="User Information", color= discord.Color.from_str("#FFFFFF"))
                    emb.add_field(name="Name:", value=ctx.message.author.display_name,inline=False)
                    emb.add_field(name="User ID:", value=ctx.message.author.id,inline=False)
                    author_status = ctx.message.author.status

                    if author_status == discord.Status.online:
                        status = " Online"

                    author_status = ctx.message.author.status
                    if author_status == discord.Status.offline:
                        status = " Not online"

                    author_status = ctx.message.author.status
                    if author_status == discord.Status.idle:
                        status = " Not active"

                    author_status = ctx.message.author.status
                    if author_status == discord.Status.dnd:
                        status = " Do not disturb"

                    emb.add_field(name="Activity:", value=status,inline=False)
                    emb.add_field(name="Status:", value=ctx.message.author.activity,inline=False)
                    emb.add_field(name="Account has been created:", value=ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
                    emb.set_thumbnail(url=ctx.message.author.avatar.url)
                    await ctx.send(embed = emb)
            else:
                    emb = discord.Embed(title="User Information", color= discord.Color.from_str("#FFFFFF"))
                    emb.add_field(name="Name:", value=member.display_name,inline=False)
                    emb.add_field(name="User ID:", value=member.id,inline=False)
                    author_status = member.status

                    if author_status == discord.Status.online:
                        status = " Online"

                    author_status = member.status
                    if author_status == discord.Status.offline:
                        status = " Not Online"

                    author_status = member.status
                    if author_status == discord.Status.idle:
                        status = " Not active"

                    author_status = member.status
                    if author_status == discord.Status.dnd:
                        status = " Do not disturb"

                    emb.add_field(name="Activity:", value=status,inline=False)
                    emb.add_field(name="Status:", value=ctx.message.author.activity,inline=False)
                    emb.add_field(name="Account has been created:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
                    emb.set_thumbnail(url=member.avatar.url)
                    emb.add_field(name="Commands:", value=status,inline=False)
                    await ctx.send(embed = emb)

    def add_shop_event(self):
        @client.command(aliases = ['add-shop'])
        @commands.has_permissions (administrator = True)
        async def _add_shop(ctx, role: discord.Role = None, cost: int = None, * , description: str = None,):

            if role is None:
                embed =  discord.Embed(color= discord.Color.from_str("#78dbe2"), description = "Specify the **role** you want to place in the store!\n\nUsage:\n`<add-shop *<role>* <cost> and <description>`")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            else:
                if cost is None:
                    embed =  discord.Embed(color= discord.Color.from_str("#78dbe2"), description = "Specify the **cost** of the role!\n\nUsage:\n`<add-shop <role> *<cost>* and <description>`")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)

                elif cost < 0:
                    embed =  discord.Embed(color= discord.Color.from_str("#78dbe2"), description = "Uncorrected price!n\nUsage:\n`<add-shop <role> *<cost>* and <description>`")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)
                
                elif description is None:
                    embed =  discord.Embed(color= discord.Color.from_str("#78dbe2"), description = "Specify the **cost** of the role!\n\nUsage:\n`<add-shop <role> <cost> and *<description>*`")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)

                else:
                    cursor.execute(f"INSERT INTO shop VALUES ({role.id},{ctx.guild.id},{cost},'{description}')")
                    connection.commit()
                    embed = discord.Embed(color= discord.Color.from_str("#FFFFFF"),description ="The role has been successfully added!")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    now = datetime.now()
                    embed.set_footer(text = f'Cегодня, в {now.strftime("%H:%M")}')
                    await ctx.send(embed=embed)

    def remove_shop_event(self):
        @client.command(aliases = ['remove-shop'])
        @commands.has_permissions (administrator = True)
        async def _remove_shop(ctx, role: discord.Role = None):

            if role is None:
                embed = discord.Embed(color= discord.Color.from_str("#78dbe2"),description = "Specify the **role** you want to remove from the store!\n\nUsage:\n`<remove-shop <role>`")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            else:
                cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
                connection.commit()
                embed = discord.Embed(color= discord.Color.from_str("#FFFFFF"), description ="The role was successfully deleted!")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                now = datetime.now()
                embed.set_footer(text = f'Cегодня, в {now.strftime("%H:%M")}')
                await ctx.send(embed=embed)

    def shop_event(self): 
        @client.command(aliases = ['shop'])
        async def _shop(ctx):
            embed  = discord.Embed(color = discord.Color.from_str("#FFFFFF"),description = 'Buy an item with the `buy [quantity] <name>` command.\nFor more information on an item use the `item-info <name>` command.\n\n')
            for row in cursor.execute("SELECT role_id, cost , description FROM shop WHERE id = {}".format(ctx.guild.id)):

                if ctx.guild.get_role(row[0]) != None:
                        embed.add_field(value = row[2] ,name = f"{row[1]} - {ctx.guild.get_role(row[0])}",inline = False)
                        embed.add_field(value = '** **',name = '** **' ,inline = False)
                else:
                    pass
            
            embed1 = discord.Embed(color = discord.Color.from_str("#FFFFFF"),description = 'Buy an item with the `buy [quantity] <name>` command.\nFor more information on an item use the `item-info <name>` command.\n\n')
            embeds = [embed, embed1]
            embed.set_author(name= f"『🔥』Role Store", icon_url=client.user.avatar.url)
            embed1.set_author(name= f"『🔥』Role Store", icon_url=client.user.avatar.url)
            await ctx.send(embed=embeds[0], view=Page(embeds))

    def buy_event(self):
        @client.command(aliases = ['buy'])
        async def _buy(ctx, role: discord.Role = None):
                if role is None:
                    embed =  discord.Embed(color= discord.Color.from_str("#78dbe2"), description = "Too few arguments given.\n\nUsage:\n`<buy [quantity] <name>`")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)
                else:
                    if cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
                        embed  = discord.Embed(color = discord.Color.from_str("#78dbe2"),description = 'Not enough funds!!')
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                    else:
                        isRoles = True
                        cursor.execute("SELECT role_id, count FROM inventory WHERE id = {}".format(ctx.author.id))
                        for row in cursor.fetchall():
                                if row[0] == role.id:
                                    cursor.execute("UPDATE inventory SET count = count + {} WHERE role_id = {}".format(1,role.id))
                                    connection.commit()
                                    isRoles = False
                                    embed = discord.Embed(color= discord.Color.from_str("#FFFFFF"),
                                    description = f' You have bough 1{role} for {cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0]}! This is now in your inventory.\n Use this item with the `use <name>` command.')
                                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                                    cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] ,ctx.author.id))
                                    now = datetime.now()
                                    embed.set_footer(text = f'Cегодня, в {now.strftime("%H:%M")}')
                                    await ctx.send(embed=embed)
                                else:
                                    continue

                        if isRoles == True:
                            print("sdfdsf")
                            cursor.execute("INSERT INTO inventory VALUES ({},{},{})".format(ctx.author.id,role.id,1))
                            cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] ,ctx.author.id))
                            embed = discord.Embed(color= discord.Color.from_str("#FFFFFF"),
                                    description = f' You have bough 1{role} for {cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0]}! This is now in your inventory.\n Use this item with the `use <name>` command.')
                            now = datetime.now()
                            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                            embed.set_footer(text = f'Cегодня, в {now.strftime("%H:%M")}')
                            await ctx.send(embed=embed)
                            connection.commit()
                        else:
                            pass
                    
                        if str(ctx.guild.get_role(role.id)) == 'Биткоин':
                            cursor.execute("UPDATE shop SET cost = cost - {} WHERE role_id = {}".format((int(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0]) * 10)/100,role.id))
                        else:
                            pass

    def сommands_error_event(self):
        @client.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.errors.RoleNotFound):
                embed =  discord.Embed(color= discord.Color.from_str("#78dbe2"), description = "I could not find any items in the store with that name.")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

    def avatar_event(self):
        @client.command(aliases = ['avatar'])
        async def _avatar(ctx):
            embed  = discord.Embed(color = discord.Color.from_str("#FFFFFF"),title = "**Avatar**")
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            embed.set_image(url = ctx.message.author.avatar.url)
            await ctx.send(embed = embed)

    def work_event(self, begin_of_range, end_of_range, text_work , cooldown_start, cooldown_end):
        @commands.cooldown(cooldown_start, cooldown_end, commands.BucketType.user)
        @client.command(aliases = ['work'])
        async def _work(ctx):
            count = randint(begin_of_range, end_of_range)
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(count,ctx.author.id))
            connection.commit()
            embed = discord.Embed(color= discord.Color.from_str("#FFFFFF"),description = f"{text_work[randint(1, 3)]} {count}".format(count))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            now = datetime.now()
            embed.set_footer(text = f'Cегодня, в {now.strftime("%H:%M")}')
            await ctx.send(embed = embed)

        @_work.error
        async def work_error(ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                embed = discord.Embed(color= discord.Color.from_str("#78dbe2"), description=f"You cannot work for {error.retry_after/3600:.0f}ч.")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

    def collect_event(self, collecting_roles, cooldown_start, cooldown_end):
        @client.command(aliases = ['collect'])
        async def _collect(ctx):
            count_collecting_roles = 0
            for role in ctx.author.roles:
                if role.name in collecting_roles.keys():
                        cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(collecting_roles.get(role.name),ctx.author.id))
                        connection.commit()
                        count_collecting_roles += 1
                else:
                    continue

            if count_collecting_roles != 0:
                embed = discord.Embed(color= discord.Color.from_str("#FFFFFF"),description =f"The money from the roles was given out.")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                now = datetime.now()
                embed.set_footer(text = f'Cегодня, в {now.strftime("%H:%M")}')
                await ctx.send(embed = embed)
            else:
                pass

            if count_collecting_roles == 0:
                Background = discord.Embed(colour = discord.Color.from_str("#78dbe2"),description = "You don't have any roles from which you could receive money.")
                await ctx.send(embed = Background)
            else:
                pass
        
    def clear_event(self):
        @client.command(aliases = ['c', 'clear'])
        async def _clear(ctx, amount : int = None):
            await ctx.channel.purge(limit = amount)

    def inventory_event(self):
        @client.command(aliases = ['inv','inventory', 'инвентарь'])
        async def _inventory(ctx, member: discord.Member = None):
            if member is None:   
                    embed =  discord.Embed(color= discord.Color.from_str("#FFFFFF"), description='Use an item with the `use [quantity] <name>` command.')
                    cursor.execute("SELECT role_id, count FROM inventory WHERE id = {}".format(ctx.author.id))
                    for row in cursor.fetchall():
                        if row[0]:
                            embed.add_field(value = "** **",name = f"{row[1]} - {ctx.guild.get_role(row[0])}",inline = False)
                            embed.add_field(value = '** **',name = '** **' ,inline = False)
                        else:
                            pass
                    embeds = [embed]
                    embed.set_author(name=ctx.author.display_name + " `s Inventory", icon_url=ctx.author.avatar.url)
                    await ctx.send(embed =embeds[0] , view = Page(embeds))
            else:
                embed = discord.Embed(color= discord.Color.from_str("#FFFFFF"), description= 'Nothing to see here!')
                embed.set_author(name= member.display_name + "`s Inventory", icon_url=member.avatar.url)
                await ctx.send(embed=embed)
            
    def use_event(self):
        @client.command(aliases = ['use'])
        async def _use(ctx, role: discord.Role = None):
            if role is None:
                embed =  discord.Embed(color= discord.Color.from_str("#78dbe2"), description = "Too few arguments given.\n\nUsage:\n`use [quantity] <name>`")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
                return
            
            cursor.execute("SELECT role_id, count FROM inventory WHERE id = {}".format(ctx.author.id))
            role_users = discord.utils.find(lambda r: r.name == role.name, ctx.message.guild.roles)

            if role in ctx.author.roles:
                cursor.execute("UPDATE inventory SET count = count - {} WHERE role_id = {}".format(1,role.id))

                if cursor.execute("SELECT count FROM inventory WHERE role_id = {}".format(role.id)).fetchone()[0] == 0:
                    cursor.execute("DELETE FROM inventory WHERE role_id = {}".format(role.id))

                embed =  discord.Embed(color= discord.Color.from_str("#78dbe2"), description= f'The role has already been used!')
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
                connection.commit()
                return

            for row in cursor.fetchall():
                if row[0] == role.id:
                    if cursor.execute("SELECT count FROM inventory WHERE role_id = {}".format(role.id)).fetchone()[0] <= 1:
                    
                        if str(ctx.guild.get_role(row[0])) != 'Биткоин':
                            await ctx.author.add_roles(role)

                        cursor.execute("DELETE FROM inventory WHERE role_id = {}".format(role.id))
                        if str(ctx.guild.get_role(row[0])) == 'Биткоин':
                            cursor.execute("UPDATE shop SET cost = cost + {} WHERE role_id = {}".format((int(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(row[0])).fetchone()[0]) * 10)/100,row[0]))
                            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(row[0])).fetchone()[0],ctx.author.id))
                            connection.commit()
                    
                        embed =  discord.Embed(color= discord.Color.from_str("#FFFFFF"), description= f'You used {ctx.guild.get_role(row[0])}.')
                        now = datetime.now()
                        embed.set_footer(text = f'Cегодня, в {now.strftime("%H:%M")}')
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                        break

                    else:

                        if str(ctx.guild.get_role(row[0])) != 'Биткоин':
                            if str(ctx.guild.get_role(row[0])) != 'Видеокарта':
                                await ctx.author.add_roles(role)

                        if str(ctx.guild.get_role(row[0])) == 'Биткоин':
                            cursor.execute("UPDATE shop SET cost = cost - {} WHERE role_id = {}".format(80000,row[0]))
                            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(row[0])).fetchone()[0],ctx.author.id))
                        else:
                            pass
                    
                        cursor.execute("UPDATE inventory SET count = count - {} WHERE role_id = {}".format(1,role.id))
                        
                        if cursor.execute("SELECT count FROM inventory WHERE role_id = {}".format(role.id)).fetchone()[0] == 0:
                            cursor.execute("DELETE FROM inventory WHERE role_id = {}".format(role.id))
                        else:
                            pass

                        embed =  discord.Embed(color= discord.Color.from_str("#FFFFFF"), description= f'You used {ctx.guild.get_role(row[0])}.')
                        now = datetime.now()
                        embed.set_footer(text = f'Cегодня, в {now.strftime("%H:%M")}')
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                        connection.commit()
                else:
                    continue

    def roll_range(self, ctx, roll, more, smaller):
        if roll >= more and roll <= smaller:
            flag = False
            cursor.execute("SELECT role_id, count FROM inventory WHERE id = {}".format(ctx.author.id))
            for row in cursor.fetchall():
                if str(ctx.guild.get_role(row[0])) == 'Биткоин':
                    flag = True
                else:
                    continue
            cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id))
            for row in cursor.fetchall():
                if ctx.guild.get_role(row[0]):
                    if str(ctx.guild.get_role(row[0])) == 'Биткоин':
                        if flag:
                            cursor.execute("UPDATE inventory SET count = count + {} WHERE role_id = {}".format(1,row[0]))
                            connection.commit()
                        else:
                            cursor.execute("INSERT INTO inventory VALUES ({},{},{})".format(ctx.author.id, row[0],1))
                            connection.commit()
                else:
                    continue

    def roll_event(self):   
        @client.command(aliases = ['roll'])
        async def _roll(ctx, limit = None):

            if limit is None:
                    embed = discord.Embed(color= discord.Color.from_str("#78dbe2"),description = f"Enter a range.\n\nUsage:\n`<roll <range>`")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    await ctx.send(embed = embed)   
                    return

            if not limit[0].isnumeric():
                embed = discord.Embed(color= discord.Color.from_str("#78dbe2"),description = f"Invalid argument provided.\n\nUsage:\n`roll <range>`")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed = embed)   
                return
            
            if int(limit) < 0:
                embed = discord.Embed(color= discord.Color.from_str("#78dbe2"),description = f"Invalid argument provided.\n\nUsage:\n`roll <range > 0>")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed = embed)   
                return

            else:
                limit = int(limit)

                cursor.execute("SELECT role_id, count FROM inventory WHERE id = {}".format(ctx.author.id))
                quantity = 0

                for row in cursor.fetchall():
                    if row[0]:
                        if str(ctx.guild.get_role(row[0])) == 'Видеокарта':
                                quantity = row[1]
                        else:
                            continue

                roll = randint(0, limit)
                embed = discord.Embed(color= discord.Color.from_str("#FFFFFF"),description = f":game_die: You rolled **{roll}**".format(roll))

                if quantity == 0:
                    if roll == 55:
                        flag = False
                        cursor.execute("SELECT role_id, count FROM inventory WHERE id = {}".format(ctx.author.id))

                        for row in cursor.fetchall():
                                if str(ctx.guild.get_role(row[0])) == 'Биткоин':
                                    flag = True
                                else:
                                    continue

                        cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id))
                        for row in cursor.fetchall():
                            if ctx.guild.get_role(row[0]):
                                if str(ctx.guild.get_role(row[0])) == 'Биткоин':
                                    if flag:
                                        cursor.execute("UPDATE inventory SET count = count + {} WHERE role_id = {}".format(1,row[0]))
                                        connection.commit()
                                    else:
                                        cursor.execute("INSERT INTO inventory VALUES ({},{},{})".format(ctx.author.id, row[0],1))
                                        connection.commit()
                            else:
                                continue
                else:
                    if quantity == 1:
                        self.roll_range(ctx, roll, 54, 56)

                    elif quantity == 2:
                        self.roll_range(ctx, roll, 53, 57)

                    elif quantity == 3:
                        self.roll_range(ctx, roll, 52, 58)
                    
                    elif quantity == 4:
                         self.roll_range(ctx, roll, 51, 59)
                    
                    elif quantity == 5:
                         self.roll_range(ctx, roll, 50, 60)
            
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed = embed)

    def remove_all_balance(self):
        @commands.has_permissions (administrator = True)
        @client.command(aliases = ['remove-all-balance'])
        async def _remove_bal(ctx, member: discord.Member = None):
            cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0,member.id))

    def remove_all_roles(self):
        @commands.has_permissions (administrator = True)
        @client.command(aliases = ['remove-all-roles'])
        async def _remove_roles(ctx, member: discord.Member = None):
            for i in range(len(member.roles)-1):
                await member.remove_roles(member.roles[i+1])

    def remove_all_inventory(self):
         @commands.has_permissions (administrator = True)
         @client.command(aliases = ['remove-inventory'])
         async def _remove_inv(ctx, member: discord.Member = None):
                    cursor.execute("SELECT role_id, count FROM inventory WHERE id = {}".format(member.id))
                    for row in cursor.fetchall():
                        if row[0]:
                            cursor.execute("DELETE FROM inventory WHERE role_id = {}".format(row[0]))
                            connection.commit()
                        else:
                            continue

    def set_money_event(self):
        @client.command(aliases = ['set-money'])
        async def _set_money(ctx, amount:int = None, member: discord.Member = None):
            if member is None:
                embed =  discord.Embed(color= discord.Color.red(), description = "Too few arguments given.\n\nUsage:\n`<set-money <member> <amount or all>`")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            else:
                if amount is None:
                    embed =  discord.Embed(color= discord.Color.red(), description = "Too few arguments given.\n\nUsage:\n`<set-money <member> <amount or all>`")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)
                else:
                    cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(amount,member.id))
                    embed = discord.Embed(color= discord.Color.from_rgb(216,191,216), description = f"The balance of the user {member.mention} has been changed to **{amount}**")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)
                    connection.commit()

    def wipe_event(self):
        @client.command(aliases = ['wipe'])
        async def _wipe(ctx):
            cursor.execute("DROP TABLE users")
            cursor.execute("DROP TABLE inventory")
            cursor.execute("DROP TABLE levels")
            connection.commit()

    def banner_event(self):
        @client.command(aliases = ['set-banner'])
        async def on_message(ctx):
            for attach in ctx.message.attachments:
                await attach.save(f"backgrounds/{attach.filename}")
            cursor.execute(f"UPDATE levels SET banner = '{attach.filename}' WHERE user = {ctx.author.id}")
            connection.commit()


    def update_xp(self, count, message):
        cursor.execute(f"UPDATE levels SET xp = xp + {count} WHERE user = {message.author.id}")
        connection.commit()

    def update_level(self, count, message):
        cursor.execute(f"UPDATE levels SET required_xp = {(self.get_data_level(message, 'required_xp') * self.get_data_level(message, 'level')) - self.get_data_level(message, 'required_xp') * {count}} WHERE user = {message.author.id}")
        connection.commit()

    def on_message_event(self):
        @client.event
        async def on_message(message):

            await client.process_commands(message)
            if self.get_data_level(message, 'xp') < self.get_data_level(message, 'required_xp'):
                if self.get_data_level(message, 'level') <= 5:
                    self.update_xp(1, message)

                elif self.get_data_level(message, 'level') >= 5 and self.get_data_level(message, 'level') <= 15:
                    self.update_xp(5, message)

                elif self.get_data_level(message, 'level') >= 15 and self.get_data_level(message, 'level') <= 30:
                    self.update_xp(10, message)
                
                elif self.get_data_level(message, 'level') >= 30 and self.get_data_level(message, 'level') <= 50:
                    self.update_xp(15, message)

                elif self.get_data_level(message, 'level') >= 50 and self.get_data_level(message, 'level') <= 60:
                    self.update_xp(20, message)


            else:
                cursor.execute(f"UPDATE levels SET level = level + {1} WHERE user = {message.author.id}")
                cursor.execute(f"UPDATE levels SET xp = 0 WHERE user = {message.author.id}")

                if self.get_data_level(message, 'level') <= 5:
                    cursor.execute(f"UPDATE levels SET required_xp = {(self.get_data_level(message, 'required_xp') * self.get_data_level(message, 'level')) - self.get_data_level(message, 'required_xp')/2} WHERE user = {message.author.id}")
                    connection.commit()
                elif self.get_data_level(message, 'level') >= 5 and self.get_data_level(message, 'level') <= 15:
                    self.update_level(4, message)

                elif self.get_data_level(message, 'level') >= 15 and self.get_data_level(message, 'level') <= 30:
                    self.update_level(5, message)
                
                elif self.get_data_level(message, 'level') >= 30 and self.get_data_level(message, 'level') <= 50:
                    self.update_level(6, message)

                elif self.get_data_level(message, 'level') >= 50 and self.get_data_level(message, 'level') <= 60:
                    self.update_level(7, message)
                
    def set_xp_event(self):
        @client.command(aliases = ['set-xp'])
        async def _set_xp(ctx, member : discord.Member = None, count : int = None):
            cursor.execute(f"UPDATE levels SET xp = {count} WHERE user = {member.id}")
            connection.commit()

    def set_level_event(self):
        @client.command(aliases = ['set-level'])
        async def _set_level(ctx, member : discord.Member = None, count : int = None):
            cursor.execute(f"UPDATE levels SET level = {count} WHERE user = {member.id}")
            connection.commit()

    def get_data_level(self, ctx, data):
        cursor.execute(f"SELECT {data} FROM levels WHERE user = {ctx.author.id}")
        return cursor.fetchone()[0]
    
    def level_event(self):
        @client.command(aliases = ['level','ранг', 'lvl'])
        async def _level(ctx, member : discord.Member = None):

                levelcard = LevelCard()
                levelcard.avatar = ctx.author.avatar.url

                member = await ctx.guild.fetch_member(ctx.author.id)
                if member.nick != None:
                    levelcard.name = member.nick
                else:
                    levelcard.name = ctx.author.name
                
                levelcard.xp = self.get_data_level(ctx, 'xp')
                levelcard.required_xp = self.get_data_level(ctx, 'required_xp')
                levelcard.level = self.get_data_level(ctx, 'level')

                for row in cursor.execute("SELECT banner FROM levels WHERE user = {}".format(ctx.author.id)):
                    if row[0]:
                        levelcard.path = row[0]
                    else:
                        pass

                await ctx.send(file = await levelcard.create())


bot = Bot()

bot.bot_ready_event()
bot.member_join_event()

bot.balance_event()
bot.give_event()
bot.remove_bal_event()
bot.info_event()
bot.add_shop_event()
bot.remove_shop_event()
bot.shop_event()
bot.buy_event()
bot.set_money_event()
bot.сommands_error_event()

bot.clear_event()   
bot.inventory_event()
bot.use_event()
bot.roll_event()
bot.avatar_event()

bot.collect_event(collecting_roles, 0, 0)
bot.work_event(70000, 100000, text_work, 0, 0)

bot.remove_all_inventory()
bot.remove_all_balance()
bot.remove_all_roles()
bot.wipe_event()

bot.banner_event()
bot.level_event()
bot.on_message_event()

bot.set_xp_event()

bot.start(setting['TOKEN'])