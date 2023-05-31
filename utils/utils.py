from hashlib import md5


def get_checksum(file_content):
    """
    Gets checksum for given file
    :param file_content: content of the file
    :type file_content: str or bytes
    :return: MD5 checksum
    :rtype: str
    """
    return md5(file_content).hexdigest()
