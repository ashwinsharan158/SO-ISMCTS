import math
import random
from itertools import combinations
from random import choice, shuffle
from card import Deck
import numpy as np
from tqdm import tqdm

from .score import score_hand, score_count
from .card import Deck
import copy

class WinGame(Exception):
    pass


class Player:
    """
    Here we define a base class for the various kinds of players in the 
    cribbage game. To define your own player, inherit from this class and 
    implement ``ask_for_input`` and ``ask_for_discards``
    """

    def __init__(self, name=None):
        self.turn_card = None
        self.name = name
        self.hand = []  # cards in player's hand
        self.table = [] # cards on table in front of player
        self.crib = []  # cards in player's crib
        self.score = 0
        self.count = 0
        self.go =False
        #self.lastPlay = []
        self.plays = []
        self.enemyTable = []
    # Discards

    def ask_for_discards(self):
        """Should return two cards from the player"""
        raise Exception("You need to implement `ask_for_discards` yourself")


    def update_after_discards(self, discards):
        for discard in discards:
            self.hand.remove(discard)


    def discards(self):
        cards = self.ask_for_discards()
        self.update_after_discards(cards)
        return cards


    # Counting plays

    def ask_for_play(self, previous_plays):
        """Should return a single card from the player

        Private method"""
        raise Exception("You need to implement `ask_for_play` yourself")


    def update_after_play(self, play):
        """Private method"""
        
        self.table.append(play)
        self.hand.remove(play)


    def play(self, count, previous_plays, turn_card, go):
        """Public method"""
        self.go = go
        self.turn_card = turn_card
        self.count = count
        if len(self.plays) + 1 > 8 or len(self.hand) == 4:
            self.plays = []
        for x in previous_plays:
            if x not in self.plays:
                self.plays.append(x)
        if not self.hand:
            print('>>> I have no cards', self)
            return "No cards!"
        elif all(count + card.value > 31 for card in self.hand):
            print(">>>", self, self.hand, "I have to say 'go' on that one")
            return "Go!"
        while True:
            card = self.ask_for_play(previous_plays)  # subclasses (that is, actual players) must implement this
            print("Nominated card", card)

            if sum((pp.value for pp in previous_plays)) + card.value < 32:
                self.update_after_play(card)
                return card
            else: 
                # `self.ask_for_play` has returned a card that would put the 
                # score above 31 but the player's hand contains at least one
                # card that could be legally played (you're not allowed to say
                # "go" here if you can legally play). How the code knows that 
                # the player has a legal move is beyond me
                print('>>> You nominated', card, 'but that is not a legal play given your hand. You must play if you can')


    # Scoring

    def peg(self, points):
        self.score += points
        if self.score > 120:
            self.win_game()


    def count_hand(self, turn_card):
        """Count the hand (which should be on the table)"""
        score = score_hand(self.table, turn_card)
        self.peg(score)
        return score 


    def count_crib(self, turn_card):
        """Count crib, with side effect of pegging the score"""
        score = score_hand(self.crib, turn_card)
        self.peg(score)
        return score 


    def win_game(self):
        raise WinGame(f"""Game was won by {self}  """
                      f"""{self.score} {self.table}""")


    @property
    def sorted_hand(self):
        return sorted(self.hand, key=lambda c: c.index)

    def __repr__(self):
        if self.name:
            return self.name + f'(score={self.score})'
        return str(self.__class__) + f'(score={self.score})'


class RandomPlayer(Player):
    """
    A player who plays randomly
    """

    def ask_for_play(self, previous_plays):
        shuffle(self.hand) # this handles a case when 0 is not a legal play
        return self.hand[0]


    def ask_for_discards(self):
        return self.hand[0:2]


class HumanPlayer(Player):
    """
    A human player. This class implements scene rendering and taking input from
    the command line 
    """


    def ask_for_play(self, previous_plays):
        """Ask a human for a card during counting"""
        
        d = dict(enumerate(self.hand, 1))
        print(f">>> Your hand ({self}):", " ".join([str(c) for c in self.hand]))

        while True:
            inp = input(">>> Card number to play: ") or "1"
            if len(inp) > 0 and int(inp) in d.keys():
                card = d[int(inp)]
                return card


    def ask_for_discards(self):
        """After deal, ask a human for two cards to discard to crib"""

        d = dict(enumerate(self.sorted_hand, 1))

        print('>>> Please nominate two cards to discard to the crib')
        print(f'>>> {d[1]} {d[2]} {d[3]} {d[4]} {d[5]} {d[6]}')
        discard_prompt = ">>> "

        while True:
            inp = input(discard_prompt) or "12"
            cards = [d[int(i)] for i in inp.replace(" ", "").replace(",", "")]
            if len(cards) == 2:
                print(f">>> Discarded {cards[0]} {cards[1]}")
                return cards


class GreedyAgentPlayer(Player):
    """
    "Expert systems" style AI player that systematically
    enumerates possible moves and chooses the move that
    maximizes its score after the move
    """

    def ask_for_discards(self):
        return self.hand[0:2]


    def ask_for_play(self, previous_plays):
        """
        Calculate points for each possible play in your hand
        and choose the one that maximizes the points
        """

        scores = []
        plays = []
        for card in self.hand:
            plays.append(card)
            scores.append(score_count(previous_plays + [card]))
        max_index = np.argmax(scores)

        return plays[max_index]


# class TrainedAIPlayer(Player):
#     """
#     A player that makes choices based on previous games
#     """

#     def __init__(self, name=""):
#         # override this constructor becasue I want to
#         # load the ML model in when we init AIPlayer instance
#         self.name = name
#         self.hand = []
#         self.score = 0
#         self.debug = False
#         self.model = load_trained_model()  # trained model we can ask directly for plays

#     def ask_for_input(self, play_vector):
#         card = self.model.ask_for_pegging_play(play_vector, self.in_hand)
#         card.ontable = True
#         return card

#     def ask_for_discards(self):
#         cards = self.model.ask_model_for_discard(
#             self.hand
#         )  # note: returns card objects
#         self.hand = [n for n in self.hand if n not in cards]
#         return cards


NondeterministicAIPlayer = RandomPlayer

class Node:
    """
    A representation of a single board state.
    MCTS works by constructing a tree of these Nodes.
    Could be e.g. a chess or checkers board state.
    """
    def __init__(self, action, parent, InfoSet):
        self.visit = 0
        self.action =  action
        self.parent = parent
        self.reward = 0
        self.childNode = []
        self.InfoSet = InfoSet
        self.availabilityCount = 0
        self.selections = []
        self.player = 0
        if parent is not None:
            if parent.player == 0:
                self.player = 2


    def setChildNode(self, child):
        self.childNode.append(child)


class determinization:
    def __init__(self, state=None, play=0, count=0):
        self.state = state # [[Cards][Table cards][Enemy Cards]]
        self.play = play #[Cards no longer being counted]
        self.count = count #Count of cards
        self.TableP1 = []  #Cards already played
        self.TableP2 = []  #Cards played by the enemy
        self.go = False # Go has been said or not.

class singleObserverISMCTS(Player):

    """
    Here we create a n-possible game state based on what we
    already know about the game.
    """
    def InformationSet(self, hand):
        self.enemyTable = []
        deck = Deck()
        state = []
        InfoSet = []
        # We record the seen cards that are excluded from creating a
        # combination.
        seenCards = hand + self.plays + self.crib
        seenCards.append(self.turn_card)
        # We calulate the number of cards in enemy hand.
        enemyCardCount = 8 - len(hand) - len(self.plays)
        # We create a list of unseen cards.
        unseenCards = [n for n in deck.cards if n not in seenCards]
        # If enemy has no cards to play there is only one possible state.
        if enemyCardCount <= 0:
            state.append(hand)
            state.append(self.plays)
            state.append([])
            InfoSet.append(state)
        else:
            # We create a compbination of unseen cards the enemy can
            # have.
            for subset in combinations(unseenCards, enemyCardCount):
                state.append(hand)
                state.append(self.plays)
                state.append(list(subset))
                InfoSet.append(state)
                state = []
        for x in self.plays:
            if x not in self.table:
                self.enemyTable.append(x)
        return InfoSet

    def ask_for_play(self, previous_plays):
        InfoSet = self.InformationSet(self.hand)
        v_init = Node(None, None, InfoSet)
        i = 0
        for _ in range(1000):
            d = determinization()
            state = random.choices(InfoSet)
            state = copy.deepcopy(state[0])
            d.state = state
            d.count = copy.deepcopy(self.count)
            d.TableP2 = copy.deepcopy(self.enemyTable)
            d.TableP1 = copy.deepcopy(self.table)
            d.go = copy.deepcopy(self.go)
            (v, d) = self.selection(v_init, d)
            if not isinstance(self.childAction(v, d),str):
                (v,d) = self.Expand( v, d)
            reward = self.simulation(d)
            self.Backpropagate(reward,v)
        action = self.maxVisitAction(v_init)
        self.plays.append(action)
        return action

    def ask_for_discards(self):
        return self.hand[0:2]

    def selection(self, v, d):
        while not self.terminal(d) and self.validNode(v,d):
            uct = self.uctCalc(v,d)
            v.selections = uct.keys()
            child = max(uct, key=uct.get)
            v = child
            d = self.transtionFucntion(d, child.action)
        return v, d

    '''
    Actions from the determinization for which v does not 
    have children. Where d is the derterminization for the
    information set to which v corresponds to.
    '''
    def childAction(self, v:Node, d:determinization):
        dc = copy.deepcopy(d)
        for w in v.childNode:
            if w.action in dc.state[dc.play]:
                dc.state[dc.play].remove(w.action)
        return self.action(dc)


    def Expand(self, v, d):
        a = random.choices(self.childAction(v,d))
        a = a[0]
        w = Node(a, v, None)
        v.setChildNode(w)
        return w, self.transtionFucntion(d, a)



    def simulation(self, dc):
        d = copy.deepcopy(dc)
        while not self.terminal(d):
            a = random.choices(self.action(d))
            a = a[0]
            d = self.transtionFucntion(d, a)
        return self.rewardCal(d)

    def Backpropagate(self, r, v:Node):
        k = v
        while k.parent is not None:
            v.visit+=1
            v.reward = v.reward + r
            v.availabilityCount +=1
            for w in v.selections:
                w.availabilityCount +=1
            k = k.parent


    '''
    Its the transition function for the when we
    take action 'a' on the chosen d to create a 
    new determinization.
    '''
    def transtionFucntion(self, d: determinization(), a):
        state = d.state
        hand = state[d.play]
        prePlays = state[1]
        count = d.count
        if isinstance(a, str):
            if d.go:
                d.count = 0
                d.go = False
                return d
            d.go = True
        else:
            d.count += a.value
            if d.play == 0:
                d.TableP1.append(a)
            else:
                d.TableP2.append(a)
            prePlays.append(a)
            hand.remove(a)
            if count == 31:
                d.count = 0
        if d.play == 0:
            d.play = 2
        else:
            d.play = 0
        return d

    '''
    Possible action of both player, one after the other
    '''
    def action(self, d: determinization):
        state = d.state
        hand = state[d.play]
        actionList = []
        if not hand:
            actionList.append('No Card')
        elif all(d.count + card.value > 31 for card in hand):
            actionList.append('go')
        else:
            for card in hand:
                if d.count + card.value <= 31:
                    actionList.append(card)
        return actionList


    '''
    Tells if the game is at its terminal state.
    '''

    def terminal(self, d: determinization()):
        if not d.state[0]:
            if not d.state[2]:
                return True
        return False

    '''
    Takes in reward of each child, number of vists for 
    each child and availability count and taking k = 2
    '''
    def uctCalc(self, v, d):
        uct = {}
        child = []
        hand = d.state[d.play]
        for x in v.childNode:
            if x.action in hand:
                child.append(x)
        for w in child:
            if v.visit > 0:
                uct[w] = (w.reward/w.visit) + math.sqrt(2*math.log(w.availabilityCount)/w.visit)
            else:
                uct[w] = 0
                return uct
        return uct

    '''
    Reward calculation for each play.
    '''
    def rewardCal(self, d: determinization()):
        player1Score = score_hand(d.TableP1, self.turn_card)
        player2Score = score_hand(d.TableP2, self.turn_card)
        reward = player1Score - player2Score
        return reward

    def maxVisitAction(self, v_init: Node):
        temp = v_init.childNode[0]
        for w in v_init.childNode:
            if temp.visit < w.visit:
                if not isinstance(w.action, str):
                    temp = w
        return temp.action

    def validNode(self,v,d):
        if isinstance(self.childAction(v,d)[0],str):
            return False
        else:
            hand = d.state[d.play]
            actions = [w.action for w in v.childNode]
            for a in actions:
                if a in hand:
                    return True
            return False



