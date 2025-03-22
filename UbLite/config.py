#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from telethon import TelegramClient
import json
import re
def config(key, default=None):
    return os.getenv(key, default)

config_main_path = os.path.expanduser("~/.ublite/config.json")
if not os.path.exists(config_main_path):
    raise FileNotFoundError(f"Config file not found at {config_main_path}. Please create it.")

with open(config_main_path, "r") as f:
    config_main = json.load(f)

api_id = config_main.get("API_ID")
api_hash = config_main.get("API_HASH")
owner_id = config_main.get("OWNER_ID")
session_name = config_main.get("SESSION_NAME")
prefixes = config_main.get("PREFIXES")

prefix_pattern = '(' + '|'.join(map(re.escape, prefixes)) + r')'
device_model = "UbLite"
app_version = "0.1.0"

client = TelegramClient(
    session_name,
    api_id,
    api_hash,
    device_model=device_model,
    app_version=app_version,
)

dl_time = 2 # success message delete timer
error_dl = 5 # error message delete timer
