"""
**dict_diff module exports:**
 * :func:`~dictionary_diff.dict_diff.apply_dict_diff` Apply the diff to a dict
 * :func:`~dictionary_diff.dict_diff.dict_diff` Get the diff between two dicts
 * :func:`~dictionary_diff.dict_diff.dict_equivalent` Checks if two items are equivalent

"""

from dictionary_diff.change import _Remove

def dict_equivalent(dict1: dict, dict2: dict, equivalent_func) -> bool:
    """
    :return: True if and only if all members of the dicts are
     :func:`~dictionary_diff.diff.equivalent`
    :rtype: bool
    """
    if not len(dict1) == len(dict2):
        return False

    for key in dict1:
        if key not in dict2 or not equivalent_func(dict1[key], dict2[key]):
            return False

    return True

def dict_diff(orig: dict, other: dict, equivalent_func, diff_func) -> dict:
    """
    :param orig: The original dict
    :param other: The dict the diff is taken of
    :param equivalent_func: This method is used for determining if two elements
     (of any types) are equivalent,
     defaults to :func:`~dictionary_diff.diff.equivalent`

    :return: The diff, so that :func:`apply_diff(orig, diff) <dictionary_diff.diff.apply_diff>`
     returns something :func:`~dictionary_diff.diff.equivalent` to other
    :rtype: dict
    """
    new_dict = {}

    for difference in find_different(orig, other, equivalent_func):
        new_dict[difference] = \
            diff_func(orig.get(difference, None), other[difference], equivalent_func)

    for removed in find_removed(orig, other):
        new_dict[removed] = _Remove(orig[removed])

    return new_dict

def find_different(orig: dict, other: dict, equivalent_func) -> list:
    """
    :return: a list of keys k whose values are not :func:`~dictionary_diff.diff.equivalent`
     in orig and other, such that k is a subset of other's keys
    :rtype: list
    """
    found_keys = []

    for key in other:
        if key not in orig or not equivalent_func(other[key], orig[key]):
            found_keys.append(key)

    return found_keys

def find_equivalent(orig: dict, other: dict, equivalent_func) -> list:
    """
    :return: a list of keys k whose values are :func:`~dictionary_diff.diff.equivalent`
     in orig and other, such that k is a subset of orig's and other's keys
    :rtype: list
    """
    found_keys = []

    for key in other:
        if key in orig and equivalent_func(other[key], orig[key]):
            found_keys.append(key)

    return found_keys

def find_added(orig: dict, other: dict) -> list:
    """
    :return: a list of keys k that are in other but not orig,
     such that k is a subset of other's keys
    :rtype: list
    """
    return find_removed(orig=other, other=orig)

def find_removed(orig: dict, other: dict) -> list:
    """
    :return: a list of keys k that are in orig but not other, such that k is a subset of orig's keys
    :rtype: list
    """
    found = []

    for key in orig:
        if key not in other:
            found.append(key)

    return found

def apply_dict_diff(orig: dict, difference: dict, apply_diff_func) -> dict:
    """
    Applies the diff to orig

    :param orig: The original dict
    :param difference: The diff to apply

    :return: a dict, so that
     :func:`apply_diff(something, dict_diff(something, other)) <dictionary_diff.diff.apply_diff>`
     is :func:`~dictionary_diff.diff.equivalent` to other
    :rtype: dict
    """
    applied = orig.copy()

    for difference_key in difference:
        if isinstance(difference[difference_key], _Remove):
            applied.pop(difference_key, None)
        else:
            applied[difference_key] = \
                apply_diff_func(orig.get(difference_key, None), difference[difference_key])

    return applied
