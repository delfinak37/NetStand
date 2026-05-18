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

<img width="1680" height="242" alt="изображение" src="https://github.com/user-attachments/assets/4596a0d4-7db7-4977-b698-d10ea473c300" />

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

## Перехват пароля

Переход к web-интерфейсу настроек роутера:

<img width="809" height="608" alt="изображение" src="https://github.com/user-attachments/assets/e79cc89f-c713-4b5c-9a9d-415c1b8ab191" />

В **Wireshark** появилась запись, содержащия учетные данные роутера:

<img width="1920" height="771" alt="изображение" src="https://github.com/user-attachments/assets/507fb935-1b45-4a19-b7e5-62f27e8f3c21" />
