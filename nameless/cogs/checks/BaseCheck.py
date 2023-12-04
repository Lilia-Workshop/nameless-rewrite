from collections.abc import Callable

import discord
from discord.ext import commands

__all__ = ["BaseCheck"]


class BaseCheck:
    """Base check class. Containing some useful decorators."""

    def __init__(self):
        pass

    @staticmethod
    def allow_display_in_help_message(check_fn: Callable[[commands.Context], bool]):
        """
        Bypasses command-specific checks.
        Note: this is a decorator for a check.
        """

        def pred(ctx: commands.Context) -> bool:
            return getattr(ctx, "invoked_with", "") == "help" or check_fn(ctx)

        return pred

    @staticmethod
    def require_intents(intents: list):
        """
        Require the bot to have specific intent(s).
        Note: this is a decorator for a command.
        """

        async def pred(ctx: commands.Context, /, **kwargs) -> bool:
            set_intents = ctx.bot.intents

            return all(set_intents.value & intent.flag == intent.flag for intent in intents)

        return pred

    @staticmethod
    def require_interaction_intents(intents: list):
        """
        Require the bot to have specific intent(s).
        Note: this is a decorator for an application command.
        """

        async def pred(interaction: discord.Interaction, /, **kwargs) -> bool:
            set_intents = interaction.client.intents

            return all(set_intents.value & intent.flag == intent.flag for intent in intents)

        return pred
