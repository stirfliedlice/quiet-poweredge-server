#!/usr/bin/python3

import requests, warnings, subprocess, argparse, time, os

def get_env_vars() -> dict:
    idrac_ip = os.environ.get("IDRACIP")
    idrac_user = os.environ.get("IDRACUSER")
    idrac_password = os.environ.get("IDRACPASSWORD")
    env_vars = {"idrac_ip":idrac_ip, "idrac_user":idrac_user, "idrac_password":idrac_password}
    return env_vars

def manual_fan_control(idrac_ip, idrac_username, idrac_password) -> None:
    # SET FANS TO LOW SPEED USING IPMI
    # enable manual/static fan control
    # ipmitool -I lanplus -H <iDRAC-IP> -U <iDRAC-USER> -P <iDRAC-PASSWORD> raw 0x30 0x30 0x01 0x00
    # set fan speed to 20 %
    # ipmitool -I lanplus -H <iDRAC-IP> -U <iDRAC-USER> -P <iDRAC-PASSWORD> raw 0x30 0x30 0x02 0xff 0x14
    # set fan speed to 12 %
    # ipmitool -I lanplus -H <iDRAC-IP> -U <iDRAC-USER> -P <iDRAC-PASSWORD> raw 0x30 0x30 0x02 0xff 0xC
    subprocess.run(["ipmitool", "-I", "lanplus", "-H", idrac_ip, "-U", idrac_username, "-P", idrac_password, "raw", "0x30", "0x30", "0x01", "0x00"])
    subprocess.run(["ipmitool", "-I", "lanplus", "-H", idrac_ip, "-U", idrac_username, "-P", idrac_password, "raw", "0x30", "0x30", "0xff", "0x14"])
    # subprocess.run(["ipmitool", "-I", "lanplus", "-H", idrac_ip, "-U", idrac_username, "-P", idrac_password, "sensor", "reading", "Exhaust Temp"])

def auto_fan_control(idrac_ip, idrac_username, idrac_password) -> None:
    # TURN ON FANS USING IPMI
    # disable manual/static fan control
    # ipmitool -I lanplus -H <iDRAC-IP> -U <iDRAC-USER> -P <iDRAC-PASSWORD> raw 0x30 0x30 0x01 0x01
    subprocess.run(["ipmitool", "-I", "lanplus", "-H", idrac_ip, "-U", idrac_username, "-P", idrac_password, "raw", "0x30", "0x30", "0x01", "0x01"])
    # subprocess.run(["ipmitool", "-I", "lanplus", "-H", idrac_ip, "-U", idrac_username, "-P", idrac_password, "sensor", "reading", "Inlet Temp"])

def query_redfish(idrac_ip, idrac_username, idrac_password) -> dict:
    warnings.filterwarnings("ignore")
    # HTTP GET REQUEST
    response = requests.get(f"https://{idrac_ip}/redfish/v1/Chassis/System.Embedded.1/Thermal",verify=False,auth=(idrac_username, idrac_password))
    data = response.json()
    return data

def check_temperature(data) -> bool:
    # ANALYZE DATA FROM REQUEST
    for i in range(len(data["Temperatures"])):
        # CHECK THE TEMPS
        if data["Temperatures"][i]["ReadingCelsius"] > (data["Temperatures"][i]["UpperThresholdNonCritical"] * .8):
            return True
    return False

def ipmitool_checker() -> bool:
    process = subprocess.run(["which","ipmitool"], capture_output=True)
    if process.returncode != 0:
        raise SystemError("ipmitool not found/installed")

def main() -> None:
    env_vars = get_env_vars()

    ipmitool_checker()
    manual_fan_control(args.ip, args.usr, args.pw)
    while True:
        data = query_redfish(args.ip, args.usr, args.pw)
        if check_temperature(data):
            auto_fan_control(args.ip, args.usr, args.pw)
            while True:
                data = query_redfish(args.ip, args.usr, args.pw)
                if not check_temperature(data):
                    manual_fan_control(args.ip, args.usr, args.pw)
                    break
                time.sleep(10)
        time.sleep(10)

if __name__ == "__main__":
    main()

