from otree.api import *


doc = """
a participants is in two different groups at the same time, one with other 3 players, one with other 1 player.
"""


class C(BaseConstants):
    NAME_IN_URL = 'simultaneous_two_groups'
    #group 1 size
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 30

    super_games_start_round= [1,4,7,10]

    SUPER_GROUP_SIZE = PLAYERS_PER_GROUP*2
    #group 2 size
    PLAYERS_PER_GROUP2 = 2


class Subsession(BaseSubsession):
    pass

#Functions

def creating_session(subsession: Subsession):
    # Importing modules needed
    from random import shuffle
    if subsession.round_number in C.super_games_start_round:
        # Get all players in the session and in the current round
        ps = subsession.get_players()
        # Apply in-place permutation
        shuffle(ps)
        #regroup players in the first period of each supergame
        subsession.group_randomly()
        for p in ps:
            p.pair_id = p.id_in_group

    # If the current round is not the first round of a super game, copy group and pair IDs
    else:
        # Set group matrix in oTree based on the matrix of the previous round
        subsession.group_like_round(subsession.round_number - 1)
        ps = subsession.get_players()
        # Apply in-place permutation
        for p in ps:
            p.pair_id = p.id_in_group


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
