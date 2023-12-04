"""Representation of a Tombola card."""


from enum import Enum
from random import sample
from typing import List


class TombolaStatus(Enum):
    NOTHING = 0
    TERNO = 1
    ONE_LINE = 2
    TWO_LINES = 3
    TOMBOLA = 4


class TombolaCard:
    """Representation of a Tombola card.
    
    The card_id param is the unique number of the card.

    The card param is a list of the three rows of the card, from top
    to bottom.

    The status param is used to determine the current state of the
    card. That is, starting with "NOTHING", then moving up to "TERNO"
    when three numbers are in a row, then "ONE_LINE" when one line is
    formed, and so on. Due to the nature of the game, this status can
    only increment by one for every number called, since cards cannot
    have duplicate numbers.

    The marked_per_row param is used internally to keep track of how
    many numbers in a given row have been called. It should be a list
    of size exactly 3, with each spot initialized to 0. For example,
    if one of the numbers is "3", the card has "terno"; if one of the
    numbers is "5", one line; if two are "5", two lines; if all three
    are "5", tombola!
    """

    card_id: int
    card: List[List[int]]
    status: TombolaStatus
    _marked_per_row: List[int]

    def __init__(self, card_id: int, numbers: List[int]):
        """Constructor for the TombolaCard.
        
        The list of numbers should be provided in order, as read from
        right to left, omitting blank spaces, such that it is of size
        15, incrementing from smallest to largest 0-4, 5-9, and
        10-15.
        """
        self.card_id = card_id
        self.card = [numbers[0:5], numbers[5:10], numbers[10:15]]
        self.status = TombolaStatus.NOTHING
        self._marked_per_row = [0, 0, 0]

    def __repr__(self):
        result = f"Card {self.card_id}:\n"
        for card_row in self.card:
            card_index = 0
            for i in range(9):
                if card_index <= 4 and (card_row[card_index] // 10 == i or (card_row[card_index] == 90 and i == 8)):
                    result += f"|{card_row[card_index]:2}"
                    card_index += 1
                else:
                    result += "|  "
            result += "|\n"
        return result[:-1]  # trim last '\n'

    def mark_number(self, number: int) -> TombolaStatus:
        """Mark a number from the card, returning the status after marking."""
        for i, row in enumerate(self.card):
            if number in row:
                self._marked_per_row[i] += 1
                if self._marked_per_row[i] == 3 and self.status.value < TombolaStatus.TERNO.value:
                    self.status = TombolaStatus.TERNO
                elif self._marked_per_row[i] == 5:
                    self.status = TombolaStatus(self.status.value + 1)
                break
        return self.status

def demo():
    card = TombolaCard(23, [23, 32, 51, 64, 83, 8, 15, 35, 57, 72, 16, 29, 48, 78, 87])
    print(card)
    nums_to_call = sample(range(1, 91), 90)
    print(len(nums_to_call))
    for number in nums_to_call:
        print(f"Calling {number} -> {card.mark_number(number)}")
        if card.status == TombolaStatus.TOMBOLA:
            print("Game over!")
            break

    
if __name__=='__main__':
    demo()
