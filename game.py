"""The code for the game master."""

from collections import defaultdict
import logging
from random import sample
from typing import Dict, List

from players import TombolaPlayer
from tombola_card import TombolaStatus, import_cards


logging.basicConfig(filename='stats.log', filemode='w+', format='%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 


def play_round(players: List[TombolaPlayer]):
    numbers_to_call = sample(range(1, 91), 90)
    players_statuses: Dict[str, TombolaStatus] = {player.name: TombolaStatus.NOTHING for player in players}
    game_status = TombolaStatus.NOTHING  # what the highest call has been so far
    called_numbers = set()

    for number in numbers_to_call:
        print(f"Calling {number}")
        called_numbers.add(number)
        changes_in_status = []
        for player in players:
            new_player_status, changed_card = player.mark_cards(number)
            if players_statuses[player.name] != new_player_status and new_player_status.value > game_status.value:
                changes_in_status.append(player.name)
                players_statuses[player.name] = new_player_status
                print(changed_card)
        if changes_in_status:
            game_status = TombolaStatus(game_status.value + 1)
            if len(changes_in_status) > 1:
                print(f"Multiple players have won {game_status.name}: {changes_in_status}!")
            else:
                print(f"{changes_in_status[0]} has won {game_status.name}!")
            if game_status == TombolaStatus.TOMBOLA:
                print("Game has ended!")
                break
            changes_in_status = []
        
        # vvv For slow control vvv
        # user_input = ""
        # while user_input != "n":
        #     user_input = input("What would you like to do?\n(q) query if a number is out\n(n) next number\n").lower()
        #     if user_input == "q":
        #         number_to_query = int(input("Enter a number: "))
        #         print(f"{number_to_query} {'HAS' if number_to_query in called_numbers else 'has NOT'} been called")

def simulate_rounds(players: List[TombolaPlayer], rounds: int):
    """Simulate a number of rounds between TombolaPlayers and record the results."""
    # Stats to collect
    terno_wins = defaultdict(int)
    oneline_wins = defaultdict(int)
    twoline_wins = defaultdict(int)
    tombola_wins = defaultdict(int)
    player_wins = defaultdict(int)

    for _ in range(rounds):
        # Round setup
        numbers_to_call = sample(range(1, 91), 90)
        players_statuses: Dict[str, TombolaStatus] = {player.name: TombolaStatus.NOTHING for player in players}
        game_status = TombolaStatus.NOTHING  # what the highest call has been so far
        called_numbers = set()

        for number in numbers_to_call:
            called_numbers.add(number)
            changes_in_status = []
            for player in players:
                new_player_status, changed_card = player.mark_cards(number)
                if players_statuses[player.name] != new_player_status and new_player_status.value > game_status.value:
                    changes_in_status.append(player.name)
                    players_statuses[player.name] = new_player_status
                    if new_player_status == TombolaStatus.TERNO:
                        terno_wins[changed_card.card_id] += 1
                    elif new_player_status == TombolaStatus.ONE_LINE:
                        oneline_wins[changed_card.card_id] += 1
                    elif new_player_status == TombolaStatus.TWO_LINES:
                        twoline_wins[changed_card.card_id] += 1
                    elif new_player_status == TombolaStatus.TOMBOLA:
                        tombola_wins[changed_card.card_id] += 1
                        player_wins[player.name] += 1
            if changes_in_status:
                game_status = TombolaStatus(game_status.value + 1)
                if game_status == TombolaStatus.TOMBOLA:
                    break
                changes_in_status = []

        # reset for next round
        for player in players:
            player.reset_player()
    return {
        "terno_wins": terno_wins,
        "oneline_wins": oneline_wins,
        "twoline_wins": twoline_wins,
        "tombola_wins": tombola_wins,
        "player_wins": player_wins
    }

if __name__=='__main__':
    cards = import_cards()
    caller_cards = cards[-6:]
    cards = cards[:-6]
    number_of_players = 1  # not including caller
    cards_per_player = 96
    cards_to_distribute = sample(cards, number_of_players * cards_per_player)
    players = [TombolaPlayer("Caller", caller_cards)]
    for i in range(number_of_players):
        players.append(TombolaPlayer(f"Player {i+1}", cards_to_distribute[(i*cards_per_player):(i*cards_per_player)+cards_per_player]))
    stats = simulate_rounds(players, 100000)

    print("TERNO WINS")
    logger.info("TERNO WINS")
    for card_num, wins in stats['terno_wins'].items():
        print(f"{card_num:3}: {wins:3} wins")
        logger.info("%s, %s", card_num, wins)
    
    print("ONE LINE WINS")
    logger.info("ONE LINE WINS")
    for card_num, wins in stats['oneline_wins'].items():
        print(f"{card_num:3}: {wins:3} wins")
        logger.info("%s, %s", card_num, wins)
    
    print("TWO LINE WINS")
    logger.info("TWO LINE WINS")
    for card_num, wins in stats['twoline_wins'].items():
        print(f"{card_num:3}: {wins:3} wins")
        logger.info("%s, %s", card_num, wins)
    
    print("TOMBOLA WINS")
    logger.info("TOMBOLA WINS")
    for card_num, wins in stats['tombola_wins'].items():
        print(f"{card_num:3}: {wins:3} wins")
        logger.info("%s, %s", card_num, wins)
    
    print("PLAYER WINS")
    for player, wins in stats['player_wins'].items():
        logger.info("%s, %s", card_num, wins)