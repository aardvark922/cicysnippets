from otree.api import *


doc = """
a participants is in two different groups at the same time, one with other 3 players, one with other 1 player.
"""


class C(BaseConstants):
    NAME_IN_URL = 'simultaneous_two_groups'
    #group 1 size
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 30
    NUM_SUPER_GAMES = 3

    SUPER_GROUP_SIZE = PLAYERS_PER_GROUP*2
    #group 2 size
    PLAYERS_PER_GROUP2 = 2


class Subsession(BaseSubsession):
    pass

#Functions

def creating_session(subsession: Subsession):
    # Importing modules needed
    from random import randint, shuffle
    # Get Constants attributes once for all
    # List of starting round for each super game
    super_games_start_round = [1] + [randint(3, 10) + 1 for _ in range(C.NUM_SUPER_GAMES)]
    # Set pairs IDs to identify who is matched with whom
    pair_ids = [n for n in range(1, C.SUPER_GROUP_SIZE // C.PLAYERS_PER_GROUP2 + 1)] * C.PLAYERS_PER_GROUP2

    # If the current round is the first round of a super game, then set the supergroups
    if subsession.round_number in super_games_start_round:
        # Get all players in the session and in the current round
        ps = subsession.get_players()
        # Apply in-place permutation
        shuffle(ps)
        # Set list of list, where each sublist is a supergroup
        super_groups = [ps[n:n + C.SUPER_GROUP_SIZE] for n in range(0, len(ps), C.SUPER_GROUP_SIZE)]
        # Set group matrix in oTree based on the supergroups
        subsession.set_group_matrix(super_groups)
        # Call the set_pairs function
        set_pairs(subsession, pair_ids)

    # If the current round is not the first round of a super game, then just set new pairs
    else:
        # Set group matrix in oTree based on the matrix of the previous round
        subsession.group_like_round(subsession.round_number - 1)
        # Call the set_pairs function
        set_pairs(subsession, pair_ids)


def set_pairs(subsession: Subsession, pair_ids: list):
    from random import shuffle
    # Get the supergroups for this round
    super_groups = subsession.get_groups()
    for g in super_groups:
        players = g.get_players()
        shuffle(pair_ids)
        for n, p in enumerate(players[:len(players)]):
            p.pair_id = pair_ids[n]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pair_id = models.IntegerField(initial=0)
    decision = models.BooleanField()


# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
