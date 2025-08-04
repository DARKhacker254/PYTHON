import nmap

# Create a PortScanner instance
from nmap import PortScanner
nm = PortScanner()


# You can scan multiple IPs or a subnet
# Example list: single IPs or CIDR subnet
targets = ['127.0.0.1', '192.168.1.1', '192.168.1.0/30']

# Port range to scan
ports = '22-443'

for target in targets:
    print(f"\n🔍 Scanning: {target}")
    nm.scan(hosts=target, ports=ports)

    for host in nm.all_hosts():
        print('----------------------------------------------------')
        print(f'Host : {host} ({nm[host].hostname()})')
        print(f'State : {nm[host].state()}')

        for proto in nm[host].all_protocols():
            print('----------')
            print(f'Protocol : {proto}')

            lport = sorted(nm[host][proto].keys())
            for port in lport:
                state = nm[host][proto][port]['state']
                print(f'Port : {port}\tState : {state}')
