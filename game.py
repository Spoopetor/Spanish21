import random
import time
import os

TITLE = "   _____                   _     _     ___  __\n  / ____|                 (_)   | |   |__ \/_ |\n | (___  _ __   __ _ _ __  _ ___| |__    ) || |\n  \___ \| '_ \ / _` | '_ \| / __| '_ \  / / | |\n  ____) | |_) | (_| | | | | \__ \ | | |/ /_ | |\n |_____/| .__/ \__,_|_| |_|_|___/_| |_|____||_|\n        | |                                    \n        |_|          \n"
START = "  _          _   _       ____             _       _ \n | |        | | ( )     |  _ \           (_)     | |\n | |     ___| |_|/ ___  | |_) | ___  __ _ _ _ __ | |\n | |    / _ \ __| / __| |  _ < / _ \/ _` | | '_ \| |\n | |___|  __/ |_  \__ \ | |_) |  __/ (_| | | | | |_|\n |______\___|\__| |___/ |____/ \___|\__, |_|_| |_(_)\n                                     __/ |          \n                                    |___/           "
CARDORDERS = {"A": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "J": 9, "Q": 10, "K": 11}
VALSCORES = {"A": (1, 11), "2": (2), "3": (3), "4": (4), "5": (5), "6": (6), "7": (7), "8": (8), "9": (9), "J": (10), "Q": (10), "K": (10)}
SUITSYMBOLS = {"H": "♥", "D": "♦", "C": "♣", "S": "♠"}
OPTIONS = ["surrender", "hit", "stand", "split", "double down", "h", "s", "x", "dd"]
OPTIONS2 = ["hit", "stand", "split", "h", "s", "x"]


class Card:

    def __init__(self, s, v, h) -> None:
        self.suit = s
        self.val = v
        self.hidden = h

    def __str__(self) -> str:
        if self.hidden:
            return f"┍━━━━━━━┑\n│+++++++│\n│+++++++│\n│+++++++│\n│+++++++│\n│+++++++│\n┕━━━━━━━┙\n"
        else:
            return f"┍━━━━━━━┑\n│{SUITSYMBOLS[self.suit]}      │\n│       │\n│   {self.val}   │\n│       │\n│      {SUITSYMBOLS[self.suit]}│\n┕━━━━━━━┙"
    
    def toString(self) -> str:
        if self.hidden:
            return f"┍━━━━━━━┑\n│+++++++│\n│+++++++│\n│+++++++│\n│+++++++│\n│+++++++│\n┕━━━━━━━┙\n"
        else:
            return f"┍━━━━━━━┑\n│{SUITSYMBOLS[self.suit]}      │\n│       │\n│   {self.val}   │\n│       │\n│      {SUITSYMBOLS[self.suit]}│\n┕━━━━━━━┙\n"
        
    def getVal(self) -> str:
        return self.val
    
    def hide(self):
        self.hidden = True
        return self

    def unhide(self) -> None:
        self.hidden = False
        return self
    
    def isHidden(self) -> None:
        return self.hidden

class Deck:
    def __init__(self) -> None:
        self.deck = []
    
    def addpacks(self, num) -> None:
        for i in range(num):
            for s in SUITSYMBOLS.keys():
                for v in VALSCORES.keys():
                    self.deck.append(Card(s, v, False))

    def __str__(self) -> str:
        out = ""
        for c in self.deck:
            out += c.toString()
        return out
    
    def prettyString(a: list) -> str:
        a = list(map(Card.toString, a))
        fullOut = ""
        for i in range(0,len(a),12):
            curr = a[i:i+12]
            curr = list(map(lambda x: x.split("\n"), curr))
            partOut = ""
            for j in range(len(curr[0])):
                for k in range(len(curr)):
                    partOut += curr[k][j]
                partOut += "\n"
            fullOut += partOut
        return fullOut

    def prettyPrint(self) -> str:
        print(Deck.prettyString(self.deck))

    def getRandom(self) -> Card:
        return self.deck.pop(random.randint(0, len(self.deck) - 1))
    
    def returnCards(self, cs: list) -> None:
        for c in cs:
            self.deck.append(c)


class Player:
    def __init__(self, n) -> None:
        self.name = n
        self.hand = []
        self.splitHands = []
        self.busted = False
        self.surrendered = False
        self.play = True
        self.chips = 0
        self.bet = 0

    def getHand(self):
        return self.hand
    
    def getName(self) -> str:
        return self.name
    
    def canPlay(self) -> bool:
        if self.chips == 0:
            return False
        return self.play
    
    def getSplitHands(self) -> list:
        return self.splitHands
    
    def isSurrendered(self) -> bool:
        return self.surrendered

    def surrender(self) -> None:
        self.play = False
        self.surrendered = True
        self.chips += self.bet//2
        self.bet = 0

    def reset(self) -> None:
        for sh in self.splitHands:
            self.addChips(sh.getChips())
            sh.setChips(0)
        self.play = True
        self.busted = False
        self.surrendered = False
        self.bet = 0

    def addChips(self, c: int) -> None:
        self.chips += c

    def removeChips(self, c: int) -> None:
        self.chips -= c

    def setChips(self, c: int) -> None:
        self.chips = c

    def getChips(self) -> int:
        return self.chips

    def addBet(self, b: int) -> bool:
        if b <= self.chips:
            self.bet += b
            self.chips -= b
            return True
        else:
            return False
        
    def getBet(self) -> int:
        return self.bet
    
    def setBet(self, b: int) -> None:
        self.bet = b
    
    def addSplit(self, b: int, sc: Card, nhc: Card, npc: Card):
        
        newHand = Player(self.name + f"{len(self.splitHands)+2}")
        newHand.addcard(sc)
        newHand.setBet(b)
        self.removeChips(b)
        self.addcard(npc)
        newHand.addcard(nhc)

    def isBusted(self) -> bool:
        return self.busted
    
    def showHand(self) -> None:
        for c in self.hand:
            c.unhide()
        
    def addcard(self, c) -> None:
        self.hand.append(c)
        self.hand.sort(key = lambda x: CARDORDERS[x.getVal()])
        self.hand.sort(key = lambda x: x.isHidden())

    def removecards(self) -> list:
        out = self.hand
        self.hand = []

        for h in self.splitHands:
            out += h.removecards()
        self.splitHands = []
        
        return out
    
    def score(self) -> int:
        cardVals = list(map(lambda x: VALSCORES[x.getVal()], self.hand))
        possHands = [cardVals]

        while any((1,11) in sl for sl in possHands):
            curr = possHands.pop(0)

            for i in range(len(curr)):
                if curr[i] == (1, 11):

                    a = (curr[0:i])+[1]+curr[i+1:]
                    possHands.append(a)

                    b = curr[0:i]+[11]+curr[i+1:]
                    possHands.append(b)
                    break
        

        possScores = list(map(sum, possHands))

        highest = -1

        for s in possScores:
            if s <= 21:
                if s > highest:
                    highest = s

        if highest == -1:
            self.play = False
            self.busted = True
        return highest
    
    def showing(self) -> int:
        cardVals = list(map(lambda x: VALSCORES[x.getVal()] if not x.isHidden() else 0, self.hand))
        possHands = [cardVals]

        while any((1,11) in sl for sl in possHands):
            curr = possHands.pop(0)

            for i in range(len(curr)):
                if curr[i] == (1, 11):

                    a = (curr[0:i])+[1]+curr[i+1:]
                    possHands.append(a)

                    b = curr[0:i]+[11]+curr[i+1:]
                    possHands.append(b)
                    break
        

        possScores = list(map(sum, possHands))

        highest = -1

        for s in possScores:
            if s <= 21:
                if s > highest:
                    highest = s

        if highest == -1:
            self.canPlay = False
            self.busted = True
        return highest

def split(p: Player, d: Deck) -> bool:
    if p.getChips() < p.getBet():
        print("Not Enough Chips To Split!")
        return False
    
    pHand = p.getHand()
    canSplit = []
    for t in VALSCORES.keys():
        if list(map(lambda x: x.getVal(), pHand)).count(t) >= 2:
            canSplit.append(t)
    if len(canSplit) == 0:
        print("Can't Split!")
    splitOp = ""
    while splitOp == "":
        pick = input("Pick Which Card Rank To Split")
        if pick.lower() not in canSplit:
            print("Invalid Selection!")
            return False
    
    for i in range(len(pHand)):
        if pHand[i].getVal == pick:
            p.addSplitHand(p.getBet(), pHand.pop(i), d.getRandom(), d.getRandom())
            print(f"Split {pick}'s")
    return True

def shSplit(sh: Player, p: Player, d: Deck) -> bool:
    if p.getChips() < p.getBet():
        print("Not Enough Chips To Split!")
        return False
    
    shHand = sh.getHand()
    canSplit = []
    for t in VALSCORES.keys():
        if list(map(lambda x: x.getVal(), shHand)).count(t) >= 2:
            canSplit.append(t)
    if len(canSplit) == 0:
        print("Can't Split!")
    splitOp = ""
    while splitOp == "":
        pick = input("Pick Which Card Rank To Split")
        if pick.lower() not in canSplit:
            print("Invalid Selection!")
            return False
    
    for i in range(len(shHand)):
        if shHand[i].getVal == pick:
            p.addSplitHand(p.getBet(), shHand.pop(i), d.getRandom(), d.getRandom())
            print(f"Split {pick}'s")
    return True
    
def main():
    d = Deck()
    d.addpacks(6)
    
    print(TITLE)

    numPlayers = -1

    while numPlayers == -1:

        num = input("How Many Players?? (Max 4) : ")
        try:
            inNum = int(num)
            if inNum > 4 or inNum <=0:
                print("Invalid Selection!")
                continue
            numPlayers = inNum
        except:
            print("Invalid Selection!")

        players = []

        dealer = Player("dealer")
        

        for i in range(numPlayers):
            pName = input(f"Enter Name For Player {i + 1}: ")
            newPlayer = Player(pName)
            players.append(newPlayer)
            cashin = -1

            while cashin == -1:
                num = input("Cash in: $")
                try:
                    inNum = int(num)
                    if inNum <=0:
                        print("Invalid Selection!")
                        continue
                    cashin = inNum
                except:
                    print("Invalid Selection!")
            newPlayer.addChips(cashin)


        os.system('cls')
        print(START)
        time.sleep(1)
        os.system('cls')

        while True:
            dealer.addcard(d.getRandom())
            dealer.addcard(d.getRandom().hide())
            
            for p in players:
                pBet = -1

                while pBet == -1:
                    num = input(f"{p.getName()}'s Chips: ${p.getChips()} | Bet: $")
                    try:
                        inNum = int(num)
                        if inNum > p.getChips() or inNum <=0:
                            print("Invalid Selection!")
                            continue
                        pBet = inNum
                    except:
                        print("Invalid Selection!")
                p.addBet(pBet)
                p.addcard(d.getRandom())
                p.addcard(d.getRandom())
            
            for p in players:
                
                initialRound = True
                while True:
                    os.system('cls')
                    if not p.canPlay() or p.score() == -1:
                        pscore = str(p.score()) if p.score() > 0 else "BUST!"
                        print(f"{p.getName()}'s Hand: {pscore}" )
                        print(Deck.prettyString(p.getHand()))
                        time.sleep(1.5)
                        break

                    if not p.canPlay():
                        pscore = str(p.score()) if p.score() > 0 else "BUST!"
                        print(f"{p.getName()}'s Hand: {pscore}" )
                        print(Deck.prettyString(p.getHand()))
                        time.sleep(1.5)
                        break

                    print(f"Dealer's Showing {dealer.showing()}...")
                    print(Deck.prettyString(dealer.getHand())+"\n")

                    print(f"{p.getName()}'s Turn...")

                    pscore = str(p.score()) if p.score() > 0 else "BUST!"
                    print(f"{p.getName()}'s Hand: {pscore} - Bet: ${p.getBet()} | Chips: ${p.getChips()}" )
                    print(Deck.prettyString(p.getHand()))

                    option = ""
                    while option == "":
                        if initialRound:
                            select = input("Surrender, Hit, Stand, Split, Double Down\n?: ")
                            if select.lower() not in OPTIONS:
                                print("Invalid Selection!")
                                continue
                            option = select
                            print("\n")
                        else:
                            select = input("Hit, Stand, Split\n?: ")
                            if select.lower() not in OPTIONS2:
                                print("Invalid Selection!")
                                continue
                            option = select
                            print("\n")
                            

                    match option.lower():
                        case "surrender":
                            p.surrender()
                            break  
                        case "hit":
                            p.addcard(d.getRandom())  
                            initialRound = False
                        case "h":
                            p.addcard(d.getRandom())
                            initialRound = False
                            
                            
                        case "stand":
                            break
                        case "s":
                            break
                        
                        case "split":
                            if not split(p, d):
                                continue
                        case "x":
                            if not split(p, d):
                                continue
                            
                        case "double down":
                            if not p.addBet(p.getBet()):
                                print("Can't Double Down!")
                                continue     
                            initialRound = False
                            p.addcard(d.getRandom())
                        case "dd":
                            if not p.addBet(p.getBet()):
                                print("Can't Double Down!")
                                continue     
                            initialRound = False
                            p.addcard(d.getRandom())




                for sh in p.getSplitHands():
                    initialRound = True
                    while True:
                        os.system('cls')
                        if not sh.canPlay():
                            shscore = str(sh.score()) if sh.score() > 0 else "BUST!"
                            print(f"{sh.getName()}'s Hand: {shscore} - Bet: ${sh.getBet()}" )
                            print(Deck.prettyString(sh.getHand()))
                            time.sleep(1.5)
                            break
                        print(f"Dealer's Showing {dealer.showing()}...")
                        print(Deck.prettyString(dealer.getHand())+"\n")

                        print(f"{sh.getName()}'s Turn...")

                        pscore = str(sh.score()) if sh.score() > 0 else "BUST!"
                        print(f"{sh.getName()}'s Hand: {shscore}" )
                        print(Deck.prettyString(sh.getHand()))

                        if not sh.canPlay():
                            break

                        option = ""
                        while option == "":
                            if initialRound:
                                select = input("Surrender, Hit, Stand, Split, Double Down\n?: ")
                                if select.lower() not in OPTIONS:
                                    print("Invalid Selection!")
                                    continue
                                option = select
                                print("\n")
                            else:
                                select = input("Hit, Stand, Split\n?: ")
                                if select.lower() not in OPTIONS2:
                                    print("Invalid Selection!")
                                    continue
                                option = select
                                print("\n")
                                

                        match option.lower():
                            case "surrender":
                                sh.surrender()
                                break  
                            case "hit":
                                initialRound = False
                                sh.addcard(d.getRandom())  
                            case "h":
                                initialRound = False
                                sh.addcard(d.getRandom())
                                
                                
                            case "stand":
                                break
                            case "s":
                                break
                            
                            case "split":
                                if not shSplit(sh, p, d):
                                    continue
                            case "x":
                                if not shSplit(sh, p, d):
                                    continue
                                
                            case "double down":                                
                                if sh.getBet() <= p.getChips:
                                    print("Can't Double Down!")
                                    continue
                                p.removeChips(p.getBet())
                                sh.setBet(p.getBet())
                                initialRound = False
                                sh.addcard(d.getRandom())

                            case "dd":
                                if sh.getBet() <= p.getChips:
                                    print("Can't Double Down!")
                                    continue
                                p.removeChips(p.getBet())
                                sh.addBet(p.getBet())
                                initialRound = False
                                sh.addcard(d.getRandom())

            
            os.system('cls')
            dealer.showHand()
            dShow = dealer.showing() if dealer.showing() >= 0 else "BUST!"
            print(f"Dealer's Showing {dShow}...")
            print(Deck.prettyString(dealer.getHand())+"\n")
            time.sleep(.5)

            allPlayers = players

            for p in players:
                allPlayers += p.getSplitHands()

            if any(list(map(lambda x: x.score() != -1, allPlayers))):
                while dealer.score() < 17 and dealer.score() != -1:
                    time.sleep(1)
                    os.system('cls')
                    dealer.addcard(d.getRandom())
                    dscore = dealer.score() if dealer.score() > 0 else "BUST!"
                    print(f"Dealer {dscore}...")
                    print(Deck.prettyString(dealer.getHand())+"\n")
            
            time.sleep(.5)
            dscore = dealer.score() if dealer.score() > 0 else "BUST!"
            print(f"Dealer : {dscore}\n")
            

            allPlayers.sort(key = lambda x: x.score(), reverse=True)
            for i in range(len(allPlayers)):
                pl = allPlayers[i]
                chipsWon = 0
                if pl.score() != -1:
                    if pl.score() == dealer.score():
                        pl.addChips(pl.getBet())
                    elif pl.score() > dealer.score():
                        chipsWon += pl.getBet()
                        pl.addChips(2 * pl.getBet())
                    else:
                        chipsWon -= pl.getBet()
                else:
                    chipsWon -= pl.getBet()
                score = pl.score() if pl.score() > 0 else "BUST!"
                print(f"{pl.getName()} : {score} | Round +/- {chipsWon} | Total: ${pl.getChips()}")


            input("\nEnter To Continue...")

            for p in players:
                d.returnCards(p.removecards())
                p.reset()
                




if __name__ == "__main__":
    main()