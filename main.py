#!/usr/bin/env python3
"""
Pollinations.ai Prompt Enhancer

A secure, robust GUI application for enhancing text prompts using the Pollinations.ai API,
featuring a dynamic UI with categorical enhancement based on an external JSON file.

Author: Enhanced by AI Assistant
Version: 2.5.0 (External JSON Prompts and Dynamic UI)
License: MIT
"""

import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
from pathlib import Path

from config.config_manager import ConfigManager
from utils.logger import Logger
from core.gui import PromptEnhancerGUI

# Try to import dotenv, provide instructions if it is missing
try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: The 'python-dotenv' library is required.")
    print("Please install it using: pip install python-dotenv")
    sys.exit(1)

def main():
    """Main function to set up and run the application."""
    script_dir = Path(__file__).parent
    dotenv_path = script_dir / '.env'
    if not dotenv_path.exists():
        root_msg = tk.Tk()
        root_msg.withdraw()
        messagebox.showerror("Configuration Error",
                             "'.env' file not found.\n\nPlease create a '.env' file with your token.")
        root_msg.destroy()
        return
    load_dotenv(dotenv_path=dotenv_path)
    api_token = os.getenv("API_TOKEN")
    if not api_token or api_token == "your-api-token":
        root_msg = tk.Tk()
        root_msg.withdraw()
        messagebox.showerror("Configuration Error",
                             "API_TOKEN not found or not set in the .env file.\n\nPlease create a '.env' file with your token.")
        root_msg.destroy()
        return


    # Load prompts from the JSON file
    prompts_path = script_dir / "config" / "prompts.json"
    if not prompts_path.exists():
        root_msg = tk.Tk()
        root_msg.withdraw()
        messagebox.showerror(
            "File Error", "The file 'prompts.json' was not found.\nMake sure the file is in the same directory as the script.")
        root_msg.destroy()
        return

    try:
        with open(prompts_path, 'r', encoding='utf-8') as f:
            prompts_data = json.load(f).get("prompts", {})
        if not prompts_data:
            raise ValueError(
                "The JSON file is empty or does not have the 'prompts' key.")
    except (json.JSONDecodeError, ValueError) as e:
        root_msg = tk.Tk()
        root_msg.withdraw()
        messagebox.showerror(
            "JSON Error", f"Error reading or processing 'prompts.json':\n\n{e}")
        root_msg.destroy()
        return

    config = ConfigManager()
    logger = Logger.setup_logger("PromptEnhancer")

    try:
        app = PromptEnhancerGUI(config, logger, api_token, prompts_data)
        app.run()
    except Exception as e:
        logger.critical(f"A critical error occurred: {e}", exc_info=True)
        root_msg = tk.Tk()
        root_msg.withdraw()
        messagebox.showerror(
            "Fatal Error", f"A critical error occurred and the application must close:\n\n{e}")
        root_msg.destroy()


if __name__ == "__main__":
    main()
