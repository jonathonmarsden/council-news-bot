import argparse
import os
import pty
import subprocess
import sys
import time

# Add current directory to path to allow importing deploy_secrets
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import credentials from a local ignored file
try:
    from deploy_secrets import HOST, USER, PASS
except ImportError:
    print("Error: deploy_secrets.py not found in the same directory.")
    print("Please create it with HOST, USER, and PASS variables.")
    sys.exit(1)

TARGET_DIR = "/opt/council-news-bot"

def read(fd):
    return os.read(fd, 1024)

def ensure_local_deploy_allowed(allow_dirty: bool) -> None:
    if not allow_dirty:
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
        )
        if status.stdout.strip():
            print("Error: working tree has uncommitted changes.")
            print("Commit changes or re-run with --allow-dirty for emergency deploys.")
            sys.exit(1)


def deploy(force_local: bool, allow_dirty: bool):
    if not force_local:
        print("Local SSH deploy is for emergency use only.")
        print("Use GitHub Actions for normal production deploys.")
        print("Re-run with --force-local to proceed anyway.")
        sys.exit(1)

    ensure_local_deploy_allowed(allow_dirty)

    # We need to run the bash script, but wrapping it in a way we can feed the password
    # Actually, the bash script calls ssh/rsync multiple times. 
    # It's better to rewrite the logic here or use sshpass if we had it.
    # Since we don't have sshpass, let's try to run the bash script and feed the password whenever requested.
    
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy_to_vps.sh")
    
    pid, fd = pty.fork()
    
    if pid == 0:
        # Child process
        os.execv(script_path, [script_path, "--force-local"])
    else:
        # Parent process
        try:
            while True:
                try:
                    output = read(fd).decode(errors='ignore')
                    if not output:
                        break
                    sys.stdout.write(output)
                    sys.stdout.flush()
                    
                    # Look for password prompts
                    # Common prompts: "password:", "Password:", "root@170.64.186.16's password:"
                    if "password:" in output.lower():
                        time.sleep(0.5) # Wait a bit for buffer
                        os.write(fd, (PASS + "\n").encode())
                        # print("\n(Auto-entered password)")
                        
                    # Also handle "Are you sure you want to continue connecting" (known_hosts)
                    if "continue connecting" in output.lower():
                        time.sleep(0.5)
                        os.write(fd, b"yes\n")
                        
                except OSError:
                    break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            os.close(fd)
            # os.waitpid(pid, 0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Emergency SSH deploy (not for normal use)")
    parser.add_argument("--force-local", action="store_true", help="Allow local SSH deploy")
    parser.add_argument("--allow-dirty", action="store_true", help="Allow deploy with uncommitted changes")
    args = parser.parse_args()
    deploy(args.force_local, args.allow_dirty)
