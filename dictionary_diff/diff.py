"""
**diff module exports:**
 * :func:`~dictionary_diff.diff.equivalent` checks if two values are equivalent
 * :func:`~dictionary_diff.diff.diff` returns the diff between two values
 * :func:`~dictionary_diff.diff.apply_diff` applies the diff to a value

"""

from dataclasses import dataclass

@dataclass
class _Remove:
    value: object

    def __init__(self, value=None) -> None:
        self.value = value

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return False

        return self.value == __o.value

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

    if isinstance(element1, list):
        from dictionary_diff import list_diff
        return list_diff.list_equivalent(element1, element2)

    if isinstance(element1, dict):
        from dictionary_diff import dict_diff
        return dict_diff.dict_equivalent(element1, element2)

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
        from dictionary_diff import dict_diff
        return dict_diff.dict_diff(orig, other, equivalent_func=equivalent_func)

    if isinstance(orig, list) and isinstance(other, list):
        from dictionary_diff import list_diff
        return list_diff.list_diff(orig, other, equivalent_func=equivalent_func)

    return other

def apply_diff(orig, diff):
    """
    Applies the diff to orig

    :param orig: The original value
    :param diff: The diff to apply

    :return: a dict, so that
     :func:`apply_diff(something, diff(something, other)) <dictionary_diff.diff.apply_diff>`
     is :func:`~dictionary_diff.diff.equivalent` to other
    """
    if isinstance(orig, dict) and isinstance(diff, dict):
        from dictionary_diff import dict_diff
        return dict_diff.apply_dict_diff(orig, diff)

    if isinstance(orig, list) and isinstance(diff, list):
        from dictionary_diff import list_diff
        return list_diff.apply_list_diff(orig, diff)

    return diff
