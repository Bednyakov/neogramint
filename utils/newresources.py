import os
from utils import Group
from utils import User
from loggers import logger


def isolation_Users(res):
    usersStrtIndex = str.find(res, "users=[")
    usersEndIndex = str.find(res, "\n\t],", usersStrtIndex)
    usersList = res[usersStrtIndex:usersEndIndex + len("\n\t]")]
    return usersList

def isolation_Channels(res):
    channelsStrtIndex = str.find(res, "chats=[")
    channelsEndIndex = str.find(res, "\n\t],", channelsStrtIndex)
    channelsList = res[channelsStrtIndex:channelsEndIndex + len("\n\t]")]
    return channelsList

def isolation_Peers(res):
    peersStrtIndex = str.find(res, "peers=[")
    peersEndIndex = str.find(res, "\n\t],", peersStrtIndex)
    peersList = res[peersStrtIndex:peersEndIndex + len("\n\t]")]
    return peersList

def find_param(res, start):
    end = str.find(res, ",", start)
    return res[start:end]

def find_dist(res, start):
    end = str.find(res, "\n", start)
    return res[start:end]

def generate_ListOfUsers(usersList, peersList):
    output = []
    i = 0
    while (i != -1):
        # parse elements to create a User Object in the Users Isolation
        i = str.find(usersList, "\tid=", i)
        uid = find_param(usersList, i + len("\tid="))
        i = str.find(usersList, "first_name=", i)
        firstname = find_param(usersList, i + len("first_name="))
        i = str.find(usersList, "last_name=", i)
        lastname = find_param(usersList, i + len("last_name="))
        i = str.find(usersList, "username=", i)
        username = find_param(usersList, i + len("username="))
        i = str.find(usersList, "phone=", i)
        phone = find_param(usersList, i + len("phone="))

        # parse elements to create User Object in the Peers Isolation
        j = str.find(peersList, uid)
        j = str.find(peersList, "distance=", j)
        distance = find_dist(peersList, j + len("distance="))

        # Adding new User to the List of User Objects
        output.append(User.User(uid, distance, username, firstname, lastname, phone))

        # Test if end of File
        i = str.find(usersList, "\tid=", i)

    # Cleaning attributes of User Object
    for elm in output:
        if elm.id == 'None':
            elm.id = None
        if elm.distance == 'None':
            elm.distance = None
        if elm.firstname == 'None':
            elm.firstname = None
        if elm.lastname == 'None':
            elm.lastname = None
        if elm.username == 'None':
            elm.username = None
        if elm.phone == 'None':
            elm.phone = None

    return output

def generate_ListOfGroups(groupList, peersList):
    output = []
    i = 0
    while (i != -1):
        # parse elements to create a Group Object in the Channels Isolation
        i = str.find(groupList, "\tid=", i)
        uid = find_param(groupList, i + len("\tid="))
        i = str.find(groupList, "title=", i)
        name = find_param(groupList, i + len("title="))

        # parse elements to create Group Object in the Peers Isolation
        j = str.find(peersList, uid)
        j = str.find(peersList, "distance=", j)
        distance = find_dist(peersList, j + len("distance="))

        # Adding new Group to the List of Group Objects
        output.append(Group.Group(uid, distance, name))

        # Test if end of File
        i = str.find(groupList, "\tid=", i)

    # Cleaning attributes of Group Object
    for elm in output:
        if elm.id == 'None':
            elm.id = None
        if elm.distance == 'None':
            elm.distance = None
        if elm.name == 'None':
            elm.name = None

    return output

def download_allprofilespics(client, ListofUser, ListofGroup, dir_name: str):
    # create cache file for users profiles pictures
    try:
        os.mkdir(f"{dir_name}/users")
    except OSError as error:
        logger.warning(f"Neogramint Files: {error}")

    # create cache file for groups profiles pictures
    try:
        os.mkdir(f"{dir_name}/groups")
    except OSError as error:
        logger.warning(f"Neogramint Files: {error}")

    # verification of the contents of User and Group objects
    invalid_objects = True
    while invalid_objects:
        invalid_objects = False
        if len(ListofUser) > 0 and not ListofUser[0].id.isnumeric():
            ListofUser.pop(0)
            invalid_objects = True
        if len(ListofGroup) > 0 and not ListofGroup[0].id.isnumeric():
            ListofGroup.pop(0)
            invalid_objects = True
    if len(ListofUser) == 0 and len(ListofGroup) == 0:
        raise Exception

    # download of users profile pics
    for elm in ListofUser:
        if not elm.id.isnumeric():
            continue
        client.download_profile_photo(int(elm.id), f"{dir_name}/users/" + elm.id)

    # download of groups profile pics
    for elm in ListofGroup:
        if not elm.id.isnumeric():
            continue
        client.download_profile_photo(int(elm.id), f"{dir_name}/groups/" + elm.id)