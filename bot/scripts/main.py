#!/usr/bin/env python3
import asyncio
import sys
import logging
from bot.src.bot import start


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())


if __name__ == "__main__":
    main()
