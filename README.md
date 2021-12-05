# команда Odysseus
Московский транспортный хакатон

Установка среды
I. Подготовка
1. Установить последнюю версию Anaconda вашу систему
https://www.anaconda.com/products/individual

◦ Установить среду для работы
Необходимо обновить conda и anaconda и установить окружение.

Для этого:

◦ Для Windows, выбираем через Start и находим папку anaconda,
и в ней command prompt (НЕ Powershell)

◦ Для ubuntu запускаем Terminal

◦ В обоих случаях слева от приглашения, должно быть написано "base"]

◦ Набираем по одной строке и нажимаем ввод, дожидаемся приглашения
и вводим следующую строку. Могут быть вопросы типа (Y/n), жмем смело y

◦ conda update conda

◦ conda update anaconda

2. сделаем клон проекта с Github
gh repo clone team-odysseus/odysseus

3. Установим окружение

◦ conda env create "путь_к_папке_с_проектом"/odysseus-base.yml

◦ conda activate odysseus-base

Запуск первой части:
cd "путь_к_папке_с_проектом"/quiz
python quizmain.py

Запуск второй части:
.env по образцу example.env.txt
python3 cyber_krot_main.py
