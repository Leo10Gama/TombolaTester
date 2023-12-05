"""Represents someone who plays Tombola."""


from typing import List, Tuple

from tombola_card import TombolaCard, TombolaStatus


class TombolaPlayer:

    name: str
    cards: List[TombolaCard]
    status: TombolaStatus

    def __init__(self, name: str, cards: List[TombolaCard]):
        self.name = name
        self.cards = cards
        self.status = TombolaStatus.NOTHING
    
    def mark_cards(self, number: int) -> Tuple[TombolaStatus, TombolaCard]:
        changed_card = None
        curr_status = self.status
        for card in self.cards:
            card_status = card.mark_number(number)
            self.status = TombolaStatus(max(self.status.value, card_status.value))
            if self.status != curr_status:
                changed_card = card
                curr_status = self.status
        return self.status, changed_card
    
    def reset_player(self):
        self.status = TombolaStatus.NOTHING
        for card in self.cards:
            card.reset_card()
