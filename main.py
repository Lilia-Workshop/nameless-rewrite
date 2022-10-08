import logging
import sys
from typing import List

import discord
from discord.ext import commands

import NamelessConfig
from nameless import Nameless, shared_vars

UPDATE_CHECK_FLAG = "--allow-updates-check"
CONFIG_CLASS_FLAG = "--config-class"


def main(args: List[str]):
    cls_arg = [arg for arg in args if arg.startswith(f"{CONFIG_CLASS_FLAG}=")]

    if cls_arg:
        try:
            cfg = __import__(cls_arg[0][len(f"{CONFIG_CLASS_FLAG}="):]).NamelessConfig
        except (ValueError, ModuleNotFoundError):
            cfg = NamelessConfig.NamelessConfig
            logging.warning("Invalid value for config class flag, NamelessConfig.NamelessConfig will be used")
    else:
        cfg = NamelessConfig.NamelessConfig

    shared_vars.config_cls = cfg
    prefixes = getattr(cfg, "PREFIXES", [])
    allow_mention = getattr(cfg, "RECEIVE_MENTION_PREFIX", False)

    intents = discord.Intents.default()
    intents.message_content = getattr(cfg, "RECEIVE_TEXTS", False)
    intents.members = getattr(cfg, "RECEIVE_MEMBER_EVENTS", False)

    nameless = Nameless(
        config_cls=cfg,
        intents=intents,
        command_prefix=commands.when_mentioned_or(*prefixes) if allow_mention else prefixes,
        allow_updates_check=UPDATE_CHECK_FLAG in args,
        description=getattr(cfg, "META", {}).get("bot_description", ""),
    )

    nameless.start_bot()


if __name__ == "__main__":
    main(sys.argv)
