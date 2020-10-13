import hashlib


def hash_email(username, email):
    """
    :param username: Discord username as string
    :param email: Uwaterloo email as string
    :return: Hex-String
    """

    sha256 = hashlib.sha256()

    sha256.update(bytes(username, 'utf-8'))
    sha256.update(bytes(email, 'utf-8'))
    return sha256.hexdigest()


def check_hash(username, email, stored_hash):
    """
    :param username: Discord username as string
    :param email: Uwaterloo email as string
    :param stored_hash: Hex-String created from username and email when verified
    :return: Boolean
    """

    sha256 = hashlib.sha256()

    sha256.update(bytes(username, 'utf-8'))
    sha256.update(bytes(email, 'utf-8'))

    return sha256.hexdigest() == stored_hash


if __name__ == '__main__':
    testHash = hash_email("testUsername", "testEmail")
    print(testHash)
    print(check_hash("testUsername", "testEmail", testHash))
