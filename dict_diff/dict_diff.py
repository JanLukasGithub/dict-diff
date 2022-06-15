"""
**dict_diff module exports:**
 * :func:`~dict_diff.dict_diff.apply_diff` Apply the diff to a dict
 * :func:`~dict_diff.dict_diff.dict_diff` Get the diff between two dicts
 * :func:`~dict_diff.dict_diff.equivalent` Checks if two items are equivalent

"""

from dataclasses import dataclass


def equivalent(element1, element2):
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

def dict_equivalent(dict1: dict, dict2: dict):
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

def list_unordered_equal(list1: list, list2: list):
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

def dict_diff(orig: dict, other: dict, removing=False, equivalent_func=equivalent):
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

def add_different(orig: dict, other: dict, equivalent_func=equivalent):
    """
    :return: the dict, where all of other's keys values not :func:`~dict_diff.dict_diff.equivalent`
         to ones in orig are present. If the value of a key is a dict, only non
         :func:`~dict_diff.dict_diff.equivalent` parts of that dictionary are present

    This is faster than :func:`~dict_diff.dict_diff.remove_equivalent`,
         if the difference between the dicts is small
    """
    new_dict = {}

    for key in find_different(orig, other, equivalent_func):
        if key in orig and isinstance(orig[key], dict) and isinstance(other[key], dict):
            new_dict[key] = add_different(orig[key], other[key], equivalent_func)
        else:
            new_dict[key] = other[key]

    for key in find_removed(orig, other):
        new_dict[key] = _Remove()

    return new_dict

def remove_equivalent(orig: dict, other: dict, equivalent_func=equivalent):
    """
    :return: the dict, where all of other's keys values :func:`~dict_diff.dict_diff.equivalent`
         to ones in orig have been removed. If the value of a key is a dict, all
         :func:`~dict_diff.dict_diff.equivalent` parts of that dictionary are removed as well

    This is faster than :func:`~dict_diff.dict_diff.add_different`,
         if the difference between the dicts is large
    """
    to_remove = find_equivalent(orig, other, equivalent_func)

    removed_from = other.copy()

    for key in to_remove:
        removed_from.pop(key)

    for key in removed_from:
        if key in orig:
            if isinstance(other[key], dict) and isinstance(orig[key], dict):
                removed_from[key] = remove_equivalent(orig[key], other[key], equivalent_func)

    for key in find_removed(orig, other):
        removed_from[key] = _Remove()

    return removed_from

def find_different(orig: dict, other: dict, equivalent_func=equivalent):
    """
    :return: a list of keys k whose values are not :func:`~dict_diff.dict_diff.equivalent`
         in orig and other, such that k is a subset of other's keys
    """
    found_keys = []

    for key in other:
        if key not in orig or not equivalent_func(other[key], orig[key]):
            found_keys.append(key)

    return found_keys

def find_equivalent(orig: dict, other: dict, equivalent_func=equivalent):
    """
    :return: a list of keys k whose values are :func:`~dict_diff.dict_diff.equivalent`
     in orig and other, such that k is a subset of orig's and other's keys
    """
    found_keys = []

    for key in other:
        if key in orig and equivalent_func(other[key], orig[key]):
            found_keys.append(key)

    return found_keys

def find_added(orig: dict, other: dict):
    """
    :return: a list of keys k that are in other but not orig,
         such that k is a subset of other's keys
    """
    return find_removed(orig=other, other=orig)

def find_removed(orig: dict, other: dict):
    """
    :return: a list of keys k that are in orig but not other, such that k is a subset of orig's keys
    """
    found = []

    for key in orig:
        if key not in other:
            found.append(key)

    return found

def apply_diff(orig: dict, diff: dict):
    """
    Applies the diff to orig

    :param orig: The original dict
    :param diff: The diff to apply

    :return: a dict, so that
         :func:`apply_diff(something, dict_diff(something, other)) <dict_diff.dict_diff.apply_diff>`
         is :func:`~dict_diff.dict_diff.equivalent` to other
    """
    applied = orig.copy()

    for key in diff:
        if key in orig and isinstance(orig[key], dict) and isinstance(diff[key], dict):
            applied[key] = apply_diff(orig[key], diff[key])
        elif isinstance(diff[key], _Remove):
            applied.pop(key)
        else:
            applied[key] = diff[key]

    return applied

@dataclass
class _Remove:
    value: object

    def __init__(self, value=None):
        self.value = value

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return False

        return self.value == __o.value
