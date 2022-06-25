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
      - For dicts: if all key-value pairs are equivalent
      - For everything else: if `element1 == element2`

    :rtype: bool
    """
    if type(element1) is not type(element2):
        return False

    if isinstance(element1, list):
        from dictionary_diff.list_diff import list_equivalent
        return list_equivalent(element1, element2)

    if isinstance(element1, dict):
        from dictionary_diff.dict_diff import dict_equivalent
        return dict_equivalent(element1, element2)

    return element1 == element2

def diff(orig, other, equivalent_func=equivalent):
    if isinstance(orig, dict) and isinstance(other, dict):
        from dictionary_diff.dict_diff import dict_diff
        return dict_diff(orig, other, equivalent_func=equivalent_func)

    if isinstance(orig, list) and isinstance(other, list):
        from dictionary_diff.list_diff import list_diff
        return list_diff(orig, other, equivalent_func=equivalent_func)
    
    return other
