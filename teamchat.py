#!/data/data/com.termux/files/usr/bin/python3
# BLACK CYBER TEAM CHAT - MEMBER FRIENDLY VERSION
# Team Leader: @BlackCyberx

import os
import sys
import hashlib
import time
import requests
from datetime import datetime
from pathlib import Path

# ============ CONFIGURATION ============
OWNER = "BlackCyberx"
REPO = "teamchat"
BRANCH = "main"
KEY_FILE = f"{Path.home()}/.blackcyber_key"
ADMIN_KEY = "BLACKCYBER2025"
# ========================================

def clear_screen():
    os.system('clear')

def print_banner():
    clear_screen()
    print("""\033[1;32m
    ╔══════════════════════════════════════╗
    ║     🔥  CYBER Squad TEAM CHAT 🔥     ║
    ║         Authorized Access Only       ║
    ║       Team Leader: BlackCyberxAlpha  
    ║   https://github.com/BlackCyberx     ║
    ╚══════════════════════════════════════╝
    \033[0m""")

def generate_device_key():
    android_id = "unknown"
    try:
        import subprocess
        android_id = subprocess.run("settings get secure android_id", shell=True, capture_output=True, text=True).stdout.strip()
    except:
        pass
    random_data = os.urandom(32).hex()
    unique_string = f"BLACKCYBER{android_id}{random_data}{time.time()}"
    device_key = hashlib.sha256(unique_string.encode()).hexdigest()
    
    with open(KEY_FILE, 'w') as f:
        f.write(device_key)
    return device_key

def get_device_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            return f.read().strip()
    else:
        return generate_device_key()

def get_file_content(filename):
    """Get file from GitHub - NO LOGIN NEEDED"""
    url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/{filename}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except:
        pass
    return None

def check_approval(device_key):
    """Check if approved - READ ONLY"""
    content = get_file_content("approved_members.txt")
    if content:
        if device_key == ADMIN_KEY:
            return True, "admin"
        if device_key in content:
            return True, "member"
    
    content = get_file_content("pending_members.txt")
    if content and device_key in content:
        return False, "pending"
    
    return False, "new"

def show_instructions():
    """Show key and instructions"""
    device_key = get_device_key()
    print(f"\n\033[1;33m🔑 YOUR DEVICE KEY:\033[0m")
    print(f"\033[1;32m{device_key}\033[0m")
    print(f"\n\033[1;36m📌 Send this key to @BlackCyberx on GitHub\033[0m")
    print(f"\033[1;36m🔗 https://github.com/BlackCyberx\033[0m")
    print(f"\n\033[1;33m⏳ After approval, run the tool again\033[0m")

def read_messages():
    """Read chat - NO LOGIN NEEDED"""
    content = get_file_content("messages.txt")
    print("\n\033[1;36m" + "="*60)
    print("📝 BLACK CYBER TEAM CHAT")
    print("="*60 + "\033[0m\n")
    if content:
        lines = content.split('\n')[-30:]
        for line in lines:
            print(line)
    else:
        print("No messages yet.")
    input("\nPress Enter to continue...")

def main():
    print_banner()
    device_key = get_device_key()
    status, status_type = check_approval(device_key)
    
    if status_type == "admin":
        print("\n\033[1;32m✅ WELCOME BACK TEAM LEADER!\033[0m")
        print("\033[1;33m📍 Admin Panel is on GitHub:\033[0m")
        print("\033[1;34mhttps://github.com/BlackCyberx/teamchat\033[0m")
        show_instructions()
        
    elif status:
        print("\n\033[1;32m✅ ACCESS GRANTED! Welcome to Black Cyber Team!\033[0m")
        while True:
            print("\n1. 📖 Read Messages")
            print("2. 🔑 Show My Key")
            print("3. 🚪 Exit")
            choice = input("\n[TeamChat]# ").strip()
            if choice == "1":
                read_messages()
            elif choice == "2":
                show_instructions()
            elif choice == "3":
                break
    else:
        print("\n\033[1;33m⏳ ACCESS PENDING - Admin Approval Required\033[0m")
        show_instructions()
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Exiting...")
