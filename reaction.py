from types import TracebackType, FrameType
from typing import Optional, List

from discord.ext import commands
import discord
from util import debug
import traceback


async def send_processing(ctx: commands.Context):
    msg: discord.Message = ctx.message
    user = discord.User = ctx.author
    debug.info(
        "command:\"{}\" id:{} user:{}:{}".format(msg.content, msg.id, user.name, user.id))
    await msg.add_reaction("⏳")


async def send_processing_msg(msg: discord.Message):
    await msg.add_reaction("⏳")


async def send_done(ctx: commands.Context):
    msg: discord.Message = ctx.message
    debug.info('done')
    await msg.add_reaction("✅")


async def send_done_msg(msg: discord.Message):
    await msg.add_reaction("✅")


async def send_error(ctx: commands.Context, error: commands.CommandError):
    msg: discord.Message = ctx.message
    debug.error("".join(traceback.format_exception(type(error), error, error.__traceback__)))
    await msg.add_reaction("❌")


async def send_error_msg(msg: discord.Message):
    debug.error(traceback.format_exc())
    await msg.add_reaction("❌")
