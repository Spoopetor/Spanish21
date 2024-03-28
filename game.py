import random
import time
import os

TITLE = "   _____                   _     _     ___  __\n  / ____|                 (_)   | |   |__ \/_ |\n | (___  _ __   __ _ _ __  _ ___| |__    ) || |\n  \___ \| '_ \ / _` | '_ \| / __| '_ \  / / | |\n  ____) | |_) | (_| | | | | \__ \ | | |/ /_ | |\n |_____/| .__/ \__,_|_| |_|_|___/_| |_|____||_|\n        | |                                    \n        |_|          \n"
START = "  _          _   _       ____             _       _ \n | |        | | ( )     |  _ \           (_)     | |\n | |     ___| |_|/ ___  | |_) | ___  __ _ _ _ __ | |\n | |    / _ \ __| / __| |  _ < / _ \/ _` | | '_ \| |\n | |___|  __/ |_  \__ \ | |_) |  __/ (_| | | | | |_|\n |______\___|\__| |___/ |____/ \___|\__, |_|_| |_(_)\n                                     __/ |          \n                                    |___/           "
CARDORDERS = {"A": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "J": 9, "Q": 10, "K": 11}
VALSCORES = {"A": (1, 11), "2": (2), "3": (3), "4": (4), "5": (5), "6": (6), "7": (7), "8": (8), "9": (9), "J": (10), "Q": (10), "K": (10)}
SUITSYMBOLS = {"H": "♥", "D": "♦", "C": "♣", "S": "♠"}
OPTIONS = ["surrender", "hit", "stand", "split", "double down", "h", "s", "dd"]


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

    def getHand(self):
        return self.hand
    
    def getName(self) -> str:
        return self.name
    
    def canPlay(self) -> bool:
        return self.play
    
    def getSplitHands(self) -> list:
        return self.splitHands
    
    def isSurrendered(self) -> bool:
        return self.surrendered

    def surrender(self) -> None:
        self.play = False
        self.surrendered = True

    def reset(self) -> None:
        self.play = True
        self.busted = False
        self.surrendered = False
    
    def addSplit(self, sc: Card, nhc: Card, npc: Card):
        
        newHand = Player(self.name + f"{len(self.splitHands)+2}")
        newHand.addcard(sc)
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
            players.append(Player(pName))

        os.system('cls')
        print(START)
        time.sleep(1)
        os.system('cls')

        while True:
            dealer.addcard(d.getRandom())
            dealer.addcard(d.getRandom().hide())
            
            for p in players:
                p.addcard(d.getRandom())
                p.addcard(d.getRandom())
            
            for p in players:
                
                while True:
                    os.system('cls')
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
                    print(f"{p.getName()}'s Hand: {pscore}" )
                    print(Deck.prettyString(p.getHand()))

                    if not p.canPlay():
                        break

                    option = ""
                    while option == "":
                        select = input("Surrender, Hit, Stand, Split, Double Down\n?: ")
                        if select.lower() not in OPTIONS:
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
                        case "h":
                            p.addcard(d.getRandom())
                            
                            
                        case "stand":
                            break
                        case "s":
                            break
                        
                        case "split":
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
                                    continue
                            
                            for i in range(len(pHand)):
                                if pHand[i].getVal == pick:
                                    p.addSplitHand(pHand.pop(i), d.getRandom(), d.getRandom())
                                    print(f"Split {pick}'s")
                            


                        case "double down":
                            p.addcard(d.getRandom())
                        case "dd":
                            p.addcard(d.getRandom())




                for sh in p.getSplitHands():

                    while True:
                        os.system('cls')
                        if not sh.canPlay():
                            shscore = str(sh.score()) if sh.score() > 0 else "BUST!"
                            print(f"{p.getName()}'s Hand: {shscore}" )
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
                            select = input("Surrender, Hit, Stand, Split, Double Down\n?: ")
                            if select.lower() not in OPTIONS:
                                print("Invalid Selection!")
                                continue
                            option = select
                            print("\n")
                                

                        match option.lower():
                            case "surrender":
                                sh.surrender()
                                break  
                            case "hit":
                                sh.addcard(d.getRandom())  
                            case "h":
                                sh.addcard(d.getRandom())
                                
                                
                            case "stand":
                                break
                            case "s":
                                break
                            
                            case "split":
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
                                        continue
                                
                                for i in range(len(pHand)):
                                    if shHand[i].getVal == pick:
                                        p.addSplitHand(shHand.pop(i), d.getRandom(), d.getRandom())
                                        print(f"Split {pick}'s")
                                
                            case "double down":
                                sh.addcard(d.getRandom())
                            case "dd":
                                sh.addcard(d.getRandom())

            
            os.system('cls')
            dealer.showHand()
            print(f"Dealer's Showing {dealer.showing()}...")
            print(Deck.prettyString(dealer.getHand())+"\n")
            time.sleep(.5)

            while dealer.score() < 17 and dealer.score() != -1:
                time.sleep(1)
                os.system('cls')
                dealer.addcard(d.getRandom())
                dscore = dealer.score() if dealer.score() > 0 else "BUST!"
                print(f"Dealer {dscore}...")
                print(Deck.prettyString(dealer.getHand())+"\n")
                
            
            time.sleep(.5)

            allplayers = [dealer]
            allplayers += players

            allplayers.sort(key = lambda x: x.score(), reverse=True)
            for i in range(len(allplayers)):
                pl = allplayers[i]
                score = pl.score() if pl.score() > 0 else "BUST!"
                print(f"{pl.getName()} : {score}")


            input("\nEnter To Continue...")

            for p in allplayers:
                d.returnCards(p.removecards())
                p.reset()
                




if __name__ == "__main__":
    main()