"""
**change module exports:**
 * _Remove

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
