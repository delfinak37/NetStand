# Генерация трафика

## Netcat

Генерация **html** трафика используя `netcat`:

<img width="616" height="336" alt="изображение" src="https://github.com/user-attachments/assets/1e5ddafb-51ef-48db-a133-70ab8efcc24a" />

## Ping

### Настройка **scapy**

Перед установкой создается виртуальное окружение через `venv`, куда после устанавливается `scapy`:

<img width="614" height="328" alt="изображение" src="https://github.com/user-attachments/assets/ae96bce3-292e-4b8a-a508-9c09e86516da" />

### Генерация ping

Скрипт для генерации `ping` запросов:
```py
#!/usr/bin/env python3
from scapy.all import *
import argparse
import time

def ping(target, count, timeout, verbose=False):
    print(f"\n[*] Scanning {target} with {count} packets...\n")
        
    for i in range(count):
         packet = IP(dst=target) / ICMP(id=i, seq=i)
        
        reply = sr1(packet, timeout=timeout, verbose=verbose)
        
        if reply:
            print(f"[+] Pong from {reply.src} | seq={reply[ICMP].seq} | ttl={reply.ttl}")
        else:
            print(f"[-] Timeout for packet {i+1}")

def ping_batch(target, count, timeout, interval=0.5):
    print(f"\n[*] Batch scanning {target} with {count} packets...\n")
    
    for i in range(count):  
        packet = IP(dst=target) / ICMP(id=i, seq=i)
        reply = sr1(packet, timeout=timeout, verbose=False)
        
        if reply:
            print(f"[+] Pong from {reply.src} | seq={reply[ICMP].seq}")
        else:
            print(f"[-] Timeout for packet {i+1}")
        
        time.sleep(interval) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scapy Ping Tool")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-c", "--count", type=int, default=4, help="Number of packets (default: 4)")
    parser.add_argument("-t", "--timeout", type=int, default=2, help="Timeout per packet in seconds (default:>
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
parser.add_argument("-i", "--interval", type=float, default=0, help="Interval between packets in seconds")
    
    args = parser.parse_args()
    
    if args.interval > 0:
        ping_batch(args.target, args.count, args.timeout, args.interval)
    else:
        ping(args.target, args.count, args.timeout, args.verbose)
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-i", "--interval", type=float, default=0, help="Interval between packets in seconds")
    
    args = parser.parse_args()
    
    if args.interval > 0:
        ping_batch(args.target, args.count, args.timeout, args.interval)
    else:
        ping(args.target, args.count, args.timeout, args.verbose)
```
