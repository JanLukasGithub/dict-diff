"""

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
      - For dicts: if all members are equivalent
      - For everything else: if `element1 == element2`

    :rtype: bool
    """
    import dictionary_diff.dict_diff as dict_diff
    import dictionary_diff.list_diff as list_diff

    if type(element1) is not type(element2):
        return False

    if isinstance(element1, list):
        return list_diff.list_unordered_equal(element1, element2)

    if isinstance(element1, dict):
        return dict_diff.dict_equivalent(element1, element2)

    return element1 == element2
