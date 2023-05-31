from logger import logger


def read_csv(path, separator=","):
    """
    Reads csv file
    :param path: path to the csv file
    :type path: str
    :param separator: csv data separator, defaults to ","
    :type separator: str
    :return: list of dictionaries of items from database
    :rtype: list of dict
    """
    items = []

    with open(path, "r", encoding="UTF-8") as csv_file:
        lines = csv_file.readlines()

    headers = _prep_line(content=lines[0], separator=separator)

    for line in lines[1:]:
        formatted_line = _prep_line(content=line, separator=separator)
        item = {key: item for key, item in zip(headers, formatted_line)}

        logger.trace(item)
        items.append(item)

    logger.debug(f"Retrieved {len(items)} item(s) from {path}")
    return items


def _prep_line(content, separator):
    """
    Removes unnecessary characters from given csv content line
    :param content: csv line's content
    :type content: str
    :param separator: csv data separator
    :type separator: str
    :return: prepared line
    :rtype: list of str
    """
    _separator = f'"{separator}"'
    content = content.replace(",,", ',"None",')

    return [item.strip('"').strip("\n") for item in content.split(_separator)]
