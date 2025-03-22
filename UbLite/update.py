#!/usr/bin/env python
# -*- coding: utf-8 -*-
# UbLite/update.py
import os
import sys
import subprocess

def update_ublite():
    """Function to upgrade UbLite via pip."""
    try:
        print("Starting the update process for UbLite...")

        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "UbLite"])

        print("UbLite has been successfully updated!")
    except subprocess.CalledProcessError as e:
        print(f"Error during the update process: {e}")
        sys.exit(1)

def main():
    """Main entry point for the update process."""
    update_ublite()
