import hashlib


def hash_email(email):
    """
    :param email: Uwaterloo email as string
    :return: Hex-String
    """

    sha256 = hashlib.sha256()

    sha256.update(bytes(email, 'utf-8'))
    return sha256.hexdigest()


# Function may be unnecessary
def check_hash(email, stored_hash):
    """
    :param email: Uwaterloo email as string
    :param stored_hash: Hex-String created from username and email when verified
    :return: Boolean
    """

    sha256 = hashlib.sha256()

    sha256.update(bytes(email, 'utf-8'))

    return sha256.hexdigest() == stored_hash


if __name__ == '__main__':
    testHash = hash_email("testUsername", "testEmail")
    print(testHash)
    print(check_hash("testUsername", "testEmail", testHash))
