import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")

mClient = None
UserInformation = None
VerifiedUsers = None
PendingVerificationUsers = None


def init():
    global mClient
    global UserInformation
    global VerifiedUsers
    global PendingVerificationUsers

    mClient = pymongo.MongoClient(CONNECTION_STRING)

    UserInformation = mClient['UserInformation']

    VerifiedUsers = UserInformation['VerifiedUsers']

    PendingVerificationUsers = UserInformation['PendingVerificationUsers']


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


init()
