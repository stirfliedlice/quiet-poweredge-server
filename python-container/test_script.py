#!/usr/bin/python3
import time, subprocess, os
from datetime import datetime

def myfunction(ip, usr, pw) -> None:
    while True:
        print(f"The current timestamp is: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{ip} {usr} {pw}")
        process = subprocess.run(["ipmitool", "-I", "lanplus", "-H", ip, "-U", usr, "-P", pw, "session", "info", "all"], capture_output=True, check=True, text=True)
        time.sleep(10)

def get_os_env_vars():
    ip = os.environ["IDRACIP"]
    usr = os.environ["IDRACUSER"]
    pw = os.environ["IDRACPASSWORD"]
    return (ip, usr, pw)

def main() -> None:
    env_vars = get_os_env_vars()
    myfunction(env_vars[0], env_vars[1], env_vars[2])

if __name__ == "__main__":
    main()