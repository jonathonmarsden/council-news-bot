import pty
import os
import sys
import time

# Credentials
HOST = "vps.example.com"
USER = "root"
PASS = "TOWING.takeshi7staples9vault"
# Fix permissions for data and logs directories
CMD = "chmod -R 777 /opt/council-news-bot/data /opt/council-news-bot/logs && docker compose -f /opt/council-news-bot/docker-compose.yml restart"

def read(fd):
    return os.read(fd, 1024)

def fix_perms():
    pid, fd = pty.fork()
    
    if pid == 0:
        os.execv("/usr/bin/ssh", ["ssh", f"{USER}@{HOST}", CMD])
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
                        
                    if "continue connecting" in output.lower():
                        time.sleep(0.5)
                        os.write(fd, b"yes\n")
                        
                except OSError:
                    break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            os.close(fd)

if __name__ == "__main__":
    fix_perms()
