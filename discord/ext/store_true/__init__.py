import copy

from typing import TypeVar, Type

import discord
from discord.ext import commands

import re


__version__ = '1.0.0'


C = TypeVar("C", bound=commands.Context)


class StoreTrueMixin:

    __slots__ = ()

    async def get_context(
        self, message: discord.Message, *, cls: Type[C] = commands.Context
    ) -> C:
        ctx = await super().get_context(message, cls=cls)  # type: ignore

        if ctx.command is None:
            return ctx

        assert isinstance(ctx.command, commands.Command)

        for param in ctx.command.clean_params.values():
            converter = commands.core.get_converter(param)

            if hasattr(converter, "__commands_is_flag__"):
                flags = converter
                break
        else:
            return ctx

        assert issubclass(flags, commands.FlagConverter)
        prefix = flags.__commands_flag_prefix__

        message = copy.copy(message)

        message.content = re.sub(
            rf"{prefix}([^\s]+)(?=(\s{prefix})|$)",
            rf"{prefix}\1 true",
            message.content,
        )

        return await super().get_context(message, cls=cls)  # type: ignore
