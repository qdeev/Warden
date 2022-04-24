from constants import *
import discord
from discord.ext import commands


class Bot(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def clear(self, ctx, amount: int = 5):

        session = sessions["bot_serversettings"]
        channel_id = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first().moderation_log

        if amount <= 15:
            await ctx.channel.purge(limit=amount + 1)

            logger.info(f"{ctx.author} cleared {amount} messages")
            await self.client.get_channel(channel_id).send(
                f"{ctx.author.mention} cleared {amount} messages")
        else:
            await ctx.send(f"This command can delete up to 15 messages")

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member, *, reason=None):

        session = sessions["bot_serversettings"]
        channel_id = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first().moderation_log

        logger.info(f"{ctx.message.author} kicked {member}")
        await ctx.channel.purge(limit=1)
        await member.kick(reason=reason)
        await self.client.get_channel(channel_id).send(
            f"{member.mention} was kicked by {ctx.message.author.mention}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, *, reason=None):

        session = sessions["bot_serversettings"]
        channel_id = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first().moderation_log

        logger.info(f"{ctx.message.author} banned {member}")
        emb = discord.Embed(colour=discord.Colour.red())
        if member != ctx.author:
            await ctx.channel.purge(limit=1)
            await member.ban(reason=reason)

            emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            emb.add_field(name="Banned User 🤬", value=member.mention)
            await self.client.get_channel(channel_id).send(embed=emb)

        else:
            await self.client.get_channel(channel_id).send("You can`t ban yourself...")

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def unban(self, ctx, id_):

        session = sessions["bot_serversettings"]
        channel_id = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first().moderation_log

        emb = discord.Embed(colour=discord.Colour.green())
        member = await self.client.fetch_user(id_)
        logger.info(f"{ctx.message.author} unbanned {member}")
        await ctx.channel.purge(limit=1)
        await ctx.guild.unban(member)

        emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        emb.add_field(name="Unbanned User ☺️", value=member.mention)
        await self.client.get_channel(channel_id).send(embed=emb)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def amnesty(self, ctx):
        await ctx.channel.purge(limit=1)

        session = sessions["bot_serversettings"]
        channel_id = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first().moderation_log

        logger.info(f"{ctx.message.author} unbanned everyone")
        banned = await ctx.guild.bans()
        bans = [entry.user.id for entry in banned]

        if bans:

            for banned_user in bans:
                member = await self.client.fetch_user(banned_user)
                await ctx.guild.unban(member)

            emb = discord.Embed(title="Unbanned everyone 😇", colour=discord.Colour.blue())
            emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await self.client.get_channel(channel_id).send(embed=emb)
        else:
            await self.client.get_channel(channel_id).send("No one is banned...")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def give_role(self, ctx, user: discord.Member, *, role: discord.Role):
        await ctx.channel.purge(limit=1)

        session = sessions["bot_serversettings"]
        channel_id = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first().moderation_log

        if role in user.roles:
            await self.client.get_channel(channel_id).send(
                f"{user.mention} already has the role, {role}")
        else:
            emb = discord.Embed(title="Given role", colour=discord.Colour.green())
            emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            emb.add_field(name=f"{role}", value=user.mention)
            await user.add_roles(role)
            await self.client.get_channel(channel_id).send(embed=emb)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def remove_role(self, ctx, user: discord.Member, *, role: discord.Role):
        await ctx.channel.purge(limit=1)

        session = sessions["bot_serversettings"]
        channel_id = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first().moderation_log

        if role in user.roles:
            emb = discord.Embed(title="Removed role", colour=discord.Colour.red())
            emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            emb.add_field(name=f"{role}", value=user.mention)
            await user.remove_roles(role)
            await self.client.get_channel(channel_id).send(embed=emb)
        else:
            await self.client.get_channel(channel_id).send(f"{user.mention} doesn't have {role} role")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def mute(self, ctx, user: discord.Member):
        await ctx.channel.purge(limit=1)

        session = sessions["bot_serversettings"]
        channel_id = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first().moderation_log

        mute_role_id = session.query(Channels).filter(Channels.server_id == ctx.guild.id).first().mute_role
        mute_role = discord.utils.get(ctx.guild.roles, id=mute_role_id)

        if mute_role in user.roles:
            await self.client.get_channel(channel_id).send(f"{user.mention} is already muted...")
        else:
            emb = discord.Embed(title="Muted 🤐", colour=mute_role.colour)
            emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            emb.add_field(name=f"{mute_role}", value=user.mention)
            await user.add_roles(mute_role)
            await self.client.get_channel(channel_id).send(embed=emb)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def unmute(self, ctx, user: discord.Member):
        await ctx.channel.purge(limit=1)

        session = sessions["bot_serversettings"]
        channel_id = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first().moderation_log

        mute_role_id = session.query(Channels).filter(Channels.server_id == ctx.guild.id).first().mute_role
        mute_role = discord.utils.get(ctx.guild.roles, id=mute_role_id)

        if mute_role in user.roles:
            emb = discord.Embed(title="Unmuted", colour=mute_role.colour)
            emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            emb.add_field(name=f"😲!", value=user.mention)
            await user.remove_roles(mute_role)
            await self.client.get_channel(channel_id).send(embed=emb)
        else:
            await self.client.get_channel(channel_id).send(f"{user.mention} is not muted...")

    @commands.command()
    async def help(self, ctx):
        await ctx.channel.purge(limit=1)
        emb = discord.Embed(title="Help", colour=discord.Colour.purple())
        emb.add_field(name="Moderation",
                      value="`clear`, `kick`, `ban`, `unban`, `mute`, `unmute`, `amnesty`, `give_role`, `remove_role`",
                      inline=False)
        emb.add_field(name="Music",
                      value="`join`, `disconnect`, `play`, `pause`, `resume`",
                      inline=False)
        emb.add_field(name="Settings",
                      value="`set_prefix`, `set_moderation_log`, `set_settings_log`, `reload_roles`, `set_mute_role`",
                      inline=False)
        await ctx.send(embed=emb)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """working with errors"""

        if isinstance(error, commands.MemberNotFound) or isinstance(error, discord.errors.NotFound):
            await ctx.send("Member not found")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.name} You haven't got enough permissions.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.name}, specify the required argument. 😵‍💫")


def setup(client):
    client.add_cog(Bot(client))
