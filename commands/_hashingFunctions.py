import hashlib


def hash_user_id(user_id):
    """
    :param user_id: Uwaterloo email as string
    :return: Hex-String
    """

    sha256 = hashlib.sha256()

    sha256.update(bytes(user_id, 'utf-8'))
    return sha256.hexdigest()


def check_hash(user_id, stored_hash):
    """
    :param user_id: Uwaterloo email as string
    :param stored_hash: Hex-String created from username and email when verified
    :return: Boolean
    """

    sha256 = hashlib.sha256()

    sha256.update(bytes(user_id, 'utf-8'))

    return sha256.hexdigest() == stored_hash


if __name__ == '__main__':
    testHash = hash_user_id("testUsername", "testEmail")
    print(testHash)
    print(check_hash("testUsername", "testEmail", testHash))
