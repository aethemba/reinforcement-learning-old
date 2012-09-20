#DMIS Assignment 2 - Aksel Ethembabaoglu - 0154644
import random
import os

def initDeck():
    deck = ['j', 'q', 'k', 'a'] * 4
    return deck

def deal(deck):
        q = len(deck) - 1
        randomCardInt = random.randint(0, q)
        randomCard = deck[randomCardInt]
        del deck[randomCardInt]
        return (deck, randomCard)

def betRandom():
        a = random.randint(0,1)
        if a == 1:
                return True
        else:
                return False    

def determineWinner(playerHand, houseHand):
    player = [0, 0, 0]
    house = [0, 0, 0]
    
    if playerHand[0] == playerHand[1] == playerHand[2]:
        if playerHand[0] == 'a':
            player[0] = 100
        if playerHand[0] == 'k':
            player[0] = 90          
        if playerHand[0] == 'q':
            player[0] = 80
        if playerHand[0] == 'j':
            player[0] = 70
            
            
    if houseHand[0] == houseHand[1] == houseHand[2]:
        if houseHand[0] == 'a':
            house[0] = 100
        if houseHand[0] == 'k':
            house[0] = 90
        if houseHand[0] == 'q':
            house[0] = 80
        if houseHand[0] == 'j':
            house[0] = 70
        
    playerPair = checkPair(playerHand)
    
    if playerPair[0] == True:
        if playerPair[1] == 'a':
            player[1] = 60
        if playerPair[1] == 'k':
            player[1] = 59
        if playerPair[1] == 'q':
            player[1] = 58
        if playerPair[1] == 'j':
            player[1] = 57
            
    housePair = checkPair(houseHand)
    if housePair[0] == True:
        if housePair[1] == 'a':
            house[1] = 60
        if housePair[1] == 'k':
            house[1] = 59
        if housePair[1] == 'q':
            house[1] = 58
        if housePair[1] == 'j':
            house[1] = 57

    temp = highestCard(playerHand, houseHand)
    
    if temp[0] == True:
        player[2] = 4
    if temp[1] == True:
        house[2] = 4
    
    for i in range(0, 3):
        if player[i] > house[i]:
            winner = 'player'
            return winner
        if player[i] < house[i]:
            winner = 'house'
            return winner
    winner = 'draw'
    return winner
        
def highestCard(playerHand, houseHand):
    highestPlayer = 0
    highestHouse = 0
    for c in range(0,2):
        if playerHand[c] == 'a':
            if highestPlayer < 5:
                highestPlayer = 5
        if playerHand[c] == 'k':
            if highestPlayer < 4:
                highestPlayer = 4
        if playerHand[c] == 'q':
            if highestPlayer < 3:
                highestPlayer = 3       
        if playerHand[c] == 'j':
            if highestPlayer < 5:
                highestPlayer = 2           

    for c in range(0,2):
        if houseHand[c] == 'a':
            if highestHouse < 5:
                highestHouse = 5
        if houseHand[c] == 'k':
            if highestHouse < 4:
                highestHouse = 4
        if houseHand[c] == 'q':
            if highestHouse < 3:
                highestHouse = 3        
        if houseHand[c] == 'j':
            if highestHouse < 5:
                highestHouse = 2
    
    if highestPlayer > highestHouse:
        return (True, False)
    if highestPlayer < highestHouse:
        return (False, True)
    if highestPlayer == highestHouse:
        return (False, False)

def checkPair(hand):
    card1 = hand[0]
    card2 = hand[1]
    card3 = hand[2]
    
    if card1 == card2:
        return (True, card1)
    if card1 == card3:
        return (True, card1)
    if card2 ==card3:
        return (True, card2)
    return (False, card1)

def makeState(pot, playerHand, houseHand):
    ph = playerHand[0]
    for i in range(1, len(playerHand)):
        ph = ph + playerHand[i]
    state = ph
    if not houseHand == []:
        hh = houseHand[0]
        for i in range(1, len(houseHand)):
            hh = hh + houseHand[i]
        state = ph + hh 
    totalState = str(pot) + state
    print totalState
    return totalState
    
def stateSave(state, bet):
    if bet == True:
        tempBet = 't'
    else:
        tempBet = 'f'
    saveState = state + tempBet
    return saveState


def average(values):
    length = len(values)
    flattendValues = flatten(values)
    total = sum(flattendValues)
    averageValue = float(total)/float(length)
    return averageValue

def flatten(x):
    """flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

    result = []
    for el in x:
        #if isinstance(el, (list, tuple)):
        if hasattr(el, "__iter__"):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def changeTurn(turn):
    if turn == 0:
        return 1
    else:
        return 0

def getPolicy(state, mode, stateSpace):
        if mode == 'random':
                bet = betRandom()
                return bet
        if mode == 'MC':
                bet = eGreedyPolicy(state, stateSpace)
                return bet
        if mode == 'QL':
                bet = eGreedyPolicy(state, stateSpace)
                return bet
        if mode == 'SL':
                bet = eGreedyPolicy(state, stateSpace)
                return bet

def play(mode, stateSpace):
        deck = initDeck()
        playerHand = []
        houseHand = []
        pot = 0
        stateSpaceEpisode = dict()
        turn = 0
        for i in range(1,7):
                temp = deal(deck)
                deck = temp[0]
                card = temp[1]
                if turn == 0:
                        playerHand = playerHand + [card]
                        playerHand.sort()
                else:
                        houseHand = houseHand + [card]
                        houseHand.sort()
                state = makeState(pot, playerHand, houseHand)
                bet = getPolicy(state, mode, stateSpace)
                if i < 6:
                    if bet == True:
                            pot = pot + 2
                    #if turn == 1 and bet == True:
                    #        pot = pot + 1
                    stateSaved = stateSave(state, bet)
                    stateSpaceEpisode[stateSaved] = random.uniform(0,7)
                if i == 6:
                    stateSaved = state 
                    stateSpaceEpisode[stateSaved] = random.uniform(0,7)
                turn = changeTurn(turn)
        winner = determineWinner(playerHand, houseHand)
        return (winner, pot, stateSpaceEpisode)

def eGreedyPolicy(state, stateSpace):
    state1 = state + 'f'
    state2 = state + 't'
    if stateSpace.has_key(state1):
        value1 = stateSpace[state1]
    else:
        value1 = random.uniform(0,7)
    if stateSpace.has_key(state2):
        value2 = stateSpace[state2]
    else:
        value2 = random.uniform(0,7)

    if value1 > value2:
        highestAction = 'noBet'
    else:
        highestAction = 'bet'

    epsilon = float(1)/float(10)
    minProb = float(epsilon)/float(2)
    maxProb = 1 - minProb
    a = random.random()
    if a < maxProb:
        if highestAction == 'noBet':
            return False
        if highestAction == 'bet':
            return True
    else:
        if highestAction == 'noBet':
            return True
        if highestAction == 'bet':
            return False

def randomPokerAgent(numberOfGames):
    stateSpace = {}
    totalWinnings = 0
    totalLosses = 0
    wins = 0
    losses = 0
    for i in range(0,numberOfGames):
        #A) Generate an episode using Pi
        episode = play('random', stateSpace)
        winner = episode[0]
        pot = episode[1]
        stateSpaceEpisode = episode[2]
        if winner == 'player':
            winnings = float(pot)/float(2)
            totalWinnings = totalWinnings + winnings
            wins = wins + 1
        if winner == 'house':
            winnings = - float(pot)/float(2)
            totalLosses = totalLosses + winnings
            losses = losses + 1
        if winner == 'draw':
            winnings = 0
        print totalWinnings
        print totalLosses
    print "Netto gain for random poker agent over " + str(numberOfGames) + " games: " + str(totalWinnings + totalLosses)
        
def monteCarloPoker(numberOfGames):
    stateSpace = dict()
    returns = dict()
    totalWinnings = 0
    totalLosses = 0
    wins = 0
    losses = 0
    for i in range(0,numberOfGames):
        #A) Generate an episode using Pi
        episode = play('MC', stateSpace)
        winner = episode[0]
        pot = episode[1]
        stateSpaceEpisode = episode[2]
        if winner == 'player':
            winnings = float(pot)/float(2)
            totalWinnings = totalWinnings + winnings
            wins = wins + 1
        if winner == 'house':
            winnings = - float(pot)/float(2)
            totalLosses = totalLosses + winnings
            losses = losses + 1
        if winner == 'draw':
            winnings = 0

        #B) update returns for each state action pair in episode
        for (k) in stateSpaceEpisode:
                        if returns.has_key(k):
                            currentValue = returns[k]
                            newListTemp = [currentValue] + [winnings]
                            newList = flatten(newListTemp)
                            returns[k] = newList

                        else:
                            returns[k] = winnings
                #Update values for Q
        for (k) in stateSpaceEpisode:
                    returnValues = returns[k]
                    if stateSpace.has_key(k):
                        averageValue = average(returnValues)
                        stateSpace[k] = averageValue
                    else:
                        stateSpace[k] = returnValues

        i = 0
    #for (k, v) in stateSpace.iteritems():
    #            i = i + 1            
    #            if i > len(stateSpace) - 100:
    #               print k + ' ' + str(v)
    #print "Sum of all values: " + str(sumTemp)
    #print wins
    #print losses
    #print str(wins/losses)
    #print '#############'
    #print totalWinnings
    #print totalLosses
    print "Netto gain for Monte Carlo agent over " + str(numberOfGames) + " games: " + str(totalWinnings + totalLosses)
    
def qLearningPoker(numberOfGames):
        stateSpace = dict()
        returns = dict()
        totalWinnings = 0
        totalLosses = 0
        wins = 0
        losses = 0        
        for i in range(0,numberOfGames):
            episode = playQLearning('QL', stateSpace)
            winner = episode[0]
            pot = episode[1]
            stateSpace = episode[2]
            if winner == 'player':
                winnings = float(pot)/float(2)
                totalWinnings = totalWinnings + winnings
                wins = wins + 1
            if winner == 'house':
                winnings = - float(pot)/float(2)
                totalLosses = totalLosses + winnings
                losses = losses + 1
            if winner == 'draw':
                winnings = 0
            
        print 'Total winnings: ' + str(totalWinnings)
        print 'Total losses: ' + str(totalLosses)
        print "Netto gain for Q Learning agent over " + str(numberOfGames) + " games: " + str(totalWinnings + totalLosses)
        
    
    
    
    
def succStateActionValue(state, stateSpace):
    #remove action
    tempState = state[:-1]
    size = len(tempState)
    value = -10
    #search for successor with highest value
    for (k,v) in stateSpace.iteritems():
        if k[0:size] == tempState and len(k) == size + 2:
            if stateSpace[k] > value:
                succStateAction = k
                value = stateSpace[k]
    if value == -10:
        value = 0
        
    #return the value of the succes state/action with the highest value 
    return value    


def playQLearning(mode, stateSpace):
    deck = initDeck()
    playerHand = []
    houseHand = []
    pot = 0
    stateSpaceEpisode = dict()
    turn = 0
    totalWinnings = 0
    totalLosses = 0
    wins = 0
    losses = 0
    for i in range(1,7):
        temp = deal(deck)
        deck = temp[0]
        card = temp[1]
        if turn == 0:
            playerHand = playerHand + [card]
            playerHand.sort()
        else:
            houseHand = houseHand + [card]
            houseHand.sort()
        state = makeState(pot, playerHand, houseHand)
        #
        bet = getPolicy(state, mode, stateSpace)
        #Do actions for first 4 rounds
        #Observe action and next state
        if i < 5:
            if bet == True:
                #house and player both bet one
                pot = pot + 2
            #if turn == 1 and bet == True:
            #    pot = pot + 1 
            #current state/action
            currentQsa = stateSave(state, bet)
            #If current state/action does not exist, generate random number for Q
            if not stateSpace.has_key(currentQsa):
                stateSpace[currentQsa] = random.uniform(0,7)
            #Generate new Q
            highestSuccessorValue = succStateActionValue(currentQsa, stateSpace)
            valueCurrentStateAction = stateSpace[currentQsa]
            stateSpace[currentQsa] = valueCurrentStateAction + 0.1*(0 + highestSuccessorValue - valueCurrentStateAction)
        if i == 5:
            if bet == True:
                pot = pot + 2
            #if turn == 1 and bet == True:
            #    pot = pot + 1 
            #current state/action
            currentQsa = stateSave(state, bet)
            #If current state/action does not exist, generate random number for Q
            if not stateSpace.has_key(currentQsa):
                stateSpace[currentQsa] = random.uniform(0,7)
            #Generate new Q
            highestSuccessorValue = succStateActionValue(currentQsa, stateSpace)
            valueCurrentStateAction = stateSpace[currentQsa]
            oneLastState = currentQsa
        turn = changeTurn(turn)
            
    winner = determineWinner(playerHand, houseHand)
    if winner == 'player':
                winnings = float(pot)/float(2)
                totalWinnings = totalWinnings + winnings
                wins = wins + 1
    if winner == 'house':
                winnings = - float(pot)/float(2)
                totalLosses = totalLosses + winnings
                losses = losses + 1
    if winner == 'draw':
                winnings = 0            
    stateSpace[oneLastState] = valueCurrentStateAction + 0.1*(winnings + highestSuccessorValue - valueCurrentStateAction)
    return (winner, pot, stateSpace)

def sarsaLambdaPoker(numberOfGames):
    stateSpace = dict()
    returns = dict()
    totalWinnings = 0
    totalLosses = 0
    wins = 0
    losses = 0
    eligible = dict()
    for i in range(0,numberOfGames):
        episode = playSarsa('SL', stateSpace, eligible)
        winner = episode[0]
        pot = episode[1]
        stateSpace = episode[2]
        if winner == 'player':
            winnings = pot/2
            totalWinnings = totalWinnings + winnings
            wins = wins + 1
        if winner == 'house':
            winnings = - pot/2
            totalLosses = totalLosses + winnings
            losses = losses + 1
        if winner == 'draw':
            winnings = 0
            
    print 'Total winnings: ' + str(totalWinnings)
    print 'Total losses: ' + str(totalLosses)
    print "Netto gain for Sarsa Learning agent over " + str(numberOfGames) + " games: " + str(totalWinnings + totalLosses)
    
#copied from qlearning
def playSarsa(mode, stateSpace, eligible):
    deck = initDeck()
    playerHand = []
    houseHand = []
    pot = 0
    stateSpaceEpisode = dict()
    turn = 0
    totalWinnings = 0
    totalLosses = 0
    wins = 0
    losses = 0
    for i in range(1,7):
        temp = deal(deck)
        deck = temp[0]
        card = temp[1]
        if turn == 0:
            playerHand = playerHand + [card]
            playerHand.sort()
        else:
            houseHand = houseHand + [card]
            houseHand.sort()
        state = makeState(pot, playerHand, houseHand)
        bet = getPolicy(state, mode, stateSpace)

        if i < 5:
            if bet == True:
                pot = pot + 2
            currentQsa = stateSave(state, bet)
            stateSpaceEpisode[currentQsa] = 0
            if not stateSpace.has_key(currentQsa):
                stateSpace[currentQsa] = random.uniform(0,7)
            highestSuccessorValue = succStateActionValue(currentQsa, stateSpace)
            valueCurrentStateAction = stateSpace[currentQsa]
            stateSpace[currentQsa] = valueCurrentStateAction + 0.1*(0 + highestSuccessorValue - valueCurrentStateAction)
            delta = highestSuccessorValue - valueCurrentStateAction
            if not eligible.has_key(currentQsa):
                eligible[currentQsa] = random.random()
            eligible[currentQsa] = eligible[currentQsa] + 1
            for (k) in stateSpaceEpisode:
                stateSpace[k] = stateSpace[k] + 0.1 * delta * eligible[k]
                eligible[k] = 0.9 * eligible[k]
            

            
        if i == 5:
            if bet == True:
                pot = pot + 2
            currentQsa = stateSave(state, bet)
            stateSpaceEpisode[currentQsa] = 0
            if not stateSpace.has_key(currentQsa):
                stateSpace[currentQsa] = random.uniform(0,7)
            highestSuccessorValue = succStateActionValue(currentQsa, stateSpace)
            valueCurrentStateAction = stateSpace[currentQsa]
            oneLastState = currentQsa
        turn = changeTurn(turn)
            
    winner = determineWinner(playerHand, houseHand)
    if winner == 'player':
                winnings = float(pot)/float(2)
                totalWinnings = totalWinnings + winnings
                wins = wins + 1
    if winner == 'house':
                winnings = - float(pot)/float(2)
                totalLosses = totalLosses + winnings
                losses = losses + 1
    if winner == 'draw':
                winnings = 0            
    delta = winnings + highestSuccessorValue - valueCurrentStateAction
    if not eligible.has_key(oneLastState):
            eligible[oneLastState] = random.random()
    eligible[oneLastState] = eligible[currentQsa] + 1
    for (k) in stateSpaceEpisode:
        stateSpace[k] = stateSpace[k] + 0.1 * delta * eligible[k]
        eligible[k] = 0.9 * eligible[k]
            
    return (winner, pot, stateSpace)    
        
