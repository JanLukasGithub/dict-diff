"""
**dict_diff module exports:**
 * :func:`~dict_diff.dict_diff.apply_diff` Apply the diff to a dict
 * :func:`~dict_diff.dict_diff.dict_diff` Get the diff between two dicts
 * :func:`~dict_diff.dict_diff.equivalent` Checks if two items are equivalent

"""

from dataclasses import dataclass


def equivalent(element1, element2) -> bool:
    """
    :return: True if and only if:

    - The types of element1 and element2 are the same
    - - For lists: if the lists are equal regardless of order
      - For dicts: if all members are equivalent
      - For everything else: if `element1 == element2`

    :rtype: bool
    """
    if type(element1) is not type(element2):
        return False

    if isinstance(element1, list):
        return list_unordered_equal(element1, element2)

    if isinstance(element1, dict):
        return dict_equivalent(element1, element2)

    return element1 == element2

def dict_equivalent(dict1: dict, dict2: dict) -> bool:
    """
    :return: True if and only if all members of the dicts are
     :func:`~dict_diff.dict_diff.equivalent`
    :rtype: bool
    """
    if not len(dict1) == len(dict2):
        return False

    for key in dict1:
        if key not in dict2 or not equivalent(dict1[key], dict2[key]):
            return False

    return True

def list_unordered_equal(list1: list, list2: list) -> bool:
    """
    :return: True if and only if each value in list1 has exactly one
     :func:`~dict_diff.dict_diff.equivalent` value in list2
    :rtype: bool
    """
    if not len(list1) == len(list2):
        return False

    list2_copy = list2.copy()

    for element_list1 in list1:
        for element_list2 in list2_copy:
            if equivalent(element_list1, element_list2):
                list2_copy.remove(element_list2)
                break

    return not list2_copy

def dict_diff(orig: dict, other: dict, removing=False, equivalent_func=equivalent) -> dict:
    """
    :param orig: The original dict
    :param other: The dict the diff is taken of
    :param removing: If this method uses :func:`~dict_diff.dict_diff.remove_equivalent` or
     :func:`~dict_diff.dict_diff.add_different`, defaults to False
    :param equivalent_func: This method is used for determining if two elements
     (of any types) are equivalent,
     defaults to :func:`~dict_diff.dict_diff.equivalent`

    :return: The diff, so that :func:`apply_diff(orig, diff) <dict_diff.dict_diff.apply_diff>`
     returns something :func:`~dict_diff.dict_diff.equivalent` to other
    :rtype: dict

    You can directly use :func:`~dict_diff.dict_diff.add_different` or
     :func:`~dict_diff.dict_diff.remove_equivalent` to circumvent one if-statement
    """
    if removing:
        return remove_equivalent(orig, other, equivalent_func)

    return add_different(orig, other, equivalent_func)

def add_different(orig: dict, other: dict, equivalent_func=equivalent) -> dict:
    """
    :return: the dict, where all of other's keys values not :func:`~dict_diff.dict_diff.equivalent`
     to ones in orig are present. If the value of a key is a dict, only non
     :func:`~dict_diff.dict_diff.equivalent` parts of that dictionary are present
    :rtype: dict

    This is faster than :func:`~dict_diff.dict_diff.remove_equivalent`,
     if the difference between the dicts is small
    """
    new_dict = {}

    for difference in find_different(orig, other, equivalent_func):
        if difference in orig and isinstance(orig[difference], dict) and isinstance(other[difference], dict):
            new_dict[difference] = add_different(orig[difference], other[difference], equivalent_func)
        else:
            new_dict[difference] = other[difference]

    for removed in find_removed(orig, other):
        new_dict[removed] = _Remove(orig[removed])

    return new_dict

def remove_equivalent(orig: dict, other: dict, equivalent_func=equivalent) -> dict:
    """
    :return: the dict, where all of other's keys values :func:`~dict_diff.dict_diff.equivalent`
     to ones in orig have been removed. If the value of a key is a dict, all
     :func:`~dict_diff.dict_diff.equivalent` parts of that dictionary are removed as well
    :rtype: dict

    This is faster than :func:`~dict_diff.dict_diff.add_different`,
     if the difference between the dicts is large
    """
    removed_from = other.copy()

    for to_remove in find_equivalent(orig, other, equivalent_func):
        removed_from.pop(to_remove)

    for remaining in removed_from:
        if remaining in orig:
            if isinstance(other[remaining], dict) and isinstance(orig[remaining], dict):
                removed_from[remaining] = remove_equivalent(orig[remaining], other[remaining], equivalent_func)

    for mark_remove in find_removed(orig, other):
        removed_from[mark_remove] = _Remove(orig[mark_remove])

    return removed_from

def find_different(orig: dict, other: dict, equivalent_func=equivalent) -> list:
    """
    :return: a list of keys k whose values are not :func:`~dict_diff.dict_diff.equivalent`
     in orig and other, such that k is a subset of other's keys
    :rtype: list
    """
    found_keys = []

    for key in other:
        if key not in orig or not equivalent_func(other[key], orig[key]):
            found_keys.append(key)

    return found_keys

def find_equivalent(orig: dict, other: dict, equivalent_func=equivalent) -> list:
    """
    :return: a list of keys k whose values are :func:`~dict_diff.dict_diff.equivalent`
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

def apply_diff(orig: dict, diff: dict) -> dict:
    """
    Applies the diff to orig

    :param orig: The original dict
    :param diff: The diff to apply

    :return: a dict, so that
     :func:`apply_diff(something, dict_diff(something, other)) <dict_diff.dict_diff.apply_diff>`
     is :func:`~dict_diff.dict_diff.equivalent` to other
    :rtype: dict
    """
    applied = orig.copy()

    for difference in diff:
        if difference in orig and isinstance(orig[difference], dict) and isinstance(diff[difference], dict):
            applied[difference] = apply_diff(orig[difference], diff[difference])
        elif isinstance(diff[difference], _Remove):
            applied.pop(difference)
        else:
            applied[difference] = diff[difference]

    return applied

@dataclass
class _Remove:
    value: object

    def __init__(self, value=None) -> None:
        self.value = value

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return False

        return self.value == __o.value
