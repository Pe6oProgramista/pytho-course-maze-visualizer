from dataclasses import dataclass

class KeyCombinationException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

@dataclass(frozen=True)
class KeyCombination:
    comb: int = 0

    def set_at(self, *positions: int) -> 'KeyCombination':
        new_comb = self.comb
        for pos in positions:
            if pos < 0:
                raise KeyCombinationException('Trying to set bit for a key with negative position')
            new_comb |= 1 << pos

        return KeyCombination(new_comb)

    def unset_at(self, *positions: int) -> 'KeyCombination':
        new_comb = self.comb
        for pos in positions:
            if pos < 0:
                raise KeyCombinationException('Trying to unset bit for a key with negative position')
            new_comb &= ~(1 << pos)

        return KeyCombination(new_comb)

    def is_set_at(self, pos: int) -> bool:
        if pos < 0:
            raise KeyCombinationException('Trying to check bit for a key with negative position')
        return bool(self.comb & (1 << pos))

    def keys_count(self) -> int:
        return bin(self.comb).count('1')

    # we want combinations with more keys to be earlier in the heapq
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, KeyCombination):
            return NotImplemented
  
        return self.keys_count() > other.keys_count()



__all__ = ['KeyCombination']
