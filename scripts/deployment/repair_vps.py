
import pty
import os
import sys
import time

# Add current directory to path to allow importing deploy_secrets
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from deploy_secrets import HOST, USER, PASS
except ImportError:
    print("Error: deploy_secrets.py not found.")
    sys.exit(1)

def read(fd):
    return os.read(fd, 1024)

def run_remote_command(command):
    ssh_cmd = ["ssh", "-o", "PreferredAuthentications=password", "-o", "PubkeyAuthentication=no", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", f"{USER}@{HOST}", command]
    
    print(f"Running: {command}")
    
    pid, fd = pty.fork()
    
    if pid == 0:
        os.execvp(ssh_cmd[0], ssh_cmd)
    else:
        try:
            while True:
                try:
                    output = read(fd).decode(errors='ignore')
                    if not output:
                        break
                    sys.stdout.write(output)
                    sys.stdout.flush()
                    
                    if "password:" in output.lower():
                        time.sleep(0.5)
                        os.write(fd, (PASS + "\n").encode())
                        
                except OSError:
                    break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            os.close(fd)

def main():
    print("=== Repairing VPS Docker State ===")
    
    # 1. Check DB State (while we are here)
    print("\n--- Checking Database State ---")
    run_remote_command("python3 /opt/council-news-bot/scripts/deployment/check_vps_db_internal.py")
    
    # 2. Prune Docker
    print("\n--- Pruning Docker System ---")
    run_remote_command("docker system prune -af")
    
    # 3. Rebuild and Start
    print("\n--- Rebuilding and Starting Bot ---")
    run_remote_command("cd /opt/council-news-bot && docker compose build --no-cache && docker compose up -d")
    
    print("\n=== Repair Complete ===")

if __name__ == "__main__":
    main()
