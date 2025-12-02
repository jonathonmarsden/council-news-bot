import pty
import os
import sys
import time

# Try to import credentials from a local ignored file
try:
    from deploy_secrets import HOST, USER, PASS
except ImportError:
    print("Error: scripts/deploy_secrets.py not found.")
    print("Please create it with HOST, USER, and PASS variables.")
    sys.exit(1)

TARGET_DIR = "/opt/council-news-bot"

def read(fd):
    return os.read(fd, 1024)

def deploy():
    # We need to run the bash script, but wrapping it in a way we can feed the password
    # Actually, the bash script calls ssh/rsync multiple times. 
    # It's better to rewrite the logic here or use sshpass if we had it.
    # Since we don't have sshpass, let's try to run the bash script and feed the password whenever requested.
    
    pid, fd = pty.fork()
    
    if pid == 0:
        # Child process
        os.execv("./scripts/deploy_to_vps.sh", ["./scripts/deploy_to_vps.sh"])
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
                    # Common prompts: "password:", "Password:", "root@vps.example.com's password:"
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
    deploy()
