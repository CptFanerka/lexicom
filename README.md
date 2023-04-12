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
uvicorn main:app --host localhost --port 8000
```
# Задача 2
Дано две таблицы в СУБД Postgres.  

В одной таблице хранятся имена файлов без расширения. В другой хранятся имена файлов с расширением. Одинаковых названий с разными расширениями быть не может, количество расширений не определено, помимо wav и mp3 может встретиться что угодно.  

Нам необходимо минимальным количеством запросов к СУБД перенести данные о статусе из таблицы short_names в таблицу full_names. Необходимо понимать, что на выполнение запросов / время работы скрипта нельзя тратить больше 10 минут.
## Запуск
Скопировать содержимое файла **sql_queries.txt** из папки lexicom, вставить в терминал **psql** и запустить
### Комментарий
Добавление данных в таблицу full_names не является элегантным, и написано только для проверки работоспособности скрипта.  
Более интересным и сложным было бы решение с использованием unnest(ARRAY['mp3','wav', 'mkv', 'avi', 'mov']) и CROSS JOIN, но это потребовало бы больше времени на продумывание запроса, при том, что заполнение данных не является основной задачей скрипта.
Основное решение представлено в этих строках:
```
CREATE INDEX IF NOT EXISTS short_names_name_index ON short_names (name);
CREATE INDEX IF NOT EXISTS full_names_name_index ON full_names (name);
UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE split_part(full_names.name, '.', 1) = short_names.name;
```
Для ускорения запросов создаются индексы по name в каждой таблице. Затем в UPDATE обновляется full_names.status, при условии, что full_names.name до разделителя-точки совпадает с short_names.name  
Результаты запуска: 
```
lexicom_database=# CREATE INDEX IF NOT EXISTS short_names_name_index ON short_names (name);
CREATE INDEX
Время: 4510,976 мс (00:04,511)

lexicom_database=# CREATE INDEX IF NOT EXISTS full_names_name_index ON full_names (name);
CREATE INDEX
Время: 3716,245 мс (00:03,716)

lexicom_database=# UPDATE full_names
lexicom_database-# SET status = short_names.status
lexicom_database-# FROM short_names
lexicom_database-# WHERE split_part(full_names.name, '.', 1) = short_names.name;
UPDATE 500000
Время: 10969,244 мс (00:10,969)
```
