import asyncio
import os
from typing import List, Tuple
from datetime import datetime
from getpass import getpass

from loggers import logger
from utils.Group import Group
from utils.User import User
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon import functions, types
from utils import newresources

code_dialog = False
connected = False

def geolocate_AllEntities_Nearby(api_id: str, 
                                 api_hash: str, 
                                 phone_number: str, 
                                 latitude: float, 
                                 longitude: float, 
                                 dir_name: str) -> Tuple[List[User], List[Group], str]:
    global code_dialog, connected
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        os.mkdir(dir_name)
    except OSError:
        logger.warning("Neogramint Files: folder already exist")
    client = TelegramClient("Neogramint", api_id, api_hash, device_model="A320MH", app_version="2.1.4a",
                            system_version="Windows 10", lang_code="en", system_lang_code="fr-FR", loop=loop)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone_number)  # message send by Telegram with verification code
        code_dialog = True
        while True:  # authentication
            try:
                code = input("Введите код для входа в Telegram: ")
                if code is not None:
                    client.sign_in(phone=phone_number, code=code)
                if client.is_user_authorized():
                    code_dialog = False
                    connected = True
                    break
            except SessionPasswordNeededError:  # if the user have 2FA auth
                while True:
                    try:
                        password = getpass(prompt="Введите пароль: ")
                        client.sign_in(phone=phone_number, password=password)
                        if client.is_user_authorized():
                            code_dialog = False
                            connected = True
                            break
                    except:  # if the password is wrong
                        password = None
                        code = None
                        code_dialog = True
                        continue
            except:  # if code is wrong
                password = None
                code = None
                code_dialog = True
                continue
        code_dialog = False
        connected = True
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    result = client(functions.contacts.GetLocatedRequest(
        geo_point=types.InputGeoPoint(
            lat=latitude,
            long=longitude
        ),
        self_expires=42
    ))
    res = result.stringify()

    # parse the result of the API request and Isolate important components
    usersList = newresources.isolation_Users(res)
    peersList = newresources.isolation_Peers(res)
    channelsList = newresources.isolation_Channels(res)

    # Create List of Objects from the isolated components
    list_of_group = newresources.generate_ListOfGroups(channelsList, peersList)
    list_of_user = newresources.generate_ListOfUsers(usersList, peersList)
    newresources.download_allprofilespics(client, list_of_user, list_of_group, dir_name)
    client.disconnect()

    return list_of_user, list_of_group, dt_string
