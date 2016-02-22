# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
total_games = 0
player = None
dealer = None
deck = None

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        ans = "Hand Contains "
        for card in self.cards:
            ans += str(card) + " "
        return ans

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        score = 0
        has_ace = False
        for card in self.cards:
            rank = card.get_rank()
            score += VALUES[rank]
            if rank == 'A':
                has_ace = True
        if has_ace:
            if score + 10 <= 21:
                return score + 10
            else:
                return score
        else:
            return score
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        for idx in (range(len(self.cards) if len(self.cards) <= 5 else 5)):
            self.cards[idx].draw(canvas, (pos[0] + i * CARD_SIZE[0], pos[1]))
            i += 1
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = [ Card(suit, rank) for suit in SUITS for rank in RANKS]
                                                      
    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop(random.randrange(len(self.cards)))
    
    def __str__(self):
        # return a string representing the deck
        ans = ""
        for card in self.cards:
            ans += str(card) + " "
        return ans                                                                        
                                                                        

#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, score, total_games
    if not in_play:
        deck = Deck()
        deck.shuffle()

        # Creating Player Hand
        player = Hand()
        player.add_card(deck.deal_card())
        player.add_card(deck.deal_card())


        # Creating Dealer Hand
        dealer = Hand()
        dealer.add_card(deck.deal_card())
        #dealer.add_card(deck.deal_card())
        in_play = True
        outcome = "Hit or Stand"
    else:
        total_games += 1
        in_play = False
        outcome = "Player Lost - New Deal?"
        

def hit():
    # replace with your code below
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global player, deck, outcome, in_play, total_games, dealer
    if player.get_value() <= 21 and in_play:
        player.add_card(deck.deal_card())
        if player.get_value() > 21:
            total_games += 1
            in_play = False
            dealer.add_card(deck.deal_card())
            outcome =  "Player Busted - New Deal?"        
            
def stand():
    # replace with your code below
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global in_play, score, outcome, total_games
    
    if in_play:
        if player.get_value() >= 21:
            total_games += 1
            dealer.add_card(deck.deal_card())
            outcome = "Player Busted - New Deal?"
        else:
            while True:
                dealer.add_card(deck.deal_card())
                if dealer.get_value() < 17:
                    continue
                elif dealer.get_value() <= 21:
                    dealer_val, player_val = dealer.get_value(), player.get_value()
                    if dealer_val >= player_val:
                        outcome = "Tie - New Deal?"
                    elif dealer_val < player_val:
                        total_games += 1
                        score += 1
                        outcome = "Player Wins - New Deal?"
                    break
                else:
                    total_games += 1
                    score += 1
                    outcome = "Dealer Busted - New Deal?"
                    break
        in_play = False
                    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", [150, 90], 50, 'Black')
    canvas.draw_text("Player", [50, 370], 25, 'Black')
    canvas.draw_text("Dealer", [50, 170], 25, 'Black')
    canvas.draw_text("Score " + str(score) + "-" + str(total_games - score), [300, 170], 25, 'Black')
    canvas.draw_text(outcome, [300, 370], 25, 'Red')
    
    player.draw(canvas, (50, 400))
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          (50 + CARD_BACK_CENTER[0] + CARD_SIZE[0], 200 + CARD_BACK_CENTER[1]), CARD_BACK_SIZE)
    dealer.draw(canvas, (50, 200))
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("White")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric