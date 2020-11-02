import os
import pymongo
import datetime
from dotenv import load_dotenv
from commands import _hashingFunctions

load_dotenv()

CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
DATABASE_STRING = os.getenv("MONGO_DATABASE_STRING")

mClient = None
GuildInformation = None
Guilds = None


def init():
    global mClient
    global Guilds
    global GuildInformation

    mClient = pymongo.MongoClient(CONNECTION_STRING)

    GuildInformation = mClient[DATABASE_STRING]

    Guilds = GuildInformation['Guilds']

    guild_list = list(Guilds.find({}))

    for guild in guild_list:
        for key, value in guild.items():
            if key == 'guild_id':
                coll = GuildInformation["a" + str(value) + ".PendingVerificationUsers"]
                coll.delete_many({})


def is_uw_id_linked_to_verified_user(guild_id: int, uw_id):
    coll = GuildInformation["a" + str(guild_id) + ".VerifiedUsers"]
    uw_id_hash = _hashingFunctions.hash_user_id(uw_id)
    if coll.find_one({"uw_id": uw_id_hash}) is None:
        return False
    return True


def is_uw_id_linked_to_pending_verification_user(guild_id: int, uw_id):
    coll = GuildInformation["a" + str(guild_id) + ".PendingVerificationUsers"]
    if coll.find_one({"uw_id": uw_id}) is None:
        return False
    return True


def is_user_id_linked_to_verified_user(guild_id: int, user_id: int):
    coll = GuildInformation["a" + str(guild_id) + ".VerifiedUsers"]
    if coll.find_one({"user_id": int(user_id)}) is None:
        return False
    return True


def remove_verified_user(guild_id: int, user_id: int):
    coll = GuildInformation["a" + str(guild_id) + ".VerifiedUsers"]
    if coll.find_one_and_delete({"user_id": int(user_id)}) is None:
        return False
    return True


def add_user_to_verified_users(guild_id: int, user_id: int, uw_id_hash):
    coll = GuildInformation["a" + str(guild_id) + ".VerifiedUsers"]
    coll.insert_one({'user_id': int(user_id), 'uw_id': uw_id_hash})


def admin_add_user_to_verified_users(guild_id: int, user_id: int):
    coll = GuildInformation["a" + str(guild_id) + ".VerifiedUsers"]
    coll.insert_one({'user_id': int(user_id)})


def add_user_to_pending_verification_users(guild_id: int, user_id: int, uw_id):
    coll = GuildInformation["a" + str(guild_id) + ".PendingVerificationUsers"]
    coll.insert_one({'user_id': int(user_id), 'uw_id': uw_id})


def remove_user_from_pending_verification_users(guild_id: int, user_id: int):
    coll = GuildInformation["a" + str(guild_id) + ".PendingVerificationUsers"]
    coll.find_one_and_delete({'user_id': int(user_id)})


def get_uw_id_from_pending_user_id(guild_id: int, user_id: int):
    coll = GuildInformation["a" + str(guild_id) + ".PendingVerificationUsers"]
    document = coll.find_one({'user_id': int(user_id)})
    if document is not None:
        return document['uw_id']


def set_users_birthday(guild_id: int, user_id: int, birth_date: datetime.datetime):
    coll = GuildInformation["a" + str(guild_id) + ".VerifiedUsers"]
    coll.update_one({'user_id': int(user_id)}, {'$set': {'birth_date': birth_date}})


def get_all_birthdays_today(guild_id: int):
    coll = GuildInformation["a" + str(guild_id) + ".VerifiedUsers"]
    return list(coll.aggregate([
        {'$match':
            {'$expr':
                {'$and': [
                    {'$eq': [{'$dayOfMonth': '$birth_date'}, datetime.date.today().day]},
                    {'$eq': [{'$month': '$birth_date'}, datetime.date.today().month]}, ], },
            }
        }]))


def add_due_date_to_upcoming_due_dates(guild_id: int, course, due_date_type, title, stream: int, date: datetime.datetime, timeIncluded: bool):
    coll = GuildInformation["a" + str(guild_id) + ".UpcomingDueDates"]
    coll.insert_one({'course': course, 'type': due_date_type, 'title': title, 'stream': int(stream), 'date': date, "time_included": bool(timeIncluded)})


def get_all_upcoming_due_dates(guild_id: int, stream: int, course):
    coll = GuildInformation["a" + str(guild_id) + ".UpcomingDueDates"]

    filter = {
        "stream": int(stream),
        "course": course
    }
    pipeline = [
        {"$match": filter},
        {'$sort': {'date': 1}}
    ]

    return list(coll.aggregate(pipeline))


def get_list_of_courses(guild_id: int):
    return Guilds.find_one({'guild_id': guild_id})['courses']


def get_list_of_due_date_types(guild_id: int):
    return Guilds.find_one({'guild_id': guild_id})['due_date_types']


def get_list_of_streams(guild_id: int):
    return Guilds.find_one({'guild_id': guild_id})['streams']


def get_guilds_information():
    return list(Guilds.find({}))


def get_due_date_channel_id(guild_id: int, stream: int):
    return Guilds.find_one({'guild_id': guild_id})['stream_' + str(stream) + '_message_id']


def remove_due_dates_passed(guild_id: int):
    coll = GuildInformation["a" + str(guild_id) + ".UpcomingDueDates"]
    query = {"date": {"$lte": datetime.datetime.now()}}

    coll.delete_many(query)


def does_assignment_exist_already(guild_id: int, course, due_date_type, title, stream: int, date: datetime.datetime, time_included: bool):
    coll = GuildInformation["a" + str(guild_id) + ".UpcomingDueDates"]
    if coll.find_one(
            {'course': course, 'type': due_date_type, 'title': title, 'stream': int(stream), 'date': date, 'time_included': bool(time_included)}) is None:
        return False
    return True


def set_bedi_bot_channel_id(guild_id: int, channel_id: int):
    Guilds.update_one({'guild_id': guild_id}, {'$set': {'channel_id': int(channel_id)}})
    Guilds.update_one({'guild_id': guild_id}, {'$set': {'last_announcement_time': None}})


def set_due_date_message_id(guild_id: int, stream: int, message_id: int):
    Guilds.update_one({'guild_id': guild_id}, {'$set': {'stream_' + str(stream) + '_message_id': message_id}})


def set_last_announcement_time(guild_id: int, time: datetime.datetime):
    Guilds.update_one({'guild_id': guild_id}, {'$set': {'last_announcement_time': time}})


def get_last_announcement_time(guild_id: int):
    return Guilds.find_one({'guild_id': guild_id})['last_announcement_time']


def insertQuote(guildId: int, quote: str, quotedPerson: str):
    doc = {
        'quote': quote,
        'name': quotedPerson.lower()
    }
    coll = GuildInformation["a" + str(guildId) + ".quotes"]
    coll.insert_one(doc)
    try:
        return True
    except:
        return False


def deleteQuote(guildId, quote, quotedPerson):
    coll = GuildInformation["a" + guildId + ".quotes"]
    coll.delete_one({"quote": quote, "name": quotedPerson})


perPage = 5


def findQuotes(guildId, quotedPerson, page):
    skip = perPage * (page - 1)
    coll = GuildInformation["a" + str(guildId) + ".quotes"]
    filter = {
        "name": {"$regex": "^.*" + quotedPerson.lower() + ".*$"}
    }
    pipeline = [
        {"$match": filter},
        {"$skip": skip},
        {"$limit": perPage},
    ]
    try:
        return list(coll.aggregate(pipeline))
    except Exception as e:
        print(e)
        return None


def randomQuote(guildId, quotedPerson):
    coll = GuildInformation["a" + str(guildId) + ".quotes"]
    filter = {
        "name": {"$regex": "^.*" + quotedPerson.lower() + ".*$"}
    }

    # print(quotedPerson)
    pipeline = [
        {"$match": filter},
        {"$sample": {"size": 1}},
    ]
    try:
        quote = list(coll.aggregate(pipeline))[0]
        return '"' + quote["quote"] + '"  - ' + quote["name"]
    except Exception as e:
        print(e)
        return None
