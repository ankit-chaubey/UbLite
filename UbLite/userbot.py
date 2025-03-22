#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import importlib

try:
    from .config import client
except ImportError:
    from config import client

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

async def start_bot():
    """Starts the userbot and loads necessary modules."""
    ublite_path = os.path.dirname(os.path.abspath(__file__))

    for file in os.listdir(ublite_path):
        if file.endswith(".py") and file not in ("__init__.py", "config.py", "setup_config.py"):
            module_name = f"UbLite.{file[:-3]}"
            importlib.import_module(module_name)

    print("UbLite Userbot is running...")
    await client.start()
    await client.run_until_disconnected()

def main():
    """Entry point for the script."""
    import asyncio
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("\nUserbot stopped by user.")

if __name__ == "__main__":
    main()
