"""
**list_diff module exports:**
 * :func:`~dictionary_diff.list_diff.equivalent` checks if two lists are equivalent
 * :func:`~dictionary_diff.list_diff.diff` returns the diff between two lists
 * :func:`~dictionary_diff.list_diff.apply_diff` applies the diff to a list

"""

from dictionary_diff.change import _Remove

def equivalent(list1: list, list2: list, equivalent_func) -> bool:
    """
    :return: True if and only if each value in list1 has exactly one
     :func:`~dictionary_diff.diff.equivalent` value in list2
    :rtype: bool
    """
    if not len(list1) == len(list2):
        return False

    list2_copy = list2.copy()

    for element_list1 in list1:
        for element_list2 in list2_copy:
            if equivalent_func(element_list1, element_list2):
                list2_copy.remove(element_list2)
                break

    return not list2_copy

def diff(orig: list, other: list, equivalent_func) -> list:
    """
    :param orig: The original list
    :param other: The list the diff is taken of
    :param equivalent_func: This method is used for determining if two elements are equivalent,
     defaults to :func:`~dictionary_diff.diff.equivalent`

    :return: The diff, so that :func:`apply_diff(orig, diff) <dictionary_diff.diff.apply_diff>`
     returns something :func:`~dictionary_diff.diff.equivalent` to other
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

def find_equivalent(orig: list, other: list, equivalent_func) -> list:
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

def find_added(orig: list, other: list, equivalent_func) -> list:
    """
    :return: a list of values v that are in other but not orig,
     such that v is a subset of other's values
    :rtype: list
    """
    return find_removed(orig=other, other=orig, equivalent_func=equivalent_func)

def find_removed(orig: list, other: list, equivalent_func) -> list:
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

def apply_diff(orig: list, difference: list) -> list:
    """
    Applies the diff to orig

    :param orig: The original list
    :param difference: The diff to apply

    :return: a list, so that
     :func:`apply_diff(something, dict_diff(something, other)) <dictionary_diff.diff.apply_diff>`
     is :func:`~dictionary_diff.diff.equivalent` to other
    :rtype: list
    """
    applied = orig.copy()

    for difference_key in difference:
        if isinstance(difference_key, _Remove):
            applied.remove(difference_key.value)
        else:
            applied.append(difference_key)

    return applied
