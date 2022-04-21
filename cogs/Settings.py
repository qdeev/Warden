import discord
from discord.ext import commands
from constants import *


class Settings(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.commands_list = [
            "help",
            "kick", "clear", "ban", "unban", "amnesty", "give_role", "remove_role", "mute", "unmute",
            "play", "disconnect", "join", "pause", "resume",
            "set_prefix", "set_moderation_log", "set_settings_log", "reload_roles", "set_mute_role",
            "load", "unload", "reload"
        ]

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Starting work")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        session = sessions["bot_serversettings"]

        session.delete(session.query(Servers).filter(Servers.id == guild.id).all())
        session.delete(session.query(Prefix).filter(Servers.id == guild.id).all())
        session.delete(session.query(Channels).filter(Servers.id == guild.id).all())
        session.delete(session.query(Roles).filter(Servers.id == guild.id).all())

        session.commit()

    @commands.Cog.listener()
    async def on_message(self, msg):
        text = str(msg.content).split()

        session = sessions["bot_serversettings"]
        prefix = session.query(Prefix).filter(Prefix.server_id == msg.guild.id).first()
        try:
            if text[0].startswith(prefix.prefix) and (text[0][1:] not in self.commands_list):
                await msg.channel.send(
                    f'There is no such a command: `{text[0]}`. Type `{prefix.prefix}help` to learn more...')
        except IndexError:
            pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send("Greetings! Welcome to our server!")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        session = sessions["bot_serversettings"]

        server = Servers(id=guild.id, server_name=guild.name)
        prefix = Prefix(server_id=guild.id, prefix='!')
        channels = Channels(server_id=guild.id)

        session.add(prefix)
        session.add(server)
        session.add(channels)

        for role in guild.roles:
            roles = Roles(server_id=guild.id, roles_id=role.id)
            session.add(roles)
        session.commit()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload_roles(self, ctx):
        await ctx.channel.purge(limit=1)

        session = sessions["bot_serversettings"]

        channel_id_ = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first().settings_log

        for role in ctx.guild.roles:
            roles_id = [r.roles_id for r in session.query(Roles).filter(Roles.server_id == ctx.guild.id).all()]

            if role.id not in roles_id:
                roles = Roles(server_id=ctx.guild.id, roles_id=role.id)
                session.add(roles)

        session.commit()
        await self.client.get_channel(channel_id_).send(f"Roles were updated")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_mute_role(self, ctx, role_id: int):
        await ctx.channel.purge(limit=1)

        session = sessions["bot_serversettings"]
        channel_id_ = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first().settings_log

        channels = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first()

        channels.mute_role = role_id
        session.commit()

        role_name = discord.utils.get(ctx.guild.roles, id=role_id)
        await self.client.get_channel(channel_id_).send(f"Mute role was changed to `{role_name}`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_roles_message(self, ctx):
        """will be added soon"""
        pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_roles_message_settings(self, ctx):
        """will be added soon"""
        pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, prefix_: str):
        await ctx.channel.purge(limit=1)

        session = sessions["bot_serversettings"]
        prefix = session.query(Prefix).filter(
            Prefix.server_id == ctx.guild.id).first()
        channel_id_ = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first().settings_log

        if prefix.prefix == prefix_:
            await self.client.get_channel(channel_id_).send(
                f"Prefix is already `{prefix_}`")

        elif prefix.prefix != prefix_:
            await self.client.get_channel(channel_id_).send(
                f"Prefix changed to `{prefix_}`")
            prefix.prefix = prefix_
            session.commit()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_settings_log(self, ctx, channel_id: int):
        await ctx.channel.purge(limit=1)

        session = sessions["bot_serversettings"]
        channels = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first()
        channel_id_ = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first().settings_log

        if channels.settings_log == channel_id:
            channel_name = discord.utils.get(ctx.guild.channels, id=channel_id)

            await self.client.get_channel(channel_id_).send(
                f"Settings log channel is already `{channel_name}`")

        elif channels.settings_log != channel_id:
            channel_name = discord.utils.get(ctx.guild.channels, id=channel_id)

            await self.client.get_channel(channel_id_).send(
                f"Settings log channel changed to `{channel_name}`")
            channels.settings_log = channel_id
            session.commit()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_moderation_log(self, ctx, channel_id: int):
        await ctx.channel.purge(limit=1)

        session = sessions["bot_serversettings"]
        channels = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first()
        channel_id_ = session.query(Channels).filter(
            Channels.server_id == ctx.guild.id).first().settings_log

        if channels.moderation_log == channel_id:
            channel_name = discord.utils.get(ctx.guild.channels, id=channel_id)

            await self.client.get_channel(channel_id_).send(
                f"Moderation log channel is already `{channel_name}`")

        elif channels.moderation_log != channel_id:
            channel_name = discord.utils.get(ctx.guild.channels, id=channel_id)

            await self.client.get_channel(channel_id_).send(
                f"Moderation log channel changed to `{channel_name}`")
            channels.moderation_log = channel_id
            session.commit()


def setup(client):
    client.add_cog(Settings(client))
