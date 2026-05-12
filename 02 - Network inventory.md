# Инвентаризация сети

## Основные задачи

  1) Просканнировать сеть
  2) Найти службы
  3) Оределить версии ОС и служб
  4) Проверить на уязвимости

## Сканирование сети

Проверка IP-адресов и маршрутов на `Kali`:

<img width="853" height="439" alt="изображение" src="https://github.com/user-attachments/assets/e1f91c9c-7c74-460e-b230-9c168769773d" />

- Машина находится в сети `192.168.10.0/24` и имеет шлюз `192.168.10.1`

Проверка доступности шлюза и интернета:

<img width="602" height="387" alt="изображение" src="https://github.com/user-attachments/assets/63e34a5f-70c1-4631-9c50-dd470b369cba" />

- Проверка успешна, шлюз и интерент доступны

Сканирование сети `192.168.10.0/24`:

<img width="900" height="787" alt="изображение" src="https://github.com/user-attachments/assets/fe837900-b59d-471b-8893-8465bb83e622" />

**Результаты сканирования:**

  - `192.168.10.1` - `OpenWrt.lan`
  - `192.168.10.24` - `kali.lan`

| Порт | Сервис | Назначение |
|------|--------|------------|
| 22/tcp | SSH | Удалённое управление роутером |
| 53/tcp | DNS | Доменные запросы |
| 80/tcp | HTTP) | Веб-интерфейс |
| 443/tcp | HTTPS | Веб-интерфейс |

Попытка перебрать доменные записи в сети:

<img width="552" height="309" alt="изображение" src="https://github.com/user-attachments/assets/289d1eef-8e60-403c-b52b-8d35face103e" />

- Ничего не нашлось кроме портов

Обычно роутер имеет IP-адрес x.x.x.1, также роутер в системе имеет имя - `OpenWrt.lan`. Тогда можно перебрать все подсети с этими условиями:

<img width="647" height="98" alt="изображение" src="https://github.com/user-attachments/assets/b3bf698f-18d0-486e-ac47-29f740ec0d30" />

- Обнаружено 3 подсети

Раз в сети `192.168.10.0` находится `Kali`, тогда следует просканировать другие сети:

<img width="531" height="148" alt="изображение" src="https://github.com/user-attachments/assets/69ec44fa-c8c3-45dc-bf6d-03128e8148ca" />

<img width="552" height="270" alt="изображение" src="https://github.com/user-attachments/assets/9da30db0-1d86-4e7e-ab0b-d85ce539fd30" />

**Результаты сканирования:**

  - `192.168.20.1` - `OpenWrt.lan`
  - `192.168.20.24` - `metasploitable3-ub1404.lan`

  - `192.168.30.x` - Не дало явных данных кроме наличия роутера в сети

  По итогу вышла такая система сети:

  | IP | Сеть | Узел |
|----|------|------|
| 192.168.10.1 | 192.168.10.0/24 | OpenWrt.lan |
| 192.168.20.1 | 192.168.20.0/24 | OpenWrt.lan |
| 192.168.30.1 | 192.168.30.0/24 | OpenWrt.lan |
| 192.168.10.24 | 192.168.10.0/24 | KaliLinux.lan |
| 192.168.20.205 | 192.168.20.0/24 | metasploitable3-ub1404.lan |

## Определение ОС служб и их версий

### 1) Узел `kali.lan`

<img width="822" height="286" alt="изображение" src="https://github.com/user-attachments/assets/a221f0ec-4689-4903-b105-88e90287699c" />

**IP-адрес:** 192.168.10.24  
**Тип устройства:** Атакующая машина  
**Операционная система:** Debian-based Linux (ядро 5.0 — 6.2)  
**Сетевое расстояние:** 0 хопов (локальный хост)

**Открытые порты и службы:**

| Порт | Состояние | Служба | Версия / Примечание |
|------|-----------|--------|---------------------|
| 22/tcp | open | SSH | OpenSSH 10.0p2 Debian 5 |

### 2) Узел `metasploitable3-ub1404.lan`

<img width="973" height="784" alt="изображение" src="https://github.com/user-attachments/assets/d9c02afe-ed3e-406c-ae37-ad9ce989e879" />

<img width="978" height="351" alt="изображение" src="https://github.com/user-attachments/assets/3a4d925c-282a-4e3c-b15c-f2eaf7ab6994" />

**IP-адрес:** 192.168.20.205  
**Тип устройства:** Уязвимая машина / Цель для атак  
**Операционная система:** Ubuntu Linux (ядро 3.2 — 4.14)  
**Сетевое расстояние:** 2 хопа (через роутер OpenWrt)

**Открытые порты и службы:**

| Порт | Состояние | Служба | Версия / Примечание |
|------|-----------|--------|---------------------|
| 21/tcp | open | FTP | ProFTPD 1.3.5 |
| 22/tcp | open | SSH | OpenSSH 6.6.1p1 Ubuntu 2.2.13 |
| 80/tcp | open | HTTP | Apache httpd 2.4.7 |
| 445/tcp | open | NetBIOS-SSN | Samba smbd 4.3.11-Ubuntu |
| 631/tcp | open | IPP | CUPS 1.7 |
| 3306/tcp | open | MySQL | MySQL |
| 8080/tcp | open | HTTP | Jetty 8.1.7.v20120910 |
| 3000/tcp | closed | ppp | - |
| 8081/tcp | closed | intermapper | - |

### 3) Узел `OpenWrt.lan`

<img width="973" height="523" alt="изображение" src="https://github.com/user-attachments/assets/65cd79aa-9a8e-4d4d-8ae9-0d9a35cc6209" />

**IP-адрес:** 192.168.10.1  
**Тип устройства:** Маршрутизатор / Шлюз сети  
**Операционная система:** OpenWrt 21.02 (Linux 5.4)  
**Сетевое расстояние:** 1 хоп

**Открытые порты и службы:**

| Порт | Состояние | Служба | Версия / Примечание |
|------|-----------|--------|---------------------|
| 22/tcp | open | SSH | Dropbear sshd (протокол 2.0) |
| 53/tcp | open | DNS | Cloudflare public DNS |
| 80/tcp | open | HTTP | OpenWrt uHTTPd |
| 443/tcp | open | SSL/HTTP | OpenWrt uHTTPd |


## Проверка на уязвимости

### 1) Узел `kali.lan`

<img width="976" height="408" alt="изображение" src="https://github.com/user-attachments/assets/4072b423-6ea4-4a5d-9914-180d3c29f27c" />

### Уязвимости

| Порт | Служба | CVE | CVSS |
|------|--------|-----|------|
| 22/tcp | OpenSSH 10.0p2 | CVE-2026-35414 | 8.1 |
| 22/tcp | OpenSSH 10.0p2 | CVE-2026-35386 | 8.1 |
| 22/tcp | OpenSSH 10.0p2 | CVE-2026-35385 | 8.1 |
| 22/tcp | OpenSSH 10.0p2 | CVE-2026-35387 | 6.5 |
| 22/tcp | OpenSSH 10.0p2 | CVE-2025-61985 | 3.6 |
| 22/tcp | OpenSSH 10.0p2 | CVE-2025-61984 | 3.6 |
| 22/tcp | OpenSSH 10.0p2 | B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150 | 3.6 |
| 22/tcp | OpenSSH 10.0p2 | 4C6E2182-0E99-5626-83F6-1646DD648C57 | 3.6 |
| 22/tcp | OpenSSH 10.0p2 | CVE-2026-35388 | 2.5 |

### 2) Узел `metasploitable3-ub1404.lan`

<img width="760" height="570" alt="изображение" src="https://github.com/user-attachments/assets/79ad9b56-738a-4e08-afc8-cd95e2b1792f" />

### Уязвимости

| Порт | Служба | Уязвимость | CVSS | Эксплойт |
|------|--------|------------|------|----------|
| 21/tcp | ProFTPD 1.3.5 | CVE-2015-3306 (mod_copy RCE) | 10.0 | Metasploit |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2023-38408 (RCE через PKCS#11) | 9.8 | Есть эксплойты |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2016-1908 (X11 forwarding DoS) | 9.8 | Эксплойт |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2020-15778 (scp command injection) | 7.8 | EDB-ID:46516 |
| 80/tcp | Apache 2.4.7 | SQL-инъекции | — | Встроенный скрипт nmap |
| 80/tcp | Apache 2.4.7 | DOM-based XSS | — | Встроенный скрипт nmap |
| 80/tcp | Apache 2.4.7 | CSRF | — | Встроенный скрипт nmap |
| 80/tcp | Apache 2.4.7 | Slowloris DoS (CVE-2007-6750) | — | Уязвим |
| 3306/tcp | MySQL | Неавторизованный доступ | — | Любой клиент MySQL |
| 6697/tcp | UnrealIRCd | Троянизированная версия (backdoor) | 10.0 | Metasploit |
| 8080/tcp | Jetty 8.1.7 | CSRF | — | Встроенный скрипт nmap |
| 8080/tcp | Jetty 8.1.7 | Slowloris DoS (CVE-2007-6750) | — | Уязвим |

### 3) Узел `OpenWrt.lan`

### Уязвимости
