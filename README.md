# QoS + Doze Stress Tester for 802.11 Hardware

## 📌 Purpose
This tool is designed to **stress test 802.11 Wi-Fi hardware** by exploiting QoS (Quality of Service) mechanisms and power-saving features (Doze mode). It continuously suppresses targeted client devices by:
- Manipulating **QoS priority levels** to degrade performance.
- Sending **Power Save (Doze) frames** to interfere with normal data transmission.
- Periodically injecting **deauthentication bursts** to disrupt reconnections.

The result is an effective **wireless device stress test**, useful for **analyzing AP behavior**, client-side recovery strategies, and potential **resilience against adaptive interference**.

---

## ⚙️ Dependencies

### **System Packages**
Ensure your system has the required dependencies:

```bash
sudo apt update
sudo apt install python3 python3-pip net-tools wireless-tools aircrack-ng

python3	Required for script execution
python3-pip	Installs Python dependencies
net-tools	Provides ifconfig for network checks
wireless-tools	Manages Wi-Fi interfaces
aircrack-ng	Enables monitor mode & packet injection
scapy
pip3 install scapy argparse

usage example
sudo python3 qos_doze.py -t <Client_MAC> -a <AP_MAC> -i <Monitor_Interface> --deauth-interval 60
Adaptive QoS Manipulation – Forces low-priority traffic to degrade performance.
Power Save (Doze) Exploitation – Keeps the client device in network limbo.
Randomized Deauth Attacks – Prevents easy detection and adaptation.
Fully Customizable – Users can tweak parameters for different stress testing scenarios.


Future Improvements

Dynamic AP Detection (Auto-find AP & clients for testing)
GUI Interface for easier configuration
Adaptive Timing (Detect recovery & auto-adjust attack intensity)

