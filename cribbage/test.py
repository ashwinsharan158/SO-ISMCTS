from cribbage.card import Card
from cribbage.score import score_hand

class determinization:
    def __init__(self, state=None, play=0, count=0):
        self.state = state
        self.play = play
        self.count = count
        self.TableP1 = []
        self.TableP2 = []
        self.go = False

'''
Its the transition function for the when we
take action 'a' on the chosen d to create a 
new determinization.
'''
def transtionFucntion(d, a):
    state = d.state
    hand = state[d.play]
    prePlays = state[1]
    count = d.count
    if isinstance(a, str):
        if d.go:
            d.count = 0
            d.go = False
            print("Go again count 0")
            return d
        d.go = True
        print("Go")
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
def action(d: determinization):
    state = d.state
    table = state[1]
    hand = state[d.play]
    actionList = []
    if not hand:
        actionList.append('No Card')
    elif all(d.count + card.value > 31 for card in hand):
        actionList.append('go')
    else:
        for card in hand:
            if d.count + card.value <=31:
                actionList.append(card)
    return actionList


'''
Tells if the game is at its terminal state.
'''
def terminal(d:determinization()):
    if not d.state[0]:
        if not d.state[2]:
            return True
    return False

'''
Reward calculation for each play.
'''
def rewardCal(d: determinization(), turnCard):
    player1Score = score_hand(d.TableP1, turnCard)
    print("score for player 1 "+ str(player1Score))
    player2Score = score_hand(d.TableP2, turnCard)
    print("score for player 2 "+ str(player2Score))
    reward = player1Score - player2Score
    return reward

if __name__ == '__main__':
    cards = [Card(n) for n in range(52)]
    prevPlays = [cards[8]]
    hand=[]
    hand.append(cards[40])
    hand.append(cards[4])
    hand.append(cards[36])
    hand.append(cards[43])
    subset=[]
    subset.append(cards[44])
    subset.append(cards[16])
    subset.append(cards[31])
    subset.append(cards[17])

    state = []
    state.append(hand)
    state.append(prevPlays)
    state.append(subset)
    d = determinization(state,0,0)
    print("---------------------------------")
    print(action(d))
    print("---------------------------------")
    d = transtionFucntion(d, cards[40])
    print(d.state[0])
    print(d.state[1])
    print(d.state[2])
    print(d.count)
    print(d.play)
    d = transtionFucntion(d, cards[44])
    print(d.state[0])
    print(d.state[1])
    print(d.state[2])
    print(d.count)
    print(d.play)
    d = transtionFucntion(d, cards[4])
    print(d.state[0])
    print(d.state[1])
    print(d.state[2])
    print(d.count)
    print(d.play)
    print("---------------------------------")
    print(action(d))
    print("---------------------------------")
    d = transtionFucntion(d, cards[16])
    print(d.state[0])
    print(d.state[1])
    print(d.state[2])
    print(d.count)
    print(d.play)
    d = transtionFucntion(d, cards[36])
    print(d.state[0])
    print(d.state[1])
    print(d.state[2])
    print(d.count)
    print(d.play)
    print("---------------------------------")
    print(action(d))
    print("---------------------------------")
    d = transtionFucntion(d, 'go')
    print(d.state[0])
    print(d.state[1])
    print(d.state[2])
    print(d.count)
    print(d.play)
    print(d.go)
    print("---------------------------------")
    print(action(d))
    print("---------------------------------")
    d = transtionFucntion(d, 'go')
    print(d.state[0])
    print(d.state[1])
    print(d.state[2])
    print(d.count)
    print(d.play)
    print(d.go)
    d = transtionFucntion(d, cards[43])
    print(d.state[0])
    print(d.state[1])
    print(d.state[2])
    print(d.count)
    print(d.play)
    print(d.go)
    d = transtionFucntion(d, cards[31])
    print(d.state[0])
    print(d.state[1])
    print(d.state[2])
    print(d.count)
    print(d.play)
    print(d.go)
    print("---------------------------------")
    print(action(d))
    print("---------------------------------")
    d = transtionFucntion(d, 'No cards')
    print(d.state[0])
    print(d.state[1])
    print(d.state[2])
    print(d.count)
    print(d.play)
    print(d.go)
    d = transtionFucntion(d, cards[17])
    print(d.state[0])
    print(d.state[1])
    print(d.state[2])
    print(d.TableP1)
    print(d.TableP2)
    print(d.count)
    print(d.play)
    print(d.go)
    print(terminal(d))
    rewardCal(d, cards[8])