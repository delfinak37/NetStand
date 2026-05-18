# Перехват сетевого трафика

## Wireshark

Запуск **Wireshark** и проверка отслеживания:

<img width="1055" height="663" alt="изображение" src="https://github.com/user-attachments/assets/5dd7f864-774e-4cab-9673-238dc19e7c83" />

Очистка **APR-кеша** и выполнение ping запроса

<img width="1057" height="525" alt="изображение" src="https://github.com/user-attachments/assets/9d4ac9c6-19c0-4221-b5fd-b2b866129bb7" />

## ARP broadcast запрос

<img width="1465" height="630" alt="изображение" src="https://github.com/user-attachments/assets/5d11200a-a8fa-43c5-b9cb-e6019d76acd0" />

## ARP ответ

<img width="1464" height="607" alt="изображение" src="https://github.com/user-attachments/assets/bed93660-bc4c-451d-9afb-f1e2e3cde031" />

## ICMP запрос

<img width="1471" height="729" alt="изображение" src="https://github.com/user-attachments/assets/d5842910-ac18-4270-a7ea-4ad471b29223" />

## ICMP ответ

<img width="1463" height="745" alt="изображение" src="https://github.com/user-attachments/assets/194ce186-ab64-47a3-870a-0ea5c39c90ae" />

## TCP

Прослушивание через **netcat** на `Kali`:

<img width="210" height="69" alt="изображение" src="https://github.com/user-attachments/assets/8406a08b-846a-454f-800c-714c561898ae" />

В **Wireshark** появилось несколько записей:

<img width="1677" height="433" alt="изображение" src="https://github.com/user-attachments/assets/504f28e7-8e58-49be-adbf-a4a100781650" />

- **Установка соединения**
    - 935: SYN
    - 936: SYN, ACK
    - 937: ACK
 
- **Переданное сообщение**
    - 940: PSH, ACK
    - 941: ACK

- **Завершение соединения**
    - 946: ACK

Перехваченное сообщение находится сегменте `data`:

<img width="1601" height="591" alt="изображение" src="https://github.com/user-attachments/assets/29844375-40ec-4bf4-867a-c6cd50bec631" />
