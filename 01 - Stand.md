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

Добавляем сетевые интерфейсы `lan`, `dmz`, `net` в **/etc/config/networ**, задаем статические адреса:

<img width="717" height="401" alt="изображение" src="https://github.com/user-attachments/assets/806355c5-06ad-45a7-91a5-bd5fa317eebf" />
<img width="730" height="162" alt="изображение" src="https://github.com/user-attachments/assets/a621940c-38da-4482-a7cf-63b09ae60ad1" />

Настраиваем DHCP в **/etc/config/dhcp**:

<img width="726" height="374" alt="изображение" src="https://github.com/user-attachments/assets/1bdb49ee-a907-412d-931d-5247a073e5d4" />
<img width="731" height="141" alt="изображение" src="https://github.com/user-attachments/assets/5a0d098c-0a21-486a-ac07-0fc1355eeb77" />


