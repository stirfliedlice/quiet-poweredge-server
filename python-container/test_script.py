#!/usr/bin/python3

import time, argparse, subprocess
from datetime import datetime

def myfunction(idrac_ip="blank idrac_ip", idrac_username="blank idrac_username", idrac_password="blank idrac_password") -> None:
    while True:
        # with open("timestamp.txt", "a") as f:
        #     f.write("The current timestamp is: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #     f.close()
        print("The current timestamp is: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(idrac_ip + " " + idrac_username + " " + idrac_password)
        process = subprocess.run(["ipmitool","-help"], capture_output=True)
        print(process.stderr)
        time.sleep(10)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]",
        description="just a test script"
    )
    parser.add_argument('ip',help='iDRAC IP address')
    parser.add_argument('usr', help='iDRAC username')
    parser.add_argument('pw', help='iDRAC password')
    parser.add_argument("-v", "--version", action="version", version = f"{parser.prog} version 1.0.0")
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    myfunction(args.ip, args.usr, args.pw)
    # myfunction()

if __name__ == "__main__":
    main()