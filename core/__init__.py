from core.TelegramAPIRequests import geolocate_AllEntities_Nearby
from loggers import logger
from time import time

dirname = str(int(time()))


def main():
    api_id = input("Введите API ID: ")
    api_hash = input("Введите API Hash: ")
    phone_number = input("Введите номер телефона: ")

    while True:
        latitude = float(input("Введите широту: "))
        longitude = float(input("Введите долготу: "))

        users, groups, timestamp = geolocate_AllEntities_Nearby(api_id, api_hash, phone_number, latitude, longitude, dirname)

        logger.info(f"Пользователи: {len(users)}")
        logger.info(f"Группы: {len(groups)}")
        logger.info(f"Время выполнения: {timestamp}")