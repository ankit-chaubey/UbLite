#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import re
from colorama import Fore, init

init(autoreset=True)

config_path = os.path.expanduser("~/.ublite/config.json")

def load_config():
    """Load existing configuration file if it exists."""
    if not os.path.exists(config_path):
        print(f"{Fore.RED}⚠ Config file not found at {Fore.YELLOW}{config_path}{Fore.RED}.")
        return None
    with open(config_path, "r") as f:
        return json.load(f)

def save_config(config_data):
    """Save configuration while keeping 'PREFIXES' in a single line."""
    json_str = json.dumps(config_data, indent=4, ensure_ascii=False)
    json_str = re.sub(r'(\s*"PREFIXES": \n\s*)', '"PREFIXES": [', json_str)
    json_str = re.sub(r'(\n\s*)', ']', json_str)

    with open(config_path, "w") as f:
        f.write(json_str)

def setup_config():
    """Setup or modify the configuration file interactively."""
    print(f"{Fore.LIGHTCYAN_EX}🚀 Setting up UbLite configuration...\n")

    api_id = input(f"{Fore.GREEN}Enter API_ID: {Fore.YELLOW}").strip()
    api_hash = input(f"{Fore.GREEN}Enter API_HASH: {Fore.YELLOW}").strip()
    owner_id = input(f"{Fore.GREEN}Enter OWNER_ID (default: 93602376): {Fore.YELLOW}").strip() or "93602376"
    session_name = input(f"{Fore.GREEN}Enter SESSION_NAME (default: UbLite): {Fore.YELLOW}").strip() or "UbLite"

    handler = input(f"{Fore.GREEN}Enter command prefixes (default: . - !): {Fore.YELLOW}").strip()
    prefixes = handler.split() if handler else [".", "-", "!"]

    config_data = {
        "API_ID": api_id,
        "API_HASH": api_hash,
        "OWNER_ID": int(owner_id),
        "SESSION_NAME": session_name,
        "PREFIXES": prefixes
    }

    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    save_config(config_data)

    print(f"\n{Fore.GREEN}✔ Configuration saved successfully!")
    print(f"\n{Fore.GREEN}✔ Setup complete! You can now use UbLite.")

def edit_config():
    """Edit existing config values."""
    config = load_config()
    if not config:
        print(f"{Fore.RED}⚠ No existing configuration found. Run setup first!")
        return
    
    print(f"\n{Fore.LIGHTCYAN_EX}🔧 Editing existing UbLite configuration...\n")
    
    config["API_ID"] = input(f"{Fore.GREEN}Enter API_ID [{config['API_ID']}]: {Fore.YELLOW}").strip() or config["API_ID"]
    config["API_HASH"] = input(f"{Fore.GREEN}Enter API_HASH [{config['API_HASH']}]: {Fore.YELLOW}").strip() or config["API_HASH"]
    config["OWNER_ID"] = int(input(f"{Fore.GREEN}Enter OWNER_ID [{config['OWNER_ID']}]: {Fore.YELLOW}").strip() or config["OWNER_ID"])
    config["SESSION_NAME"] = input(f"{Fore.GREEN}Enter SESSION_NAME [{config['SESSION_NAME']}]: {Fore.YELLOW}").strip() or config["SESSION_NAME"]

    handler = input(f"{Fore.GREEN}Enter command prefixes (current: {' '.join(config['PREFIXES'])}): {Fore.YELLOW}").strip()
    config["PREFIXES"] = handler.split() if handler else config["PREFIXES"]

    save_config(config)

    print(f"\n{Fore.GREEN}✔ Configuration updated successfully!")

def main():
    """Main menu to setup or edit configuration."""
    print(f"{Fore.CYAN}================= {Fore.LIGHTMAGENTA_EX}UbLite Configuration {Fore.CYAN}=================")
    print(f"{Fore.GREEN}Press {Fore.YELLOW}c {Fore.GREEN}to set up a new configuration.")
    print(f"{Fore.GREEN}Press {Fore.YELLOW}e {Fore.GREEN}to edit the existing configuration.")
    print(f"{Fore.GREEN}Press {Fore.YELLOW}n {Fore.GREEN}or {Fore.YELLOW}Enter {Fore.GREEN}to skip setup and exit.")
    print(f"{Fore.CYAN}=================================================================")

    choice = input(f"{Fore.LIGHTCYAN_EX}Enter your choice: {Fore.YELLOW}").strip().lower()

    if choice == "c":
        setup_config()
    elif choice == "e":
        edit_config()
    else:
        print(f"{Fore.RED}⚠ Skipping setup. Exiting...\n")

if __name__ == "__main__":
    main()
