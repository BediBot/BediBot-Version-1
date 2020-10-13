import os
import pymongo
import datetime
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")

mClient = None
UserInformation = None
GuildInformation = None
VerifiedUsers = None
PendingVerificationUsers = None
UpcomingDueDates = None


def init():
    global mClient
    global UserInformation
    global VerifiedUsers
    global PendingVerificationUsers
    global GuildInformation
    global UpcomingDueDates

    mClient = pymongo.MongoClient(CONNECTION_STRING)

    UserInformation = mClient['UserInformation']

    GuildInformation = mClient['GuildInformation']

    VerifiedUsers = UserInformation['VerifiedUsers']

    PendingVerificationUsers = UserInformation['PendingVerificationUsers']

    UpcomingDueDates = GuildInformation['UpcomingDueDates']

    PendingVerificationUsers.delete_many({})


def is_email_linked_to_verified_user(email_address):
    if VerifiedUsers.find_one({"email_address": email_address}) is None:
        return False
    return True


def is_user_id_linked_to_verified_user(user_id):
    if VerifiedUsers.find_one({"user_id": user_id}) is None:
        return False
    return True


def remove_verified_user(user_id):
    if VerifiedUsers.find_one_and_delete({"user_id": user_id}) is None:
        return False
    return True


def add_user_to_verified_users(user_id, email):
    VerifiedUsers.insert_one({'user_id': user_id, 'email_address': email})


def add_user_to_pending_verification_users(user_id, email):
    PendingVerificationUsers.insert_one({'user_id': user_id, 'email_address': email})


def remove_user_from_pending_verification_users(user_id):
    PendingVerificationUsers.find_one_and_delete({'user_id': user_id})


def get_email_from_pending_user_id(user_id):
    document = PendingVerificationUsers.find_one({'user_id': user_id})
    if document is not None:
        return document['email_address']


def set_users_birthday(user_id, birth_date):
    VerifiedUsers.update_one({'user_id': user_id}, {'$set': {'birth_date': birth_date}})


def get_all_birthdays_today():
    return list(VerifiedUsers.aggregate([
        {'$match':
            {'$expr':
                {'$and': [
                    {'$eq': [{'$dayOfMonth': '$birth_date'}, datetime.date.today().day]},
                    {'$eq': [{'$month': '$birth_date'}, datetime.date.today().month]}, ], },
            }
        }]))


def add_due_date_to_upcoming_due_dates(course, due_date_type, title, date):
    UpcomingDueDates.insert_one({'course': course, 'type': due_date_type, 'title': title, 'date': date})


def get_all_upcoming_due_dates():
    return list(UpcomingDueDates.aggregate())
