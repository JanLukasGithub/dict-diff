"""
**diff module exports:**
 * :func:`~dictionary_diff.diff.equivalent` checks if two values are equivalent
 * :func:`~dictionary_diff.diff.diff` returns the diff between two values
 * :func:`~dictionary_diff.diff.apply_diff` applies the diff to a value

"""

from dictionary_diff import list_diff
from dictionary_diff import dict_diff

def equivalent(element1, element2) -> bool:
    """
    :return: True if and only if:

    - The types of element1 and element2 are the same
    - - For lists: if the lists are equal regardless of order
      - For dicts: if all key-value pairs are equivalent
      - For everything else: if `element1 == element2`

    :rtype: bool
    """
    if type(element1) is not type(element2):
        return False
    
    if isinstance(element1, dict):
        return dict_diff.equivalent(element1, element2, equivalent_func=equivalent)

    if isinstance(element1, list):
        return list_diff.equivalent(element1, element2, equivalent_func=equivalent)

    return element1 == element2

def diff(orig, other, equivalent_func=equivalent):
    """
    :param orig: The original value
    :param other: The value the diff is taken of
    :param equivalent_func: This method is used for determining if two values are equivalent,
     defaults to :func:`~dictionary_diff.diff.equivalent`

    :return: The diff, so that :func:`apply_diff(orig, diff) <dictionary_diff.diff.apply_diff>`
     returns something :func:`~dictionary_diff.diff.equivalent` to other
    """
    if isinstance(orig, dict) and isinstance(other, dict):
        return dict_diff.diff(orig, other, equivalent_func=equivalent_func, diff_func=diff)

    if isinstance(orig, list) and isinstance(other, list):
        return list_diff.diff(orig, other, equivalent_func=equivalent_func)

    return other

def apply_diff(orig, difference):
    """
    Applies the diff to orig

    :param orig: The original value
    :param difference: The diff to apply

    :return: a dict, so that
     :func:`apply_diff(something, diff(something, other)) <dictionary_diff.diff.apply_diff>`
     is :func:`~dictionary_diff.diff.equivalent` to other
    """
    if isinstance(orig, dict) and isinstance(difference, dict):
        return dict_diff.apply_diff(orig, difference, apply_diff)

    if isinstance(orig, list) and isinstance(difference, list):
        return list_diff.apply_diff(orig, difference)

    return difference
