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

Создаем виртуальный роутер в `Vmware`, также настраиваем сетевые интерфейсы на устройстве:

- NetworkAdapter - `NAT`
- NetworkAdapter 2 - `LAN Segment(LAN)`
- NetworkAdapter 3 - `LAN Segment(DMZ)`
- NetworkAdapter 4 - `LAN Segment(NET)`

<img width="300" height="370" alt="изображение" src="https://github.com/user-attachments/assets/8deefdbc-4509-44ec-9ea7-1713eaec6afd" />

Добавляем сетевые интерфейсы `lan`, `dmz`, `net`, задаем статические адреса:

<img width="731" height="424" alt="изображение" src="https://github.com/user-attachments/assets/04031c1a-09ad-4dc2-b576-a9948b9f897c" />

