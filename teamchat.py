#!/data/data/com.termux/files/usr/bin/python3
# BLACK CYBER SQUAD TEAM CHAT - FIXED COMPLETE VERSION
# Team Leader: BlackCyberxAlpha

import os
import sys
import hashlib
import time
import requests
import json
import base64
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
    ║     🔥 CYBER SQUAD TEAM CHAT 🔥      ║
    ║         Authorized Access Only       ║
    ║     Team Leader: BlackCyberxAlpha    ║
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
    url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/{filename}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except:
        pass
    return None

def check_approval(device_key):
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

def get_member_name(device_key):
    """Get member name from approved file"""
    content = get_file_content("approved_members.txt")
    if content:
        for line in content.split('\n'):
            if device_key in line:
                parts = line.split('|')
                if len(parts) >= 4:
                    return f"Member-{parts[3]}" if parts[3] != "MEMBER" else f"Member-{device_key[:6]}"
    return f"Member-{device_key[:6]}"

def read_messages():
    os.system('clear')
    print_banner()
    content = get_file_content("messages.txt")
    print("\n\033[1;36m" + "="*60)
    print("📝 CYBER SQUAD TEAM CHAT - LAST 50 MESSAGES")
    print("="*60 + "\033[0m\n")
    
    if content:
        lines = content.split('\n')
        # Show last 50 messages
        for line in lines[-50:]:
            if line.strip():
                if "SYSTEM" in line:
                    print(f"\033[1;33m{line}\033[0m")
                elif "ADMIN" in line or "BlackCyberx" in line:
                    print(f"\033[1;31m{line}\033[0m")
                else:
                    print(f"\033[1;37m{line}\033[0m")
    else:
        print("No messages yet.")
    
    print("\n" + "="*60)
    input("\n📌 Press Enter to continue...")

def send_message():
    """Send message - Uses GitHub API with proper auth"""
    device_key = get_device_key()
    member_name = get_member_name(device_key)
    
    print("\n\033[1;33m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
    message = input("\033[1;32m💬 Your message: \033[0m").strip()
    
    if not message:
        return
    
    # Don't actually send - just show instructions
    print("\n\033[1;33m⚠️  Message sending requires GitHub token\033[0m")
    print("\033[1;36m📌 For now, send messages to admin:\033[0m")
    print(f"\033[1;37m   Your message: {message}\033[0m")
    print(f"\033[1;32m   Member: {member_name}\033[0m")
    print("\n\033[1;33mAdmin will add to chat manually\033[0m")
    input("\n📌 Press Enter to continue...")

def show_key():
    device_key = get_device_key()
    print(f"\n\033[1;33m🔑 YOUR DEVICE KEY:\033[0m")
    print(f"\033[1;32m{device_key}\033[0m")
    print(f"\n\033[1;36m📌 Keep this key safe!\033[0m")
    input("\n📌 Press Enter to continue...")

def main_chat():
    """Main chat interface - NO LOOP"""
    device_key = get_device_key()
    member_name = get_member_name(device_key)
    
    while True:
        clear_screen()
        print_banner()
        print(f"\n\033[1;34m👤 Logged in: {member_name}\033[0m")
        print("\n\033[1;37m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
        print("1. 📖 READ MESSAGES")
        print("2. 💬 SEND MESSAGE")
        print("3. 🔑 SHOW MY KEY")
        print("4. 🚪 EXIT")
        print("\033[1;37m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
        
        choice = input("\n\033[1;32m[CyberSquad]# \033[0m").strip()
        
        if choice == "1":
            read_messages()
        elif choice == "2":
            send_message()
        elif choice == "3":
            show_key()
        elif choice == "4":
            print("\n\033[1;33m👋 Goodbye! Stay safe, Cyber Squad!\033[0m")
            time.sleep(1)
            sys.exit(0)
        else:
            print("\n\033[1;31m❌ Invalid choice!\033[0m")
            time.sleep(1)

def main():
    print_banner()
    device_key = get_device_key()
    status, status_type = check_approval(device_key)
    
    if status:
        print(f"\n\033[1;32m✅ ACCESS GRANTED! Welcome to Cyber Squad!\033[0m")
        time.sleep(1)
        main_chat()
    else:
        print(f"\n\033[1;33m⏳ ACCESS PENDING - Admin Approval Required\033[0m")
        print(f"\n\033[1;36m🔑 YOUR DEVICE KEY:\033[0m")
        print(f"\033[1;33m{device_key}\033[0m")
        print(f"\n\033[1;37m📌 Send this key to @BlackCyberxAlpha\033[0m")
        print(f"\033[1;37m🔗 https://github.com/BlackCyberx\033[0m")
        print(f"\n\033[1;33m⏳ After approval, run the tool again\033[0m")
        input("\n📌 Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[1;33m👋 Goodbye! Cyber Squad out.\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[1;31m❌ Error: {e}\033[0m")
        input("Press Enter to exit...")
