#!/usr/bin/python3
import requests, warnings, subprocess, time, os

def get_env_vars() -> dict:
    ip = os.environ["IDRACIP"]
    usr = os.environ["IDRACUSER"]
    pw = os.environ["IDRACPASSWORD"]
    return (ip, usr, pw)

def ipmitool_checker() -> bool:
    process = subprocess.run(["which","ipmitool"], check=True)

def query_redfish(idrac_ip, idrac_username, idrac_password) -> dict:
    warnings.filterwarnings("ignore")
    # HTTP GET REQUEST
    response = requests.get(f"https://{idrac_ip}/redfish/v1/Chassis/System.Embedded.1/Thermal", verify=False, auth=(idrac_username, idrac_password))
    return response.json()

def check_temperature(data) -> bool:
    # ANALYZE DATA FROM REQUEST
    for i in range(len(data["Temperatures"])):
        # CHECK THE TEMPS
        current_temp = data["Temperatures"][i]["ReadingCelsius"]
        max_non_crit_temp = data["Temperatures"][i]["UpperThresholdNonCritical"]
        if current_temp > (max_non_crit_temp * .8):
            return True
    return False

def run_ipmi_cmd(ipmi_cmd) -> None:
    subprocess.run(ipmi_cmd, check=True)

def main() -> None:
    env_vars = get_env_vars()

    ip = env_vars[0]
    usr = env_vars[1]
    pw = env_vars[2]

    ipmi_cmd = ["ipmitool", "-I", "lanplus", "-H", ip, "-U", usr, "-P", pw, "raw", "0x30", "0x30"]
    manual_control = ["0x01", "0x00"]
    manual_setpoint = ["0xff", "0x14"]
    auto_control = ["0x01", "0x01"]

    ipmitool_checker()

    run_ipmi_cmd(ipmi_cmd.extend(manual_control))
    run_ipmi_cmd(ipmi_cmd.extend(manual_setpoint))
    while True:
        data = query_redfish(ip, usr, pw)
        if check_temperature(data):
            run_ipmi_cmd(ipmi_cmd.extend(auto_control))
            while True:
                data = query_redfish(ip, usr, pw)
                if not check_temperature(data):
                    run_ipmi_cmd(ipmi_cmd.extend(manual_control))
                    run_ipmi_cmd(ipmi_cmd.extend(manual_setpoint))
                    break
                time.sleep(10)
        time.sleep(10)

if __name__ == "__main__":
    main()

# SET FANS TO LOW SPEED USING IPMI
# enable manual/static fan control
# ipmitool -I lanplus -H <iDRAC-IP> -U <iDRAC-USER> -P <iDRAC-PASSWORD> raw 0x30 0x30 0x01 0x00
# set fan speed to 20 %
# ipmitool -I lanplus -H <iDRAC-IP> -U <iDRAC-USER> -P <iDRAC-PASSWORD> raw 0x30 0x30 0x02 0xff 0x14
# set fan speed to 12 %
# ipmitool -I lanplus -H <iDRAC-IP> -U <iDRAC-USER> -P <iDRAC-PASSWORD> raw 0x30 0x30 0x02 0xff 0xC
# TURN ON FANS USING IPMI
# disable manual/static fan control
# ipmitool -I lanplus -H <iDRAC-IP> -U <iDRAC-USER> -P <iDRAC-PASSWORD> raw 0x30 0x30 0x01 0x01
