#!/data/data/com.termux/files/usr/bin/python3
# TeamChat - Termux Team Communication Tool
# Created for Black Cyber & Team
# GitHub: https://github.com/BlackCyberx

import os
import sys
import hashlib
import subprocess
import time
import json
from datetime import datetime
from pathlib import Path

# ============ CONFIGURATION ============
GITHUB_REPO = "https://github.com/BlackCyberx/teamchat"
REPO_PATH = f"{Path.home()}/storage/downloads/teamchat"
KEY_FILE = f"{Path.home()}/.teamchat_key"
CONFIG_FILE = f"{Path.home()}/.teamchat_config"
ADMIN_KEY = "BLACKCYBER2025"  # Master admin key
# ========================================

def clear_screen():
    """Clear terminal screen"""
    os.system('clear')

def print_banner():
    """Display team banner"""
    clear_screen()
    print("""\033[1;32m
    ╔══════════════════════════════════════╗
    ║     🔥 BLACK CYBER TEAM CHAT 🔥      ║
    ║         Authorized Access Only       ║
    ║       Team Leader: @BlackCyberx      ║
    ╚══════════════════════════════════════╝
    \033[0m""")

def run_cmd(cmd):
    """Run shell command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def setup_termux():
    """Install required packages"""
    print("[*] Setting up Termux environment...")
    packages = ["git", "python", "openssh", "termux-api"]
    for pkg in packages:
        print(f"[*] Installing {pkg}...")
        run_cmd(f"pkg install -y {pkg}")

def setup_repo():
    """Clone or pull repository"""
    if not os.path.exists(REPO_PATH):
        print("\n[*] First time setup - Creating team chat environment...")
        run_cmd(f"git clone {GITHUB_REPO} {REPO_PATH}")
    else:
        print("\n[*] Updating team chat...")
        os.chdir(REPO_PATH)
        run_cmd("git pull")

def generate_device_key():
    """Generate unique device key for team member"""
    # Collect device information
    android_id = subprocess.run("settings get secure android_id", shell=True, capture_output=True, text=True).stdout.strip()
    termux_version = subprocess.run("getprop ro.termux.version", shell=True, capture_output=True, text=True).stdout.strip()
    hostname = subprocess.run("hostname", shell=True, capture_output=True, text=True).stdout.strip()
    random_data = os.urandom(64).hex()
    timestamp = str(time.time())
    
    # Generate unique team member key
    unique_string = f"BLACKCYBER{android_id}{termux_version}{hostname}{random_data}{timestamp}"
    device_key = hashlib.sha256(unique_string.encode()).hexdigest()
    
    # Save key
    with open(KEY_FILE, 'w') as f:
        f.write(device_key)
    
    return device_key

def get_device_key():
    """Get existing key or generate new one"""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            return f.read().strip()
    else:
        return generate_device_key()

def check_approval(device_key):
    """Check if team member is approved"""
    os.chdir(REPO_PATH)
    
    # Pull latest team roster
    run_cmd("git pull")
    
    # Check if admin (Black Cyber)
    if device_key == ADMIN_KEY:
        return True, "admin"
    
    # Check approved members
    if os.path.exists("approved_members.txt"):
        with open("approved_members.txt", 'r') as f:
            for line in f:
                if device_key in line:
                    return True, "member"
    
    # Check pending requests
    if os.path.exists("pending_members.txt"):
        with open("pending_members.txt", 'r') as f:
            for line in f:
                if device_key in line:
                    return False, "pending"
    
    # New member - add to pending
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("pending_members.txt", 'a') as f:
        f.write(f"{device_key}|{timestamp}|PENDING|NEW_MEMBER\n")
    
    # Commit pending request
    run_cmd("git add pending_members.txt")
    run_cmd(f'git commit -m "New team member request: {device_key[:16]}"')
    run_cmd("git push")
    
    return False, "new"

def admin_panel():
    """Black Cyber admin control panel"""
    while True:
        print_banner()
        print("\n\033[1;33m🔐 BLACK CYBER ADMIN PANEL 🔐\033[0m")
        print("\n1. View pending member requests")
        print("2. Approve member")
        print("3. Remove member")
        print("4. View all team members")
        print("5. Broadcast message to team")
        print("6. Clear chat history")
        print("7. View team statistics")
        print("8. Exit admin panel")
        
        choice = input("\n[BlackCyber@Team]# ").strip()
        
        if choice == "1":
            view_pending_requests()
        elif choice == "2":
            approve_member()
        elif choice == "3":
            remove_member()
        elif choice == "4":
            view_all_members()
        elif choice == "5":
            broadcast_message()
        elif choice == "6":
            clear_chat_history()
        elif choice == "7":
            view_statistics()
        elif choice == "8":
            break
        else:
            input("Invalid option! Press Enter to continue...")

def view_pending_requests():
    """View all pending approval requests"""
    os.chdir(REPO_PATH)
    run_cmd("git pull")
    
    print("\n\033[1;33m📋 PENDING TEAM MEMBER REQUESTS:\033[0m\n")
    if os.path.exists("pending_members.txt"):
        with open("pending_members.txt", 'r') as f:
            requests = f.readlines()
        
        if requests:
            for i, req in enumerate(requests, 1):
                parts = req.strip().split('|')
                key = parts[0][:16] + "..."
                date = parts[1] if len(parts) > 1 else "Unknown"
                print(f"{i}. Key: {key} | Requested: {date}")
        else:
            print("No pending requests.")
    else:
        print("No pending requests.")
    
    input("\nPress Enter to continue...")

def approve_member():
    """Approve a team member"""
    os.chdir(REPO_PATH)
    run_cmd("git pull")
    
    view_pending_requests()
    
    choice = input("\nEnter member number to approve: ").strip()
    
    if choice.isdigit():
        with open("pending_members.txt", 'r') as f:
            requests = f.readlines()
        
        idx = int(choice) - 1
        if 0 <= idx < len(requests):
            selected = requests[idx]
            parts = selected.strip().split('|')
            device_key = parts[0]
            
            # Add to approved members
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("approved_members.txt", 'a') as f:
                f.write(f"{device_key}|{timestamp}|APPROVED|TEAM_MEMBER\n")
            
            # Remove from pending
            del requests[idx]
            with open("pending_members.txt", 'w') as f:
                f.writelines(requests)
            
            # Commit changes
            run_cmd("git add approved_members.txt pending_members.txt")
            run_cmd(f'git commit -m "Approved team member: {device_key[:16]}"')
            run_cmd("git push")
            
            print(f"\n✅ Member approved successfully!")
            input("Press Enter to continue...")

def view_all_members():
    """View all approved team members"""
    os.chdir(REPO_PATH)
    run_cmd("git pull")
    
    print("\n\033[1;32m👥 BLACK CYBER TEAM MEMBERS:\033[0m\n")
    if os.path.exists("approved_members.txt"):
        with open("approved_members.txt", 'r') as f:
            members = f.readlines()
        
        if members:
            for i, member in enumerate(members, 1):
                parts = member.strip().split('|')
                key = parts[0][:16] + "..."
                date = parts[1] if len(parts) > 1 else "Unknown"
                status = parts[2] if len(parts) > 2 else "ACTIVE"
                print(f"{i}. Member ID: {key} | Joined: {date} | Status: {status}")
        else:
            print("No team members yet.")
    else:
        print("No team members yet.")
    
    print(f"\nTeam Leader: @BlackCyberx (Admin)")
    input("\nPress Enter to continue...")

def broadcast_message():
    """Admin broadcast to all team members"""
    print("\n\033[1;33m📢 BROADCAST MESSAGE:\033[0m")
    message = input("Enter broadcast message: ").strip()
    
    if message:
        os.chdir(REPO_PATH)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("messages.txt", 'a') as f:
            f.write(f"\n[📢 ADMIN BROADCAST - {timestamp}]\n")
            f.write(f"[BlackCyber] 🔥 {message}\n")
            f.write("-" * 50 + "\n")
        
        run_cmd("git add messages.txt")
        run_cmd(f'git commit -m "Admin broadcast message"')
        run_cmd("git push")
        
        print("✅ Broadcast sent to all team members!")
        input("Press Enter to continue...")

def chat_interface(username):
    """Main chat interface for team members"""
    while True:
        print_banner()
        print(f"\n\033[1;34m👤 Logged in as: {username}\033[0m")
        print("\n1. 📖 Read messages")
        print("2. 💬 Send message")
        print("3. 🔄 Refresh")
        print("4. 🚪 Exit")
        
        choice = input("\n[TeamChat]# ").strip()
        
        if choice == "1":
            read_messages()
        elif choice == "2":
            send_message(username)
        elif choice == "3":
            continue
        elif choice == "4":
            break

def read_messages():
    """Read team chat messages"""
    os.chdir(REPO_PATH)
    run_cmd("git pull")
    
    print("\n\033[1;36m" + "="*60)
    print("📝 TEAM MESSAGES")
    print("="*60 + "\033[0m")
    
    if os.path.exists("messages.txt"):
        with open("messages.txt", 'r') as f:
            messages = f.readlines()
        
        if messages:
            for msg in messages[-50:]:  # Show last 50 messages
                print(msg.strip())
        else:
            print("No messages yet.")
    else:
        print("No messages yet.")
    
    input("\nPress Enter to continue...")

def send_message(username):
    """Send message to team chat"""
    message = input("\n💬 Your message: ").strip()
    
    if message:
        os.chdir(REPO_PATH)
        run_cmd("git pull")
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%Y-%m-%d")
        
        with open("messages.txt", 'a') as f:
            f.write(f"[{date} {timestamp}] {username}: {message}\n")
        
        run_cmd("git add messages.txt")
        run_cmd(f'git commit -m "New message from {username}"')
        run_cmd("git push")
        
        print("✅ Message sent!")
        time.sleep(1)

def clear_chat_history():
    """Admin function to clear chat"""
    confirm = input("\n⚠️  Clear entire chat history? (yes/no): ").strip()
    
    if confirm.lower() == "yes":
        os.chdir(REPO_PATH)
        with open("messages.txt", 'w') as f:
            f.write("=== BLACK CYBER TEAM CHAT ===\n")
            f.write(f"Chat cleared by Admin on {datetime.now()}\n")
            f.write("="*50 + "\n")
        
        run_cmd("git add messages.txt")
        run_cmd(f'git commit -m "Chat cleared by admin"')
        run_cmd("git push")
        
        print("✅ Chat history cleared!")
        input("Press Enter to continue...")

def view_statistics():
    """View team statistics"""
    os.chdir(REPO_PATH)
    run_cmd("git pull")
    
    print("\n\033[1;35m📊 TEAM STATISTICS:\033[0m\n")
    
    # Count members
    member_count = 0
    if os.path.exists("approved_members.txt"):
        with open("approved_members.txt", 'r') as f:
            member_count = len(f.readlines())
    
    # Count messages
    message_count = 0
    if os.path.exists("messages.txt"):
        with open("messages.txt", 'r') as f:
            message_count = len(f.readlines())
    
    # Count pending
    pending_count = 0
    if os.path.exists("pending_members.txt"):
        with open("pending_members.txt", 'r') as f:
            pending_count = len(f.readlines())
    
    print(f"Team Members: {member_count}")
    print(f"Pending Requests: {pending_count}")
    print(f"Total Messages: {message_count}")
    print(f"Team Leader: Black Cyber (@BlackCyberx)")
    print(f"Repository: https://github.com/BlackCyberx/teamchat")
    
    input("\nPress Enter to continue...")

def remove_member():
    """Remove a team member"""
    os.chdir(REPO_PATH)
    run_cmd("git pull")
    
    view_all_members()
    
    choice = input("\nEnter member number to remove: ").strip()
    
    if choice.isdigit():
        with open("approved_members.txt", 'r') as f:
            members = f.readlines()
        
        idx = int(choice) - 1
        if 0 <= idx < len(members):
            removed = members[idx]
            
            # Move to blacklist
            with open("blacklist.txt", 'a') as f:
                f.write(f"{removed.strip()}|REMOVED|{datetime.now()}\n")
            
            # Remove from approved
            del members[idx]
            with open("approved_members.txt", 'w') as f:
                f.writelines(members)
            
            run_cmd("git add approved_members.txt blacklist.txt")
            run_cmd(f'git commit -m "Removed team member"')
            run_cmd("git push")
            
            print(f"✅ Member removed successfully!")
            input("Press Enter to continue...")

def main():
    """Main function"""
    print_banner()
    
    # Setup environment
    setup_termux()
    setup_repo()
    
    # Get device key
    device_key = get_device_key()
    
    # Check approval status
    status, status_type = check_approval(device_key)
    
    if status_type == "admin":
        print("\n\033[1;32m✅ WELCOME BACK TEAM LEADER BLACK CYBER!\033[0m")
        time.sleep(1)
        admin_panel()
        chat_interface("BlackCyber")
        
    elif status:
        print("\n\033[1;32m✅ ACCESS GRANTED! Welcome to Black Cyber Team!\033[0m")
        time.sleep(1)
        chat_interface(f"Member-{device_key[:8]}")
        
    else:
        if status_type == "pending":
            print("\n\033[1;33m⏳ YOUR REQUEST IS PENDING ADMIN APPROVAL\033[0m")
            print("\nYour device key:", device_key)
            print("\nSend this key to @BlackCyberx for approval")
            print("GitHub: https://github.com/BlackCyberx")
        else:
            print("\n\033[1;33m📨 APPROVAL REQUEST SENT!\033[0m")
            print("\nYour device key:", device_key)
            print("\nSend this key to @BlackCyberx on GitHub")
            print("\nWaiting for approval...")
        
        print("\n1. Check approval status")
        print("2. Exit")
        
        choice = input("\n[TeamChat]# ").strip()
        if choice == "1":
            main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Exiting Black Cyber Team Chat...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        input("Press Enter to exit...")
