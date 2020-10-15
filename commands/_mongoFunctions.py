import os
import pymongo
import datetime
from dotenv import load_dotenv
from commands import _hashingFunctions

load_dotenv()

CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")

mClient = None
GuildInformation = None
Guilds = None


def init():
    global mClient
    global Guilds
    global GuildInformation

    mClient = pymongo.MongoClient(CONNECTION_STRING)

    GuildInformation = mClient['GuildInformation']

    Guilds = GuildInformation['Guilds']

    guild_list = list(Guilds.find({}))

    for guild in guild_list:
        for key, value in guild.items():
            if key == 'guild_id':
                coll = GuildInformation["a" + value + ".PendingVerificationUsers"]
                coll.delete_many({})


def is_email_linked_to_verified_user(guild_id, email_address):
    coll = GuildInformation["a" + str(guild_id) + ".VerifiedUsers"]
    email_address_hash = _hashingFunctions.hash_email(email_address)
    print(email_address_hash)
    if coll.find_one({"email_address_hash": email_address_hash}) is None:
        return False
    return True


def is_user_id_linked_to_verified_user(guild_id, user_id):
    coll = GuildInformation["a" + str(guild_id) + ".VerifiedUsers"]
    if coll.find_one({"user_id": user_id}) is None:
        return False
    return True


def remove_verified_user(guild_id, user_id):
    coll = GuildInformation["a" + str(guild_id) + ".VerifiedUsers"]
    if coll.find_one_and_delete({"user_id": user_id}) is None:
        return False
    return True


def add_user_to_verified_users(guild_id, user_id, email_address_hash):
    coll = GuildInformation["a" + str(guild_id) + ".VerifiedUsers"]
    coll.insert_one({'user_id': user_id, 'email_address_hash': email_address_hash})


def add_user_to_pending_verification_users(guild_id, user_id, email):
    coll = GuildInformation["a" + str(guild_id) + ".PendingVerificationUsers"]
    email_address_hash = _hashingFunctions.hash_email(email)
    print(email_address_hash)
    coll.insert_one({'user_id': user_id, 'email_address_hash': email_address_hash})


def remove_user_from_pending_verification_users(guild_id, user_id):
    coll = GuildInformation["a" + str(guild_id) + ".PendingVerificationUsers"]
    coll.find_one_and_delete({'user_id': user_id})


def get_email_hash_from_pending_user_id(guild_id, user_id):
    coll = GuildInformation["a" + str(guild_id) + ".PendingVerificationUsers"]
    document = coll.find_one({'user_id': user_id})
    if document is not None:
        return document['email_address_hash']


def set_users_birthday(guild_id, user_id, birth_date):
    coll = GuildInformation["a" + str(guild_id) + ".VerifiedUsers"]
    coll.update_one({'user_id': user_id}, {'$set': {'birth_date': birth_date}})


def get_all_birthdays_today(guild_id):
    coll = GuildInformation["a" + str(guild_id) + ".VerifiedUsers"]
    return list(coll.aggregate([
        {'$match':
            {'$expr':
                {'$and': [
                    {'$eq': [{'$dayOfMonth': '$birth_date'}, datetime.date.today().day]},
                    {'$eq': [{'$month': '$birth_date'}, datetime.date.today().month]}, ], },
            }
        }]))


def add_due_date_to_upcoming_due_dates(guild_id, course, due_date_type, title, stream, date, timeIncluded):
    coll = GuildInformation["a" + str(guild_id) + ".UpcomingDueDates"]
    coll.insert_one({'course': course, 'type': due_date_type, 'title': title, 'stream': stream, 'date': date, "time_included": timeIncluded})


def get_all_upcoming_due_dates(guild_id, stream, course):
    coll = GuildInformation["a" + str(guild_id) + ".UpcomingDueDates"]

    filter = {
        "stream": str(stream),
        "course": course
    }
    pipeline = [
        {"$match": filter},
        {'$sort': {'date': 1}}
    ]

    return list(coll.aggregate(pipeline))


def get_list_of_courses(guild_id):
    return Guilds.find_one({'guild_id': str(guild_id)})['courses']


def get_guilds_information():
    return list(Guilds.find({}))


def get_due_date_channel_id(guild_id, stream):
    return Guilds.find_one({'guild_id': str(guild_id)})['stream_' + str(stream) + '_message_id']


def remove_due_dates_passed(guild_id):
    coll = GuildInformation["a" + str(guild_id) + ".UpcomingDueDates"]
    query = {"date": {"$lte": datetime.datetime.now()}}

    coll.delete_many(query)
