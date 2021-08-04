import asyncio
import datetime
import os
import threading

import discord
import pymongo
from dotenv import load_dotenv

from commands import _hashingFunctions, _scheduling

load_dotenv()

CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
DATABASE_STRING = os.getenv("MONGO_DATABASE_STRING")


async def init(client: discord.Client):
    global mClient, Guilds, GuildInformation, Settings_Cache

    mClient = pymongo.MongoClient(CONNECTION_STRING)

    GuildInformation = mClient.get_database(DATABASE_STRING)

    Guilds = GuildInformation.get_collection('Guilds')

    guild_list = list(Guilds.find({}))

    Settings_Cache = {}

    for guild in guild_list:
        Settings_Cache[str(guild['guild_id'])] = guild

        # Empties pending verification collection (in case bot goes offline while a user was pending verification)
        pending_verification_coll = GuildInformation.get_collection("a" + str(guild['guild_id']) + ".PendingVerificationUsers")
        pending_verification_coll.delete_many({})

    # Starts a new AsyncIO event loop that runs in a separate thread (to avoid blocking main)
    update_guild_loop = asyncio.new_event_loop()
    update_guilds_thread = threading.Thread(target = start_loop, args = (update_guild_loop,))
    update_guilds_thread.start()

    # Adds update_guilds function to the created loop (now this function will run forever without blocking main)
    # If in the future multiple coroutines must run at this point concurrently, look into asyncio.gather
    asyncio.run_coroutine_threadsafe(update_guilds(client), update_guild_loop)


# Starts an AsyncIO event loop (Function exists so that a thread can target it)
def start_loop(loop: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


# Watches for changes in the Guild Settings Collection, then updates the settings cache, and reschedules all jobs
# This function runs forever so it should be called in its own thread
async def update_guilds(client):
    stream = Guilds.watch()
    for change in stream:
        guild_list = list(Guilds.find({}))
        for guild in guild_list:
            if guild['_id'] == change['documentKey']['_id']:
                Settings_Cache[str(guild['guild_id'])] = guild
                await _scheduling.reschedule_jobs(client)
                break


def update_setting(guild_id: int, setting: str, new_value):
    Guilds.update_one({'guild_id': int(guild_id)}, {'$set': {setting: new_value}})


# Returns a dictionary containing the settings for the guild. If the settings do not exist, inserts default settings for the guild into the collection and the cache
def get_settings(guild_id: int) -> dict:
    try:
        return Settings_Cache[str(guild_id)]
    except KeyError:
        generate_default_settings(guild_id)
        return Settings_Cache[str(guild_id)]


def generate_default_settings(guild_id: int):
    default_settings = {"guild_id": guild_id,
                        "prefix": "$",
                        "timezone": "America/Toronto",
                        "admin_role": "admin",
                        "pins_enabled": False,

                        "quotes_enabled": True,
                        "reaction_emoji": "Default Reaction Emoji",
                        "required_quote_reactions": 4,

                        "verification_enabled": False,
                        "verified_role": "Verified",
                        "email_domain": "@uwaterloo.ca",

                        "birthday_announcements_enabled": True,
                        "birthday_channel_id": 0,
                        "birthday_role": "Birthday",
                        "birthday_time": "00:00",

                        "morning_announcements_enabled": True,
                        "announcement_channel_id": 0,
                        "last_announcement_time": None,
                        "announcement_quoted_person": "bedi",
                        "announcement_time": "08:30",

                        "due_dates_enabled": True,
                        "due_date_channel_id": 0,
                        "courses": ["Add", "Some", "Courses"],
                        "due_date_types": ["Assignment", "Test", "Quiz", "Exam", "Project", "Other"],
                        "streams": ["4", "8"]
                        }
    Guilds.insert_one(default_settings)
    Settings_Cache[str(guild_id)] = default_settings


def get_guilds_information() -> dict:
    return Settings_Cache


def is_uw_id_linked_to_verified_user(guild_id: int, uw_id: str) -> bool:
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".VerifiedUsers")
    uw_id_hash = _hashingFunctions.hash_user_id(uw_id)
    if coll.find_one({"uw_id": uw_id_hash}) is None:
        return False
    else:
        return True


def is_uw_id_linked_to_pending_verification_user(guild_id: int, uw_id: str) -> bool:
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".PendingVerificationUsers")
    if coll.find_one({"uw_id": uw_id}) is None:
        return False
    else:
        return True


# Checks if user id is linked to a verified user in a specific guild
def is_user_id_linked_to_verified_user_in_guild(guild_id: int, user_id: int) -> bool:
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".VerifiedUsers")
    if coll.find_one({"user_id": int(user_id)}) is None:
        return False
    else:
        return True


# Checks if user id is linked to a verified user in any guild with the same email domain
def is_user_id_linked_to_verified_user_anywhere(guild_id: int, user_id: int) -> bool:
    for guild in Settings_Cache:
        if is_user_id_linked_to_verified_user_in_guild(int(guild), user_id) and Settings_Cache[guild]['email_domain'] == Settings_Cache[str(guild_id)]['email_domain']:
            return True
    return False


# Gets the user document from a verified user's ID (Only call this if you have confirmed that the user is verified in at least one guild with the same email domain.)
# Otherwise, it will return None
def get_user_doc_from_verified_user_id(guild_id: int, user_id: int) -> dict:
    for guild in get_guilds_information():
        coll = GuildInformation.get_collection("a" + str(guild) + ".VerifiedUsers")
        user_doc = coll.find_one({"user_id": int(user_id)})
        if user_doc is not None and Settings_Cache[guild]['email_domain'] == Settings_Cache[str(guild_id)]['email_domain']:
            return user_doc


def remove_verified_user(guild_id: int, user_id: int) -> bool:
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".VerifiedUsers")
    if coll.find_one_and_delete({"user_id": int(user_id)}) is None:
        return False
    else:
        return True


def add_user_to_verified_users(guild_id: int, user_id: int, uw_id_hash: str):
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".VerifiedUsers")
    coll.insert_one({'user_id': int(user_id), 'uw_id': uw_id_hash})


def admin_add_user_to_verified_users(guild_id: int, user_id: int):
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".VerifiedUsers")
    coll.insert_one({'user_id': int(user_id)})


def add_user_to_pending_verification_users(guild_id: int, user_id: int, uw_id: str):
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".PendingVerificationUsers")
    coll.insert_one({'user_id': int(user_id), 'uw_id': uw_id})


def remove_user_from_pending_verification_users(guild_id: int, user_id: int):
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".PendingVerificationUsers")
    coll.delete_one({'user_id': int(user_id)})


def get_uw_id_from_pending_user_id(guild_id: int, user_id: int):
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".PendingVerificationUsers")
    document = coll.find_one({'user_id': int(user_id)})
    return document['uw_id']


def set_users_birthday(user_id: int, birth_date: datetime.datetime):
    coll = GuildInformation.get_collection("Birthdays")
    # Upsert is true so that the document is inserted if it doesn't exist
    coll.update_one({'user_id': int(user_id)}, {'$set': {'birth_date': birth_date}}, upsert = True)


def get_all_birthdays_today() -> list:
    coll = GuildInformation.get_collection("Birthdays")
    return list(coll.aggregate([{'$match': {'$expr': {'$and': [
        {'$eq': [{'$dayOfMonth': '$birth_date'}, datetime.date.today().day]},
        {'$eq': [{'$month': '$birth_date'}, datetime.date.today().month]}
    ], }, }}]))


def get_birthdays_from_month(num_months: int) -> list:
    coll = GuildInformation.get_collection("Birthdays")

    # Projection to allow pipeline to sort by day
    projection = {
        "user_id": 1,
        "birth_date": 1,
        "day": {"$dayOfMonth": "$birth_date"}
    }

    # Filter by month
    match_filter = {'$expr':
                        {'$eq': [{'$month': '$birth_date'}, int(num_months)]}
                    }

    pipeline = [
        {"$project": projection},
        {"$match": match_filter},
        {'$sort': {"day": 1}}
    ]

    return list(coll.aggregate(pipeline))


def add_due_date_to_upcoming_due_dates(guild_id: int, course: str, due_date_type: str, title: str, stream: int, date: datetime.datetime, time_included: bool):
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".UpcomingDueDates")
    due_date = {'course': course, 'type': due_date_type, 'title': title, 'stream': int(stream), 'date': date, "time_included": bool(time_included)}
    coll.insert_one(due_date)


def remove_due_date_from_upcoming_due_dates(guild_id: int, course: str, due_date_type: str, title: str, stream: int, date: datetime.datetime, time_included: bool):
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".UpcomingDueDates")
    due_date = {'course': course, 'type': due_date_type, 'title': title, 'stream': int(stream), 'date': date, "time_included": bool(time_included)}
    coll.find_one_and_delete(due_date)


def get_all_upcoming_due_dates(guild_id: int, stream: int, course: str) -> list:
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".UpcomingDueDates")

    match_filter = {
        "stream": int(stream),
        "course": course
    }
    pipeline = [
        {"$match": match_filter},
        {'$sort': {'date': 1}}
    ]

    return list(coll.aggregate(pipeline))


def remove_due_dates_passed(guild_id: int):
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".UpcomingDueDates")
    today_date = datetime.date.today()

    time_included_query = {"date": {"$lte": datetime.datetime.now()},
                           "time_included": {"$eq": True}}

    # If time is not included in the due date, deletes any due dates before today, but not including today
    time_not_included_query = {"date": {"$lte": datetime.datetime(today_date.year, today_date.month, today_date.day) - datetime.timedelta(days = 1)},
                               "time_included": {"$eq": False}}

    coll.delete_many(time_included_query)
    coll.delete_many(time_not_included_query)


def does_assignment_exist_already(guild_id: int, course: str, due_date_type: str, title: str, stream: int, date: datetime.datetime, time_included: bool) -> bool:
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".UpcomingDueDates")
    if coll.find_one({'course': course,
                      'type': due_date_type,
                      'title': title,
                      'stream': int(stream),
                      'date': date,
                      'time_included': bool(time_included)}) is None:
        return False
    else:
        return True


def set_due_date_channel_id(guild_id: int, channel_id: int):
    Guilds.update_one({'guild_id': guild_id}, {'$set': {'due_date_channel_id': int(channel_id)}})
    Guilds.update_one({'guild_id': guild_id}, {'$set': {'last_announcement_time': None}})


def set_due_date_message_id(guild_id: int, stream: int, message_id: int):
    Guilds.update_one({'guild_id': guild_id}, {'$set': {'stream_' + str(stream) + '_message_id': message_id}})


def set_last_announcement_time(guild_id: int, time: datetime.datetime):
    Guilds.update_one({'guild_id': guild_id}, {'$set': {'last_announcement_time': time}})


def insert_quote(guild_id: int, quote: str, quoted_person: str) -> bool:
    document = {
        'quote': quote,
        'name': quoted_person.lower()
    }
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".quotes")
    try:
        coll.insert_one(document)
        return True
    except:
        return True


def delete_quote(guild_id: int, quote: str, quoted_person: str):
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".quotes")
    return coll.delete_one({"quote": quote, "name": quoted_person})


def find_quotes(guild_id: int, quoted_person: str, page: int):
    perPage = 5
    skip = perPage * (page - 1)
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".quotes")
    filter = {
        "name": {"$regex": "^.*" + quoted_person.lower() + ".*$"}
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


def random_quote_from_person(guild_id: int, quoted_person: str):
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".quotes")
    filter = {
        "name": {"$regex": "^.*" + quoted_person.lower() + ".*$"}
    }

    # print(quotedPerson)
    pipeline = [
        {"$match": filter},
        {"$sample": {"size": 1}},
    ]
    try:
        quote = list(coll.aggregate(pipeline))[0]
        return quote["quote"], quote["name"]
    except Exception as e:
        print(e)
        return None


def random_quote(guild_id: int):
    coll = GuildInformation.get_collection("a" + str(guild_id) + ".quotes")

    pipeline = [
        {"$sample": {"size": 1}},
    ]
    try:
        quote = list(coll.aggregate(pipeline))[0]
        return quote["quote"], quote["name"]
    except Exception as e:
        print(e)
        return None
