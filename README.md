# neogramint
OSINT parser of telegram users and groups by location

## Установка и запуск приложения:
1. Скачайте репозиторий
2. Запустите контейнер с MongoDB:
   ```bash
   docker run -d --name mongo_container -p 27017:27017 mongo
   ```
3. Запустите neogramint.py

### Инструкция по запуску Docker-контейнера приложения

1. **Создание Docker образа**  
   Скачайте репозиторий. В директории проекта выполните команду для создания образа:
   ```bash
   docker build -t neogramint_app .
   ```

2. **Запуск контейнеров**  
   Запустите контейнер с MongoDB:
   ```bash
   docker run -d --name mongo_container -p 27017:27017 mongo
   ```
   Запустите контейнер с Neogramint:
   ```bash
   docker run -d -p 5000:5000 --name neogramint_container neogramint_app
   ```

   - `-d` —  фоновый режим. 
   - `-p 27017:27017` — проброс порта MongoDB (27017).
   - `--name neogramint_container` — имя контейнера.

3. **Подключение к контейнеру**  
   Для подключения к контейнеру выполните:
   ```bash
   docker exec -it neogramint_container bash
   ```

4. **Запуск приложения**  
   ```bash
   python3 neogramint.py
   ```

### Управление базой данных через MongoDB Shell

MongoDB запускается вместе с контейнером, и можно использовать встроенный MongoDB shell для управления базой данных.

1. Подключитесь к контейнеру:
   ```bash
   docker exec -it mongodb_container bash
   ```

2. Подключитесь к MongoDB через shell:
   ```bash
   mongosh
   ```

3. В интерфейсе MongoDB вы можете выполнять команды для создания, удаления баз данных и коллекций. Например:

   - Создать или использовать базу данных:
     ```bash
     use mydatabase
     ```

   - Посмотреть список баз данных:
     ```bash
     show dbs
     ```

   - Посмотреть коллекции в базе данных:
     ```bash
     show collections
     ```

   - Добавить данные:
     ```bash
     db.mycollection.insert({name: "Artem", age: 30})
     ```

   - Посмотреть содержимое коллекции:
     ```bash
     db.mycollection.find()
     ```

3. Для выхода из MongoDB shell введите `exit`.

### Остановка и удаление контейнера

- Остановка контейнера:
  ```bash
  docker stop neogramint_container
  ```

- Удаление контейнера:
  ```bash
  docker rm neogramint_container
  ```

- Удаление Docker образа:
  ```bash
  docker rmi neogramint_mongodb
  ```

