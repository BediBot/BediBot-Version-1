import asyncio
import os
import threading
import pymongo
import datetime
from dotenv import load_dotenv
from commands import _hashingFunctions, _scheduling

load_dotenv()

CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
DATABASE_STRING = os.getenv("MONGO_DATABASE_STRING")

mClient = None
GuildInformation = None
Guilds = None
Guild_Cache = {}


async def init(client):
    global mClient
    global Guilds
    global GuildInformation
    global Guild_Cache

    mClient = pymongo.MongoClient(CONNECTION_STRING)

    GuildInformation = mClient[DATABASE_STRING]

    Guilds = GuildInformation['Guilds']

    guild_list = list(Guilds.find({}))

    for guild in guild_list:
        Guild_Cache[str(guild['guild_id'])] = {}
        Guild_Cache[str(guild['guild_id'])]['settings'] = guild

        pending_verification_coll = GuildInformation["a" + str(guild['guild_id']) + ".PendingVerificationUsers"]
        pending_verification_coll.delete_many({})

    # Starts a new AsyncIO event loop to run in a separate thread (to avoid blocking main)
    update_guild_loop = asyncio.new_event_loop()
    update_guilds_thread = threading.Thread(target = start_loop, args = (update_guild_loop,))
    update_guilds_thread.start()

    # Adds update_guilds function to the created loop (now this function will run forever without blocking main)
    # If in the future multiple functions must run at this point concurrently, look into asyncio.gather
    asyncio.run_coroutine_threadsafe(update_guilds(client), update_guild_loop)


# Starts an AsyncIO event loop (Function exists so that a thread can target it)
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


# Watched for changes in the Guild Settings Collection, Updated the Cache, and Reschedules all Jobs (in case announcement times changed)
async def update_guilds(client):
    stream = Guilds.watch()
    for change in stream:
        guild_list = list(Guilds.find({}))
        for guild in guild_list:
            if guild['_id'] == change['documentKey']['_id']:
                Guild_Cache[str(guild['guild_id'])]['settings'] = guild
                await _scheduling.reschedule_jobs(client)
                break


def get_settings(guild_id: int):
    try:
        return Guild_Cache[str(guild_id)]['settings']
    except KeyError:
        default_settings = {"guild_id": guild_id,
                            "timezone": "America/Toronto",
                            "admin_role": "admin",
                            "channel_id": 0,
                            "verification_enabled": False,
                            "birthday_announcements_enabled": True,
                            "morning_announcements_enabled": True,
                            "due_dates_enabled": True,
                            "last_announcement_time": None,
                            "announcement_role": "Bedi Follower",
                            "announcement_quoted_person": "bedi",
                            "announcement_time": "08:30",
                            "birthday_role": "Bedi's Favourite",
                            "birthday_time": "00:00",
                            "courses": ["Add", "Some", "Courses"],
                            "due_date_types": ["Assignment", "Test", "Quiz", "Exam", "Project", "Other"],
                            "streams": ["8", "4"],
                            "reaction_emoji": "Default Reaction Emoji",
                            "required_quote_reactions": 4
                            }
        Guilds.insert_one(default_settings)
        Guild_Cache[str(guild_id)]['settings'] = default_settings
        return Guild_Cache[str(guild_id)]['settings']


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


def set_users_birthday(user_id: int, birth_date: datetime.datetime):
    coll = GuildInformation["Birthdays"]
    coll.update_one({'user_id': int(user_id)}, {'$set': {'birth_date': birth_date}}, upsert = True)


def get_all_birthdays_today():
    coll = GuildInformation["Birthdays"]
    return list(coll.aggregate([
        {'$match':
            {'$expr':
                {'$and': [
                    {'$eq': [{'$dayOfMonth': '$birth_date'}, datetime.date.today().day]},
                    {'$eq': [{'$month': '$birth_date'}, datetime.date.today().month]}, ], },
            }
        }]))


def get_birthdays_from_month(num_months: int):
    coll = GuildInformation["Birthdays"]

    project = {
        "user_id": 1,
        "birth_date": 1,
        "day": {"$dayOfMonth": "$birth_date"}
    }

    filter = {'$expr':
                  {'$eq': [{'$month': '$birth_date'}, int(num_months)]}
              }
    pipeline = [
        {"$project": project},
        {"$match": filter},
        {'$sort': {"day": 1}}
    ]

    return list(coll.aggregate(pipeline))


def add_due_date_to_upcoming_due_dates(guild_id: int, course, due_date_type, title, stream: int, date: datetime.datetime, timeIncluded: bool):
    coll = GuildInformation["a" + str(guild_id) + ".UpcomingDueDates"]
    due_date = {'course': course, 'type': due_date_type, 'title': title, 'stream': int(stream), 'date': date, "time_included": bool(timeIncluded)}
    coll.insert_one(due_date)


def remove_due_date_from_upcoming_due_dates(guild_id: int, course, due_date_type, title, stream: int, date: datetime.datetime, timeIncluded: bool):
    coll = GuildInformation["a" + str(guild_id) + ".UpcomingDueDates"]
    due_date = {'course': course, 'type': due_date_type, 'title': title, 'stream': int(stream), 'date': date, "time_included": bool(timeIncluded)}
    coll.find_one_and_delete(due_date)


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


def get_guilds_information():
    return Guild_Cache


def remove_due_dates_passed(guild_id: int):
    coll = GuildInformation["a" + str(guild_id) + ".UpcomingDueDates"]
    today_date = datetime.date.today()

    time_included_query = {"date": {"$lte": datetime.datetime.now()}, "time_included": {"$eq": True}}
    time_not_included_query = {"date": {"$lte": datetime.datetime(today_date.year, today_date.month, today_date.day) - datetime.timedelta(days = 1)},
                               "time_included": {"$eq": False}}

    coll.delete_many(time_included_query)
    coll.delete_many(time_not_included_query)


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


def insert_quote(guild_id: int, quote: str, quoted_person: str):
    doc = {
        'quote': quote,
        'name': quoted_person.lower()
    }
    coll = GuildInformation["a" + str(guild_id) + ".quotes"]
    coll.insert_one(doc)
    try:
        return True
    except:
        return False


def delete_quote(guild_id, quote, quoted_person):
    coll = GuildInformation["a" + str(guild_id) + ".quotes"]
    coll.delete_one({"quote": quote, "name": quoted_person})


def find_quotes(guild_id, quoted_person, page):
    perPage = 5
    skip = perPage * (page - 1)
    coll = GuildInformation["a" + str(guild_id) + ".quotes"]
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


def random_quote(guild_id, quoted_person):
    coll = GuildInformation["a" + str(guild_id) + ".quotes"]
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
        return '"' + quote["quote"] + '"  - ' + quote["name"]
    except Exception as e:
        print(e)
        return None
