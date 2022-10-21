from otree.api import *

c = Currency

doc = """
Sample app to show how to generate nested groups in oTree.
Here, we consider super groups of size 7, with 1 observer and 3 nested groups of size 2.
"""


class Constants(BaseConstants):
    name_in_url = 'nested_groups'
    players_per_group = None
    num_rounds = 40

    num_super_games = 3

    # Nested groups parameters
    super_group_size = 7
    obersever_num = 1
    group_size = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pair_id = models.IntegerField(initial=0)
    decision = models.BooleanField()


# FUNCTIONS
def creating_session(subsession: Subsession):
    # Importing modules needed
    from random import randint, shuffle
    # Get Constants attributes once for all
    const = Constants
    # List of starting round for each super game
    super_games_start_round = [1] + [randint(3, 10) + 1 for _ in range(const.num_super_games)]
    # Set pairs IDs to identify who is matched with whom
    pair_ids = [n for n in range(1, const.super_group_size // const.group_size + 1)] * const.group_size

    # If the current round is the first round of a super game, then set the supergroups
    if subsession.round_number in super_games_start_round:
        # Get all players in the session and in the current round
        ps = subsession.get_players()
        # Apply in-place permutation
        shuffle(ps)
        # Set list of list, where each sublist is a supergroup
        super_groups = [ps[n:n + const.super_group_size] for n in range(0, len(ps), const.super_group_size)]
        # Set group matrix in oTree based on the supergroups
        subsession.set_group_matrix(super_groups)
        # Call the set_pairs function
        set_pairs(subsession, pair_ids, const.obersever_num)

    # If the current round is not the first round of a super game, then just set new pairs
    else:
        # Set group matrix in oTree based on the matrix of the previous round
        subsession.group_like_round(subsession.round_number - 1)
        # Call the set_pairs function
        set_pairs(subsession, pair_ids, const.obersever_num)


# Within each supergroup, randomly assign a paird ID, excluding the last player who will be an observer
def set_pairs(subsession: Subsession, pair_ids: list, obersever_num: int):
    from random import shuffle
    # Get the supergroups for this round
    super_groups = subsession.get_groups()
    for g in super_groups:
        players = g.get_players()
        shuffle(pair_ids)
        for n, p in enumerate(players[:len(players) - obersever_num]):
            p.pair_id = pair_ids[n]


def set_other_player(player: Player):
    return [p for p in player.get_others_in_group() if p.pair_id == player.pair_id][0]



# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]