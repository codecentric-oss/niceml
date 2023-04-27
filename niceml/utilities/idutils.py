"""Module for generating id's """
import hashlib
import string

ALPHANUMERICLIST = list(string.digits + string.ascii_lowercase)


def id_from_id_list(id_list: list, id_len=4):
    """Returns a single id from a list of id's"""
    hash_value = hashlib.md5(str(id_list).encode()).hexdigest()
    hash_value = int(hash_value, base=16)
    poss_values = len(ALPHANUMERICLIST) ** id_len
    hash_value %= poss_values
    str_value = base_10_to_n(hash_value, ALPHANUMERICLIST)
    str_value = str_value.rjust(id_len, ALPHANUMERICLIST[0])
    return str_value


def generate_short_id(run_id: str, id_len=4) -> str:
    """Generates an alphanumeric hashed version of an experiments run_id"""
    hash_value = hashlib.md5(str([run_id]).encode()).hexdigest()
    hash_value = int(hash_value, base=16)
    poss_values = len(ALPHANUMERICLIST) ** id_len
    hash_value %= poss_values
    str_value = base_10_to_n(hash_value, ALPHANUMERICLIST)
    str_value = str_value.rjust(id_len, ALPHANUMERICLIST[0])
    return str_value


def base_10_to_n(number: int, base_chars: list) -> str:
    """
    Convert 'number' to given base with character list
    Args:
        number: Specify the number to be converted
        base_chars: characters to convert to
    Returns:
        The base-n representation of a given number
    """
    base = len(base_chars)
    if base <= 1:
        raise ValueError("len(base_chars) must be more than 2")
    converted_string = ""
    if number == 0:
        converted_string += base_chars[0]
    current_number = number
    while current_number > 0:
        current_number, mod = divmod(current_number, base)
        converted_string = base_chars[mod] + converted_string
    return converted_string
