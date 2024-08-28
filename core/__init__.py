from core.TelegramAPIRequests import geolocate_AllEntities_Nearby
from db_manager import DBManager
from loggers import logger
from time import time

dirname = 'photos/' + str(int(time()))


def main() -> None:
    api_id = input("Введите API ID: ")
    api_hash = input("Введите API Hash: ")
    phone_number = input("Введите номер телефона: ")
    db_name = input("Введиите название базы данных: ")

    try:
        db = DBManager(db_name=db_name)
        users_collection = db.create_collection("users")
        groups_collection = db.create_collection("groups")
    except Exception as e:
        logger.error(e)

    while True:
        latitude = float(input("Введите широту: "))
        longitude = float(input("Введите долготу: "))

        users, groups, timestamp = geolocate_AllEntities_Nearby(api_id, 
                                                                api_hash, 
                                                                phone_number, 
                                                                latitude, 
                                                                longitude, 
                                                                dirname)
        
        for user in users:
            user_data = {
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'username': user.username,
                'phone': user.phone,
                'distance': user.distance,
                'timestamp': timestamp,
                'latitude': latitude,
                'longitude': longitude,}
            users_collection.insert_one(user_data)

        for group in groups:
            group_data = {
                'id': group.id,
                'name': group.name,
                'distance': group.distance,
                'timestamp': timestamp,
                'latitude': latitude,
                'longitude': longitude,}
            groups_collection.insert_one(group_data)


        logger.info(f"Пользователи: {len(users)} добавлены в коллекцию 'users'")
        logger.info(f"Группы: {len(groups)} добавлены в коллекцию 'groups'")
        logger.info(f"Время выполнения: {timestamp}")
        logger.info(f"Изображения сохранены в {dirname}")