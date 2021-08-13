import copy

from typing import Any, ClassVar, TypeVar, Type

import discord
from discord.ext import commands

import re


__version__ = "1.0.2"


C = TypeVar("C", bound=commands.Context)


class StoreTrueMixin:
    _STORE_TRUE_FLAG_REGEX: ClassVar[str] = r"{0}([^\s]+)(?=(\s{0}[^\s]+)|$)"

    __slots__ = ()

    async def get_context(
        self,
        message: discord.Message,
        *args: Any,
        cls: Type[C] = commands.Context,
        **kwargs: Any,
    ) -> C:
        ctx = await super().get_context(message, *args, cls=cls, **kwargs)  # type: ignore

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

        # add support for `-foo` shortcut
        if prefix == "--":
            prefix = r"--?"
        else:
            prefix = re.escape(prefix)

        message = copy.copy(message)

        message.content = re.sub(
            self._STORE_TRUE_FLAG_REGEX.format(prefix),
            rf"{prefix if prefix != r'--?' else '--'}\1 true",
            message.content,
        )

        return await super().get_context(message, *args, cls=cls, **kwargs)  # type: ignore
