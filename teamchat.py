#!/data/data/com.termux/files/usr/bin/python3
# BLACK CYBER TEAM CHAT - Created by @BlackCyberx
# GitHub: https://github.com/BlackCyberx/teamchat

import os
import sys
import hashlib
import subprocess
import time
from datetime import datetime
from pathlib import Path

# ============ CONFIGURATION ============
GITHUB_REPO = "https://github.com/BlackCyberx/teamchat.git"
REPO_PATH = f"{Path.home()}/storage/downloads/teamchat"
KEY_FILE = f"{Path.home()}/.blackcyber_key"
ADMIN_KEY = "BLACKCYBER2025"
# ========================================

def clear_screen():
    os.system('clear')

def print_banner():
    clear_screen()
    print("""\033[1;32m
    ╔══════════════════════════════════════╗
    ║     🔥 BLACK CYBER TEAM CHAT 🔥      ║
    ║         Authorized Access Only       ║
    ║       Team Leader: @BlackCyberx      ║
    ║   https://github.com/BlackCyberx     ║
    ╚══════════════════════════════════════╝
    \033[0m""")

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def setup_git():
    """Configure git to avoid prompts"""
    run_cmd('git config --global user.name "BlackCyberx"')
    run_cmd('git config --global user.email "blackcyber@github.com"')
    run_cmd('git config --global pull.rebase false')
    run_cmd('git config --global credential.helper store')

def setup_repo():
    if not os.path.exists(REPO_PATH):
        print("\n[*] First time setup - Downloading team chat...")
        run_cmd(f"git clone {GITHUB_REPO} {REPO_PATH}")
    else:
        os.chdir(REPO_PATH)
        run_cmd("git pull")

def generate_device_key():
    android_id = subprocess.run("settings get secure android_id", shell=True, capture_output=True, text=True).stdout.strip()
    termux_version = subprocess.run("getprop ro.termux.version", shell=True, capture_output=True, text=True).stdout.strip()
    random_data = os.urandom(32).hex()
    unique_string = f"BLACKCYBER{android_id}{termux_version}{random_data}{time.time()}"
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

def check_approval(device_key):
    os.chdir(REPO_PATH)
    run_cmd("git pull")
    
    # Check if admin (BlackCyberx)
    if device_key == ADMIN_KEY:
        return True, "admin"
    
    # Check approved members
    if os.path.exists("approved_members.txt"):
        with open("approved_members.txt", 'r') as f:
            for line in f:
                if device_key in line and "ADMIN" not in line:
                    return True, "member"
    
    # Check if already pending
    if os.path.exists("pending_members.txt"):
        with open("pending_members.txt", 'r') as f:
            for line in f:
                if device_key in line:
                    return False, "pending"
    
    # New member - add to pending
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("pending_members.txt", 'a') as f:
        f.write(f"{device_key}|{timestamp}|WAITING|{device_key[:8]}\n")
    
    run_cmd("git add pending_members.txt")
    run_cmd(f'git commit -m "New join request: {device_key[:8]}"')
    run_cmd("git push")
    
    return False, "new"

def admin_panel():
    while True:
        print_banner()
        print("\033[1;33m╔══════════════════════════════════════╗")
        print("║     🔐 BLACK CYBER ADMIN PANEL     ║")
        print("╚══════════════════════════════════════╝\033[0m")
        print("\n\033[1;36m[ ADMIN: @BlackCyberx ]\033[0m\n")
        print("1.  👥  View Pending Requests")
        print("2.  ✅  Approve Member")
        print("3.  ❌  Remove Member")
        print("4.  📋  View All Team Members")
        print("5.  📢  Broadcast Message")
        print("6.  🗑️   Clear Chat History")
        print("7.  📊  Team Statistics")
        print("8.  💬  Open Team Chat")
        print("9.  🚪  Exit Admin Panel")
        
        choice = input("\n\033[1;32m[BlackCyber@Team]# \033[0m").strip()
        
        if choice == "1": view_pending()
        elif choice == "2": approve_member()
        elif choice == "3": remove_member()
        elif choice == "4": view_members()
        elif choice == "5": broadcast_message()
        elif choice == "6": clear_chat()
        elif choice == "7": team_stats()
        elif choice == "8": chat_interface("admin")
        elif choice == "9": break

def view_pending():
    os.chdir(REPO_PATH)
    run_cmd("git pull")
    
    print("\n\033[1;33m📋 PENDING APPROVAL REQUESTS:\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    if os.path.exists("pending_members.txt"):
        with open("pending_members.txt", 'r') as f:
            requests = [line for line in f if "WAITING" in line]
        
        if requests:
            for i, req in enumerate(requests, 1):
                parts = req.strip().split('|')
                print(f"{i}.  🔑 Key: {parts[3]}")
                print(f"    📅 Requested: {parts[1]}")
                print(f"    🆔 Full ID: {parts[0][:16]}...\n")
        else:
            print("No pending requests.")
    
    input("\nPress Enter to continue...")

def approve_member():
    os.chdir(REPO_PATH)
    run_cmd("git pull")
    
    view_pending()
    
    choice = input("\nEnter member number to approve: ").strip()
    
    if choice.isdigit():
        with open("pending_members.txt", 'r') as f:
            requests = f.readlines()
        
        pending_list = [r for r in requests if "WAITING" in r]
        idx = int(choice) - 1
        
        if 0 <= idx < len(pending_list):
            selected = pending_list[idx]
            parts = selected.strip().split('|')
            device_key = parts[0]
            member_id = parts[3]
            
            # Add to approved members
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("approved_members.txt", 'a') as f:
                f.write(f"{device_key}|{timestamp}|ACTIVE|MEMBER|Approved_by_BlackCyberx\n")
            
            # Remove from pending
            requests.remove(selected)
            with open("pending_members.txt", 'w') as f:
                f.writelines(requests)
            
            # Log approval
            with open("messages.txt", 'a') as f:
                f.write(f"\n[SYSTEM {timestamp}] ✅ Member {member_id} approved by @BlackCyberx\n")
            
            run_cmd("git add approved_members.txt pending_members.txt messages.txt")
            run_cmd(f'git commit -m "Approved member: {member_id} by BlackCyberx"')
            run_cmd("git push")
            
            print(f"\n✅ Member {member_id} approved successfully!")
    
    input("\nPress Enter to continue...")

def view_members():
    os.chdir(REPO_PATH)
    run_cmd("git pull")
    
    print("\n\033[1;32m👥 BLACK CYBER TEAM MEMBERS:\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    print("\033[1;33m👑 TEAM LEADER: @BlackCyberx (ADMIN)\033[0m\n")
    
    if os.path.exists("approved_members.txt"):
        with open("approved_members.txt", 'r') as f:
            members = f.readlines()
        
        active = [m for m in members if "ACTIVE" in m and "ADMIN" not in m]
        
        if active:
            for i, member in enumerate(active, 1):
                parts = member.strip().split('|')
                print(f"{i}.  🎖️  Member ID: {parts[3]}")
                print(f"    📅 Joined: {parts[1]}")
                print(f"    🔑 Key: {parts[0][:16]}...\n")
        else:
            print("No active team members yet.")
    
    input("\nPress Enter to continue...")

def broadcast_message():
    print("\n\033[1;33m📢 ADMIN BROADCAST\033[0m")
    message = input("Message to team: ").strip()
    
    if message:
        os.chdir(REPO_PATH)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("messages.txt", 'a') as f:
            f.write(f"\n[📢 ADMIN BROADCAST - {timestamp}]\n")
            f.write(f"[👑 @BlackCyberx] 🔥 {message}\n")
            f.write("─" * 50 + "\n")
        
        run_cmd("git add messages.txt")
        run_cmd(f'git commit -m "Admin broadcast by BlackCyberx"')
        run_cmd("git push")
        
        print("\n✅ Broadcast sent to all team members!")
    
    input("\nPress Enter to continue...")

def clear_chat():
    print("\n\033[1;31m⚠️  WARNING: This will delete ALL chat history!\033[0m")
    confirm = input("Type 'CLEAR' to confirm: ").strip()
    
    if confirm == "CLEAR":
        os.chdir(REPO_PATH)
        
        with open("messages.txt", 'w') as f:
            f.write("========================================\n")
            f.write("🔥 BLACK CYBER TEAM CHAT 🔥\n")
            f.write("========================================\n")
            f.write(f"Team Leader: @BlackCyberx\n")
            f.write(f"Chat cleared on: {datetime.now()}\n")
            f.write("========================================\n\n")
        
        run_cmd("git add messages.txt")
        run_cmd(f'git commit -m "Chat cleared by Admin BlackCyberx"')
        run_cmd("git push")
        
        print("\n✅ Chat history cleared!")
    
    input("\nPress Enter to continue...")

def team_stats():
    os.chdir(REPO_PATH)
    run_cmd("git pull")
    
    print("\n\033[1;35m📊 TEAM STATISTICS\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    member_count = 0
    if os.path.exists("approved_members.txt"):
        with open("approved_members.txt", 'r') as f:
            member_count = len([l for l in f if "ACTIVE" in l and "ADMIN" not in l])
    
    message_count = 0
    if os.path.exists("messages.txt"):
        with open("messages.txt", 'r') as f:
            message_count = len(f.readlines())
    
    pending_count = 0
    if os.path.exists("pending_members.txt"):
        with open("pending_members.txt", 'r') as f:
            pending_count = len([l for l in f if "WAITING" in l])
    
    print(f"👑 Team Leader: @BlackCyberx")
    print(f"👥 Active Members: {member_count}")
    print(f"⏳ Pending Requests: {pending_count}")
    print(f"💬 Total Messages: {message_count}")
    print(f"📁 Repository: https://github.com/BlackCyberx/teamchat")
    
    input("\nPress Enter to continue...")

def chat_interface(user_type):
    username = "👑 BlackCyberx" if user_type == "admin" else f"🎖️ Member-{get_device_key()[:8]}"
    
    while True:
        print_banner()
        print(f"\n\033[1;34m💬 TEAM CHAT - {username}\033[0m\n")
        print("1.  📖  Read Messages")
        print("2.  💬  Send Message")
        print("3.  🔄  Refresh")
        print("4.  🔙  Back to Main Menu")
        
        choice = input("\n[TeamChat]# ").strip()
        
        if choice == "1":
            os.chdir(REPO_PATH)
            run_cmd("git pull")
            
            print("\n\033[1;36m" + "="*60)
            print("📝 LATEST MESSAGES")
            print("="*60 + "\033[0m")
            
            if os.path.exists("messages.txt"):
                with open("messages.txt", 'r') as f:
                    lines = f.readlines()[-30:]
                    for line in lines:
                        print(line.strip())
            
            input("\nPress Enter to continue...")
        
        elif choice == "2":
            message = input("\n💬 Message: ").strip()
            
            if message:
                os.chdir(REPO_PATH)
                timestamp = datetime.now().strftime("%H:%M:%S")
                date = datetime.now().strftime("%Y-%m-%d")
                
                with open("messages.txt", 'a') as f:
                    f.write(f"[{date} {timestamp}] {username}: {message}\n")
                
                run_cmd("git add messages.txt")
                run_cmd(f'git commit -m "Message from {username}"')
                run_cmd("git push")
                
                print("✅ Message sent!")
                time.sleep(1)
        
        elif choice == "3":
            continue
        elif choice == "4":
            break

def main():
    print_banner()
    setup_git()
    setup_repo()
    device_key = get_device_key()
    status, status_type = check_approval(device_key)
    
    if status_type == "admin":
        print("\n\033[1;32m✅ WELCOME BACK TEAM LEADER BLACK CYBER!\033[0m")
        time.sleep(2)
        admin_panel()
    elif status:
        print("\n\033[1;32m✅ ACCESS GRANTED! Welcome to Black Cyber Team!\033[0m")
        time.sleep(2)
        chat_interface("member")
    else:
        if status_type == "pending":
            print("\n\033[1;33m⏳ YOUR REQUEST IS PENDING ADMIN APPROVAL\033[0m")
        else:
            print("\n\033[1;33m📨 APPROVAL REQUEST SENT TO @BlackCyberx!\033[0m")
        
        print(f"\n\033[1;36m🔑 YOUR DEVICE KEY:\033[0m")
        print(f"\033[1;33m{device_key}\033[0m")
        print(f"\n📌 Send this key to @BlackCyberx on GitHub")
        print(f"🔗 https://github.com/BlackCyberx")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Exiting Black Cyber Team Chat...")
        sys.exit(0)
