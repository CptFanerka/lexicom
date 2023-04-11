# Тестовое задание для компании Lexicom
[Ссылка на полный текст задания](https://disk.yandex.ru/i/xSAO9-HPiKs8Eg)
## Задача 1
Необходимо разработать RESTful сервис с использованием Fast API и Redis.  

**Эндпоинты (ручки):**  
**Write_data** (запись и обновление данных)  
```
    a. Phone  
    b. Address  
```
**Check_data** (получение данных)  
```
    a. Phone  
```
Сценарии использования сервиса:  
1. Клиент отправляет запрос на ручку вида https://111.111.111.111/check_data?phone='89090000000'  
Эндпоинт в свою очередь получает номер телефона и идёт в redis по ключу (номер телефона) получает сохраненный адрес и отдаёт его в ответе клиенту.
2. Клиент отправляет запрос на ручку для записи данных в redis вида https://111.111.111.111/write_data с телом 
```
    phone:'89090000000'
    address:'текстовый адрес'
```
3. Клиент отправляет запрос на ручку изменения адреса вида https://111.111.111.111/write_data с телом
```
    phone:'89090000000'
    address:'текстовый адрес'
```

## Установка и запуск
**Вариант 1: Docker**
```
git clone https://github.com/cptfanerka/lexicom.git
cd lexicom
docker build -t simple_service_image .
docker run -p 80:80 simple_service_image
```
**Вариант 2: Python**
```
git clone https://github.com/cptfanerka/lexicom.git
cd lexicom
pip install -r requirements.txt
cd src
uvicorn main:app --host 0.0.0.0 --port 8000
```
# Задача 2
Дано две таблицы в СУБД Postgres.  

В одной таблице хранятся имена файлов без расширения. В другой хранятся имена файлов с расширением. Одинаковых названий с разными расширениями быть не может, количество расширений не определено, помимо wav и mp3 может встретиться что угодно.  

Нам необходимо минимальным количеством запросов к СУБД перенести данные о статусе из таблицы short_names в таблицу full_names. Необходимо понимать, что на выполнение запросов / время работы скрипта нельзя тратить больше 10 минут.
## Установка и запуск
**Python**
```
git clone https://github.com/cptfanerka/lexicom.git
cd lexicom
pip install -r requirements.txt
cd src
python sql_queries.py
```