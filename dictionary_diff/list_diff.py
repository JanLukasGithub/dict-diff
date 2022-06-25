"""

"""

from dictionary_diff import diff
from dictionary_diff.diff import _Remove


def list_equivalent(list1: list, list2: list) -> bool:
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
            if diff.equivalent(element_list1, element_list2):
                list2_copy.remove(element_list2)
                break

    return not list2_copy

def list_diff(orig: list, other: list, equivalent_func=diff.equivalent) -> list:
    """
    :param orig: The original list
    :param other: The list the diff is taken of
    :param equivalent_func: This method is used for determining if two elements
     (of any types) are equivalent,
     defaults to :func:`~dict_diff.dict_diff.equivalent`

    :return: The diff, so that :func:`apply_diff(orig, diff) <dict_diff.dict_diff.apply_diff>`
     returns something :func:`~dict_diff.dict_diff.equivalent` to other
    :rtype: list
    """
    difference = []

    added = find_added(orig, other, equivalent_func)
    removed = find_removed(orig, other, equivalent_func)

    for item in added:
        difference.append(item)

    for item in removed:
        difference.append(_Remove(item))

    return difference

def find_equivalent(orig: list, other: list, equivalent_func=diff.equivalent) -> list:
    """
    :return: a list of values v that are :func:`~dictionary_diff.diff.equivalent` in orig and other,
     such that v is a subset of orig and other
    :rtype: list
    """
    found = []
    orig_copy = orig.copy()

    for item_other in other:
        for item_orig in orig_copy:
            if equivalent_func(item_other, item_orig):
                found.append(item_orig)
                orig_copy.remove(item_orig)
                break

    return found

def find_added(orig: list, other: list, equivalent_func=diff.equivalent) -> list:
    """
    :return: a list of values v that are in other but not orig,
     such that v is a subset of other's values
    :rtype: list
    """
    return find_removed(orig=other, other=orig, equivalent_func=equivalent_func)

def find_removed(orig: list, other: list, equivalent_func=diff.equivalent) -> list:
    """
    :return: a list of values v that are in orig but not other, such that v is a subset of orig's
    values
    :rtype: list
    """
    orig_copy = orig.copy()

    for item_other in other:
        for item_orig in orig_copy:
            if equivalent_func(item_other, item_orig):
                orig_copy.remove(item_orig)
                break

    return orig_copy

def apply_list_diff(orig: list, diff: list) -> list:
    """
    Applies the diff to orig

    :param orig: The original list
    :param diff: The diff to apply

    :return: a list, so that
     :func:`apply_diff(something, dict_diff(something, other)) <dict_diff.dict_diff.apply_diff>`
     is :func:`~dict_diff.dict_diff.equivalent` to other
    :rtype: list
    """
    applied = orig.copy()

    for difference in diff:
        if isinstance(difference, _Remove):
            applied.remove(difference.value)
        else:
            applied.append(difference)

    return applied
