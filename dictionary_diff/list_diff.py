"""

"""

import dictionary_diff.diff as diff


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
            if diff.equivalent(element_list1, element_list2):
                list2_copy.remove(element_list2)
                break

    return not list2_copy

def add_different_list(orig: list, other: list, equivalent_func=diff.equivalent) -> list:
    """
    :return: the list, where all other's values not :func:`~dict_diff.dict_diff.equivalent`
     to ones in orig are present. If the value dict or list, only non
     :func:`~dict_diff.dict_diff.equivalent` parts of that are present
    :rtype: list

    This is faster than :func:`~dict_diff.dict_diff.remove_equivalent_list`,
     if the difference between the lists is small
    """
    pass
