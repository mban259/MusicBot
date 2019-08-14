from types import TracebackType
from typing import List, Optional
import discord
from util import debug
from discord.ext import commands
import myHelpCommand
import reaction
import os
import sys

help_command: myHelpCommand.myHelpCommand = myHelpCommand.myHelpCommand()
bot: commands.Bot = commands.Bot(command_prefix="./takashi ", help_command=help_command)


def get_voice_client() -> discord.VoiceClient:
    global guild_id
    guild: discord.Guild = bot.get_guild(guild_id)
    cli: discord.VoiceClient = guild.voice_client
    return cli


@bot.event
async def on_ready():
    debug.info("Logged in as")
    debug.info(bot.user.name)
    debug.info(bot.user.id)
    debug.info("------")


def is_owner(user: discord.User) -> bool:
    global admin_id
    return user.id == admin_id


def is_member(user: discord.User) -> bool:
    global guild_id
    global role_id
    xpc: discord.Guild = bot.get_guild(guild_id)
    role: discord.Role = xpc.get_role(role_id)
    members: list[discord.User] = role.members
    for mem in members:
        member: discord.User = mem
        if member.id == user.id:
            return True
    return False


def has_permission(user: discord.User) -> bool:
    return is_owner(user) or is_member(user)


async def has_permission_check(ctx: commands.Context) -> bool:
    user: discord.User = ctx.author
    return has_permission(user)


@bot.command()
@commands.check(has_permission_check)
async def ping(ctx: commands.Context):
    await reaction.send_processing(ctx)
    await ctx.send("pong")
    await reaction.send_done(ctx)


@bot.command()
@commands.check(has_permission_check)
async def join(ctx: commands.Context):
    global vc_id
    await reaction.send_processing(ctx)
    channel: discord.VoiceChannel = bot.get_channel(vc_id)
    await channel.connect()
    await reaction.send_done(ctx)


@bot.command()
@commands.check(has_permission_check)
async def leave(ctx: commands.Context):
    await reaction.send_processing(ctx)
    cli: discord.VoiceClient = get_voice_client()
    await cli.disconnect()
    await reaction.send_done(ctx)


@bot.command()
@commands.check(has_permission_check)
async def start(ctx: commands.Context, name: str):
    await reaction.send_processing(ctx)
    cli: discord.VoiceClient = get_voice_client()
    if os.path.isfile("data/music/{}".format(name)):
        raise FileNotFoundError()
    cli.play(discord.FFmpegPCMAudio("data/music/{}".format(name)), after=lambda e: print(e))
    await reaction.send_done(ctx)


@bot.command()
@commands.check(has_permission_check)
async def stop(ctx: commands.Context):
    await reaction.send_processing(ctx)
    cli: discord.VoiceClient = get_voice_client()
    cli.stop()
    await reaction.send_done(ctx)


@bot.command()
@commands.check(has_permission_check)
async def pause(ctx: commands.Context):
    await reaction.send_processing(ctx)
    cli: discord.VoiceClient = get_voice_client()
    cli.pause()
    await reaction.send_done(ctx)


@bot.command()
@commands.check(has_permission_check)
async def resume(ctx: commands.Context):
    await reaction.send_processing(ctx)
    cli: discord.VoiceClient = get_voice_client()
    cli.resume()
    await reaction.send_done(ctx)


@bot.command()
@commands.check(has_permission_check)
async def list(ctx: commands.Context):
    await reaction.send_processing(ctx)
    files: List[str] = os.listdir("data/music/")
    await ctx.send("```" + "\n".join(files) + "```")
    await reaction.send_done(ctx)


@bot.command()
@commands.check(has_permission_check)
async def delete(ctx: commands.Context, filename: str):
    await reaction.send_processing(ctx)
    os.remove("data/music/{}".format(filename))
    await reaction.send_done(ctx)


def is_private(msg: discord.Message) -> bool:
    return msg.guild is None


@bot.event
async def on_message(msg: discord.Message):
    user: discord.User = msg.author
    if user.id == bot.user.id:
        return
    if is_private(msg) and has_permission(user):
        s_message: str = msg.content
        # debug.log(s_message == "")
        attachments: List[discord.Attachment] = msg.attachments
        if len(attachments) == 1:
            attachment: discord.Attachment = attachments[0]
            debug.info(attachment.filename)
            debug.info(attachment.id)
            debug.info(attachment.proxy_url)
            debug.info(attachment.size)
            debug.info(attachment.url)
            filename: str = attachment.filename if s_message == '' else s_message
            try:
                debug.info("download")
                await reaction.send_processing_msg(msg)
                await attachment.save(open("data/music/{0}".format(filename), "ab"))
                await reaction.send_done_msg(msg)
            except:
                await reaction.send_error_msg(msg)
    await bot.process_commands(msg)


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    await reaction.send_error(ctx, error)


if __name__ == '__main__':
    args = sys.argv
    global token
    global guild_id
    global vc_id
    global admin_id
    global role_id
    token = args[1]
    debug.info("token:{}".format(token))
    guild_id = int(args[2])
    debug.info("guild_id:{}".format(guild_id))
    vc_id = int(args[3])
    debug.info("vc_id:{}".format(vc_id))
    admin_id = int(args[4])
    debug.info("admin_id:{}".format(admin_id))
    role_id = int(args[5])
    debug.info("role_id:{}".format(role_id))
    bot.run(token)
