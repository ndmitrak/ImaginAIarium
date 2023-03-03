import os

from settings.unicode import emoji

msg_dir = './settings/messages/'


def get_message(message_name: str) -> str:
    """
    Get message text from .txt file.

    Usage:
    >>> msg = get_message('help')
    >>> print(msg)
    This is contexts of help.txt file
    """
    path = f'{msg_dir}{message_name}.txt'
    file_exists = os.path.isfile(path)
    if not file_exists:
        raise LookupError(
            f'There are no file {message_name} in {msg_dir} folder'
        )
    with open(path, 'r') as fd:
        message = fd.read()
    return message.format(**emoji)
