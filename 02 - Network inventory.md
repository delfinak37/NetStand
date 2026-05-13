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

<img width="911" height="620" alt="изображение" src="https://github.com/user-attachments/assets/89979332-176d-484f-8abb-79aaf58c71c9" />


### Уязвимости

| Порт | Служба | Уязвимость | CVSS | Эксплойт |
|------|--------|------------|------|----------|
| 21/tcp | ProFTPD 1.3.5 | CVE-2015-3306 (mod_copy RCE) | 10.0 | Metasploit, EDB-ID:37262, EDB-ID:49908 |
| 21/tcp | ProFTPD 1.3.5 | CVE-2026-44331 | 8.1 | Нет |
| 21/tcp | ProFTPD 1.3.5 | CVE-2024-48651 | 7.5 | Нет |
| 21/tcp | ProFTPD 1.3.5 | CVE-2023-51713 | 7.5 | Нет |
| 21/tcp | ProFTPD 1.3.5 | CVE-2021-46854 | 7.5 | Нет |
| 21/tcp | ProFTPD 1.3.5 | CVE-2020-9272 | 7.5 | Нет |
| 21/tcp | ProFTPD 1.3.5 | CVE-2019-19272 | 7.5 | Нет |
| 21/tcp | ProFTPD 1.3.5 | CVE-2019-19271 | 7.5 | Нет |
| 21/tcp | ProFTPD 1.3.5 | CVE-2019-19270 | 7.5 | Нет |
| 21/tcp | ProFTPD 1.3.5 | CVE-2019-18217 | 7.5 | Нет |
| 21/tcp | ProFTPD 1.3.5 | CVE-2016-3125 | 7.5 | Нет |
| 21/tcp | ProFTPD 1.3.5 | CVE-2023-48795 | 5.9 | Нет |
| 21/tcp | ProFTPD 1.3.5 | CVE-2017-7418 | 5.5 | Нет |
| 21/tcp | ProFTPD 1.3.5 | CVE-2013-4359 | 5.0 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2023-38408 (RCE через PKCS#11) | 9.8 | Есть |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2016-1908 (X11 forwarding DoS) | 9.8 | Есть |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2015-5600 | 8.5 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2026-35414 | 8.1 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2026-35386 | 8.1 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2026-35385 | 8.1 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2020-15778 (scp command injection) | 7.8 | EDB-ID:46516 |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2016-6515 | 7.8 | Есть |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2016-10012 | 7.8 | Есть |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2015-8325 | 7.8 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2016-10708 | 7.5 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2016-10009 | 7.5 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2021-41617 | 7.0 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2016-10010 | 7.0 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2015-6564 | 6.9 | Есть |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2019-6110 | 6.8 | Есть |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2019-6109 | 6.8 | Есть |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2026-35387 | 6.5 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2023-51385 | 6.5 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2016-3115 | 6.4 | Есть |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2023-48795 | 5.9 | Есть |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2020-14145 | 5.9 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2019-6111 | 5.9 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2018-15473 | 5.9 | Есть |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2016-6210 | 5.9 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2016-10011 | 5.5 | Есть |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2018-20685 | 5.3 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2018-15919 | 5.3 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2017-15906 | 5.3 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2016-20012 | 5.3 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2015-5352 | 4.3 | Есть |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2021-36368 | 3.7 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2025-61985 | 3.6 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2025-61984 | 3.6 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2026-35388 | 2.5 | Нет |
| 22/tcp | OpenSSH 6.6.1p1 | CVE-2015-6563 | 1.9 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2026-28780 | 9.8 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2024-38476 | 9.8 | Есть |
| 80/tcp | Apache 2.4.7 | CVE-2024-38474 | 9.8 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2023-25690 | 9.8 | Есть |
| 80/tcp | Apache 2.4.7 | CVE-2022-31813 | 9.8 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2022-23943 | 9.8 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2022-22720 | 9.8 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2021-44790 | 9.8 | Есть |
| 80/tcp | Apache 2.4.7 | CVE-2021-39275 | 9.8 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2021-26691 | 9.8 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2018-1312 | 9.8 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2017-7679 | 9.8 | Есть |
| 80/tcp | Apache 2.4.7 | CVE-2017-3169 | 9.8 | Есть |
| 80/tcp | Apache 2.4.7 | CVE-2017-3167 | 9.8 | Есть |
| 80/tcp | Apache 2.4.7 | CVE-2024-40898 | 9.1 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2024-38475 | 9.1 | Есть |
| 80/tcp | Apache 2.4.7 | CVE-2022-28615 | 9.1 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2022-22721 | 9.1 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2017-9788 | 9.1 | Есть |
| 80/tcp | Apache 2.4.7 | CVE-2022-36760 | 9.0 | Есть |
| 80/tcp | Apache 2.4.7 | CVE-2021-40438 | 9.0 | Есть |
| 80/tcp | Apache 2.4.7 | CVE-2026-24072 | 8.8 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2025-58098 | 8.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2021-44224 | 8.2 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2024-38473 | 8.1 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2017-15715 | 8.1 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2016-5387 | 8.1 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2026-34059 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2026-29169 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2025-59775 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2024-47252 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2024-43394 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2024-43204 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2024-42516 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2024-39573 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2024-38477 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2024-38472 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2023-31122 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2022-30556 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2022-29404 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2022-26377 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2022-22719 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2021-34798 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2021-33193 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2021-26690 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2019-0217 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2018-8011 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2018-17199 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2018-1303 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2017-9798 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2017-15710 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2016-8743 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2016-2161 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2016-0736 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2006-20001 | 7.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2025-49812 | 7.4 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2023-38709 | 7.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2020-35452 | 7.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2014-0226 | 6.8 | Есть |
| 80/tcp | Apache 2.4.7 | CVE-2026-33523 | 6.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2025-65082 | 6.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2024-24795 | 6.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2020-1927 | 6.1 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2019-10098 | 6.1 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2019-10092 | 6.1 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2016-4975 | 6.1 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2018-1302 | 5.9 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2018-1301 | 5.9 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2020-13938 | 5.5 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2025-66200 | 5.4 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2026-34032 | 5.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2026-33857 | 5.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2026-33007 | 5.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2022-37436 | 5.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2022-28614 | 5.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2022-28330 | 5.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2020-1934 | 5.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2020-11985 | 5.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2019-17567 | 5.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2019-0220 | 5.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2018-1283 | 5.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2015-3183 | 5.0 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2015-0228 | 5.0 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2014-3581 | 5.0 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2014-3523 | 5.0 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2014-0231 | 5.0 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2014-0098 | 5.0 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2013-6438 | 5.0 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2013-5704 | 5.0 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2026-33006 | 4.8 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2016-8612 | 4.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2015-3185 | 4.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2014-8109 | 4.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2014-0118 | 4.3 | Нет |
| 80/tcp | Apache 2.4.7 | CVE-2014-0117 | 4.3 | Нет |
| 80/tcp | Apache 2.4.7 | Slowloris DoS (CVE-2007-6750) | — | Уязвим |
| 80/tcp | Apache 2.4.7 | SQL-инъекции | — | Встроенный скрипт nmap |
| 80/tcp | Apache 2.4.7 | CSRF | — | Встроенный скрипт nmap |
| 80/tcp | Apache 2.4.7 | Листинг директорий | — | Информативное |
| 445/tcp | Samba 3.X-4.X | regsvc DoS (null dereference) | — | Уязвим |
| 631/tcp | CUPS 1.7 | CVE-2014-5031 | 5.0 | Нет |
| 631/tcp | CUPS 1.7 | CVE-2014-2856 | 4.3 | Нет |
| 631/tcp | CUPS 1.7 | CVE-2014-5030 | 1.9 | Нет |
| 631/tcp | CUPS 1.7 | CVE-2014-3537 | 1.2 | Нет |
| 631/tcp | CUPS 1.7 | CVE-2013-6891 | 1.2 | Нет |
| 631/tcp | CUPS 1.7 | Slowloris DoS (CVE-2007-6750) | — | Уязвим |
| 3306/tcp | MySQL | Неавторизованный доступ | — | Любой клиент MySQL |
| 3500/tcp | WEBrick 1.3.1 (Ruby 2.3.8) | CVE-2017-9225 | 9.8 | Есть |
| 3500/tcp | WEBrick 1.3.1 (Ruby 2.3.8) | CVE-2022-28739 | 7.5 | Нет |
| 3500/tcp | WEBrick 1.3.1 (Ruby 2.3.8) | CVE-2021-41819 | 7.5 | Нет |
| 3500/tcp | WEBrick 1.3.1 (Ruby 2.3.8) | CVE-2021-28966 | 7.5 | Нет |
| 3500/tcp | WEBrick 1.3.1 (Ruby 2.3.8) | CVE-2021-28965 | 7.5 | Нет |
| 3500/tcp | WEBrick 1.3.1 (Ruby 2.3.8) | CVE-2020-25613 | 7.5 | Нет |
| 3500/tcp | WEBrick 1.3.1 (Ruby 2.3.8) | CVE-2017-9229 | 7.5 | Есть |
| 3500/tcp | WEBrick 1.3.1 (Ruby 2.3.8) | CVE-2015-9096 | 6.1 | Нет |
| 3500/tcp | WEBrick 1.3.1 (Ruby 2.3.8) | CVE-2021-31810 | 5.8 | Нет |
| 3500/tcp | WEBrick 1.3.1 (Ruby 2.3.8) | CVE-2023-28756 | 5.3 | Нет |
| 3500/tcp | WEBrick 1.3.1 (Ruby 2.3.8) | Slowloris DoS (CVE-2007-6750) | — | Уязвим |
| 6697/tcp | UnrealIRCd | Троянизированная версия (backdoor) | 10.0 | Metasploit |
| 8080/tcp | Jetty 8.1.7 | CSRF | — | Встроенный скрипт nmap |
| 8080/tcp | Jetty 8.1.7 | Slowloris DoS (CVE-2007-6750) | — | Уязвим |

### 3) Узел `OpenWrt.lan`

<img width="786" height="527" alt="изображение" src="https://github.com/user-attachments/assets/59b5862d-9307-4a61-b670-061a4c5b028d" />

### Уязвимости

- Ничего конкретного не было найдено
