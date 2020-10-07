import os

import pymongo

from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")

mClient = pymongo.MongoClient(CONNECTION_STRING)

VerifiedUsersCollection = mClient['UserInformation']['VerifiedUsers']

PendingVerificationUsersCollection = mClient['UserInformation']['PendingVerificationUsers']


def is_email_linked_to_verified_user(email_address):
    if VerifiedUsersCollection.find_one({"email_address": email_address}) is None:
        return False
    return True


def is_user_id_linked_to_verified_user(user_id):
    print(VerifiedUsersCollection.find_one({"user_id": user_id}))
    if VerifiedUsersCollection.find_one({"user_id": user_id}) is None:
        return False
    return True


def remove_verified_user(user_id):
    if VerifiedUsersCollection.find_one_and_delete({"user_id": user_id}) is None:
        return False
    return True

def add_user_to_verified_users(user_id, email):
    VerifiedUsersCollection.insert_one({'user_id': user_id, 'email_address': email})


def add_user_to_pending_verification_users(user_id, email):
    PendingVerificationUsersCollection.insert_one({'user_id': user_id, 'email_address': email})


def remove_user_from_pending_verification_users(user_id):
    PendingVerificationUsersCollection.find_one_and_delete({'user_id': user_id})


def get_email_from_pending_user_id(user_id):
    Document = PendingVerificationUsersCollection.find_one({'user_id': user_id})
    if Document is not None:
        return Document['email_address']
