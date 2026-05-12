# Стенд системы

## Основные задачи

  1) Настройка роутера для выхода в интернет
  2) Настройка локальных узлов (Windows, Metasploitable) в локальной сети
  3) Подключение Kali к локальной сети

## Используемое ПО

В работе используются следующие системы:

  - **OpenWrt** - в роли маршрутизатора
  - **Kali Linux** - атакующая машина
  - **Ubuntu Server** - сервер
  - **Metasploitable** - уязвимая система

## Настройка роутера OpenWrt

Создание виртуального роутера в `Vmware`, настройка сетевых интерфейсов на устройстве:

- NetworkAdapter - `NAT`
- NetworkAdapter 2 - `LAN Segment(LAN)`
- NetworkAdapter 3 - `LAN Segment(DMZ)`
- NetworkAdapter 4 - `LAN Segment(NET)`

<img width="300" height="370" alt="изображение" src="https://github.com/user-attachments/assets/8deefdbc-4509-44ec-9ea7-1713eaec6afd" />

Добавление сетевых интерфейсов `lan`, `dmz`, `net` в `/etc/config/network`, присваивание статических адресов:

<img width="576" height="497" alt="изображение" src="https://github.com/user-attachments/assets/fb03e61c-a789-4a68-8ebf-839c703adb93" />

Настройка DHCP в `/etc/config/dhcp`:

<img width="317" height="506" alt="изображение" src="https://github.com/user-attachments/assets/6c3c389b-8ae7-4eb5-a9d1-1595b9bfb8e8" />

Настройка межсетевого экрана в `/etc/config/firewall`, для `lan`, `dmz`, `net` одинаковые параметры, исключение `lan` - разрешены входящие от него сообщения:

<img width="343" height="407" alt="изображение" src="https://github.com/user-attachments/assets/5bf7266a-7c6c-483c-ab4f-88d5317e9a08" />

Тут же настройка `forwarding`. Все видят `wan`, взаимно общаются пары `lan`-`dmz` и `net`-`dmz`, и лишь `net` видит `lan`:

<img width="343" height="534" alt="изображение" src="https://github.com/user-attachments/assets/3c765efe-171a-4e77-943e-1852ec3d885c" />

После блокировки роутера DHCP и DNS тоже заблокировались. Добавление правил для их разрешения:

<img width="314" height="445" alt="изображение" src="https://github.com/user-attachments/assets/8e448c9f-32ff-4215-a313-67c93501319b" />

По итогу:

- WAN
  - изолирован
  - каждый имеет доступ в интернет

- LAN
  - Запрещён доступ к NET
  - Разрешён доступ к DMZ
  - Разрешён доступ к роутеру

- NET
  - Разрешён доступ к DMZ
  - Разрешён доступ к LAN
  - Запрещён доступ к роутеру

- DMZ
  - Разрешён доступ к NET
  - Разрешён доступ к LAN
  - Запрещён доступ к роутеру
